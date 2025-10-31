#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import uuid
import csv
from datetime import datetime
import requests

# ====================== 配 置 ======================
CONFIG = {
    # 目标地址（示例：内网穿透后的域名 + 页面路径）
    "URL": "https://visitor-counter-cheater.vercel.app/",

    # 基础间隔（秒）：例如每小时一次 3600；快速验证可改小如 5
    "INTERVAL": 10,

    # 抖动（秒）：每轮会在 INTERVAL 上加一个 [-JITTER, +JITTER] 的随机值
    "JITTER": 0.3,

    # 运行轮数：0 表示无限循环（Ctrl+C 结束）；否则按次数停止
    "RUNS": 0,

    # 设备ID池大小：每次随机挑一个作为 X-Device-ID
    "DEVICES": 20,

    # HTTP 请求超时（秒）
    "TIMEOUT": 10.0,

    # 输出 CSV 文件名
    "CSV_FILE": "visits_log.csv",

    # （可改）可选的 UA 列表
    "USER_AGENTS": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TestClient/1.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) SimBrowser/0.9",
        "VisitProbe/2.3 (+https://example.local/)",
        "LocalTester/0.1",
    ],

    # 固定随机种子（可留 None；设定后便于复现实验）
    "SEED": None,
}
# ==================== 配 置 结 束 ===================


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def gen_devices(n: int):
    return [str(uuid.uuid4()) for _ in range(n)]

def main():
    url = CONFIG["URL"]

    if CONFIG["SEED"] is not None:
        random.seed(CONFIG["SEED"])

    # 准备 CSV 头
    try:
        with open(CONFIG["CSV_FILE"], "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if f.tell() == 0:
                w.writerow(["timestamp_utc", "run_index", "url", "device_id",
                            "user_agent", "status", "http_code", "elapsed_s", "note"])
    except Exception as e:
        print("无法写入 CSV 文件：", e)
        return

    devices = gen_devices(CONFIG["DEVICES"])
    session = requests.Session()

    run = 0
    print(f"开始运行：{url}")
    print(f"interval={CONFIG['INTERVAL']}s  jitter=±{CONFIG['JITTER']}s  devices={CONFIG['DEVICES']}")
    print("按 Ctrl+C 结束。")

    try:
        while True:
            if CONFIG["RUNS"] > 0 and run >= CONFIG["RUNS"]:
                print("完成指定轮次，退出。")
                break
            run += 1

            dev = random.choice(devices)
            ua = random.choice(CONFIG["USER_AGENTS"])
            ts = now_iso()
            status = "SENT"
            http_code = ""
            elapsed = ""
            note = ""

            try:
                headers = {"User-Agent": ua, "X-Device-ID": dev}
                t0 = time.time()
                r = session.get(url, headers=headers, timeout=CONFIG["TIMEOUT"])
                elapsed = f"{time.time() - t0:.3f}"
                http_code = str(r.status_code)
                status = "OK" if r.status_code < 400 else "ERR_STATUS"
            except Exception as e:
                status = "EXCEPTION"
                note = f"{type(e).__name__}:{e}"

            # 写日志
            try:
                with open(CONFIG["CSV_FILE"], "a", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerow([ts, run, url, dev, ua, status, http_code, elapsed, note])
            except Exception as e:
                print("写 CSV 失败：", e)

            print(f"[run {run}] {ts} dev={dev[:8]}.. status={status} code={http_code} elapsed={elapsed} note={note}")

            # 计算等待（interval + jitter）
            interval = CONFIG["INTERVAL"]
            jitter = CONFIG["JITTER"]
            total_wait = max(0.0, interval + (random.uniform(-jitter, jitter) if jitter > 0 else 0.0))

            # 分段睡眠便于 Ctrl+C 立即响应
            remaining = total_wait
            step = 10.0
            while remaining > 0:
                t = min(step, remaining)
                time.sleep(t)
                remaining -= t


    except KeyboardInterrupt:
        print("\n用户中止。日志已写入：", CONFIG["CSV_FILE"])

if __name__ == "__main__":
    main()
