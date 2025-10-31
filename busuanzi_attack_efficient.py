#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
busuanzi_efficient.py

超高效的不蒜子访问量刷新工具
直接模拟 JS 发送的 JSONP 请求，无需启动浏览器

原理：
不蒜子 JS 会动态创建 script 标签，请求：
https://busuanzi.ibruce.info/busuanzi?jsonpCallback=BusuanziCallback_xxx
并带上 Referer 头，告诉服务器是从哪个页面访问的

我们直接用 urllib 模拟这个请求，速度比 Selenium 快 50+ 倍！

依赖：无需安装任何第三方库，使用 Python 标准库
"""
import urllib.request
import urllib.parse
import time
import random
import csv
import os
import json
import re
from datetime import datetime, timezone

# ============= 配置区域（在这里修改参数） =================
CONFIG = {
    "URL": "https://visitor-counter-cheater.vercel.app/",   # 目标网页 URL
    "MAX_VISITS": 100,          # 最大访问次数（设置为 0 表示无限次）
    "INTERVAL_MEAN": 1.0,       # 平均访问间隔（秒）
    "INTERVAL_MIN": 0.3,        # 最小间隔（秒）
    "CSV_FILE": "visits_log_efficient.csv",
    "TIMEOUT": 10,              # 请求超时时间（秒）
}
# ========================================================

# 常见设备的 User-Agent 列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-X906C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Safari/537.36",
]

def get_log_file_path():
    """获取日志文件路径，确保 logs 目录存在"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    return os.path.join(logs_dir, CONFIG["CSV_FILE"])

def now_iso():
    """返回当前 UTC 时间的 ISO 格式字符串"""
    return datetime.now(timezone.utc).isoformat()

def get_interval():
    """生成随机访问间隔时间（指数分布）"""
    interval = random.expovariate(1.0 / CONFIG["INTERVAL_MEAN"])
    return max(CONFIG["INTERVAL_MIN"], interval)

def write_csv_header(csvfile):
    """写入 CSV 文件头"""
    file_exists = os.path.exists(csvfile) and os.path.getsize(csvfile) > 0
    if not file_exists:
        with open(csvfile, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp_utc", 
                "visit_number", 
                "url", 
                "user_agent", 
                "status", 
                "response_time_ms",
                "site_pv",
                "page_pv",
                "site_uv",
                "page_uv",
                "note"
            ])

def log_visit(visit_num, url, user_agent, status, response_time, stats, note=""):
    """记录访问日志到 CSV"""
    log_file = get_log_file_path()
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            now_iso(),
            visit_num,
            url,
            user_agent,
            status,
            response_time,
            stats.get("site_pv", ""),
            stats.get("page_pv", ""),
            stats.get("site_uv", ""),
            stats.get("page_uv", ""),
            note
        ])

def visit_busuanzi(url, user_agent):
    """
    模拟不蒜子 JS 发送的请求
    
    关键：
    1. 请求地址：https://busuanzi.ibruce.info/busuanzi
    2. 参数：jsonpCallback=BusuanziCallback_随机数
    3. 必须带 Referer 头（你的页面 URL）
    """
    try:
        # 不蒜子 API 地址
        api_url = "https://busuanzi.ibruce.info/busuanzi"
        
        # 生成随机回调函数名（模拟 JS 的做法）
        callback = f"BusuanziCallback_{int(time.time() * 1000)}"
        
        # 构造完整 URL
        params = urllib.parse.urlencode({"jsonpCallback": callback})
        full_url = f"{api_url}?{params}"
        
        # 构造请求头，模拟真实浏览器
        headers = {
            "User-Agent": user_agent,
            "Referer": url,  # ⭐ 关键：告诉不蒜子是从哪个页面来的
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        # 创建请求对象
        req = urllib.request.Request(full_url, headers=headers)
        
        # 发送请求
        start_time = time.time()
        with urllib.request.urlopen(req, timeout=CONFIG["TIMEOUT"]) as response:
            data = response.read().decode('utf-8')
            response_time = int((time.time() - start_time) * 1000)  # 毫秒
        
        # 解析 JSONP 响应
        # 实际格式：try{BusuanziCallback_xxx({"site_pv":123,...});}catch(e){}
        # 使用更精确的正则：匹配括号内的 JSON 对象
        match = re.search(r'BusuanziCallback_\d+\((\{[^}]+\})\)', data)
        if match:
            json_str = match.group(1)  # 获取第一个捕获组（JSON 部分）
            
            try:
                stats = json.loads(json_str)
                return "SUCCESS", response_time, stats, ""
            except json.JSONDecodeError as e:
                return "ERROR", response_time, {}, f"JSON解析失败: {str(e)}"
        else:
            return "ERROR", response_time, {}, f"无法提取JSON，原始数据: {data[:200]}"
            
    except urllib.error.HTTPError as e:
        return "HTTP_ERROR", 0, {}, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return "URL_ERROR", 0, {}, str(e.reason)
    except TimeoutError:
        return "TIMEOUT", 0, {}, "请求超时"
    except Exception as e:
        return "EXCEPTION", 0, {}, str(e)

def main():
    """主函数"""
    url = CONFIG["URL"]
    max_visits = CONFIG["MAX_VISITS"]
    log_file = get_log_file_path()
    
    print(f"🚀 开始超高效访问任务（直接模拟 JS 请求）")
    print(f"📍 目标网页: {url}")
    print(f"🔢 最大访问次数: {max_visits if max_visits > 0 else '无限'}")
    print(f"⏱️  平均间隔: {CONFIG['INTERVAL_MEAN']} 秒（最小 {CONFIG['INTERVAL_MIN']} 秒）")
    print(f"💾 日志文件: {log_file}")
    print(f"⚡ 性能: 比 Selenium 快 50+ 倍！无需启动浏览器！")
    print(f"📚 使用标准库: 无需安装任何第三方包")
    print("=" * 70)
    
    write_csv_header(log_file)
    
    visit_count = 0
    success_count = 0
    total_response_time = 0
    
    try:
        while True:
            # 检查是否达到最大访问次数
            if max_visits > 0 and visit_count >= max_visits:
                print(f"\n✅ 已完成 {visit_count} 次访问，达到最大访问次数")
                break
            
            visit_count += 1
            
            # 随机选择 User-Agent
            user_agent = random.choice(USER_AGENTS)
            
            print(f"\n[访问 #{visit_count}]")
            print(f"  🌐 UA: {user_agent[:75]}...")
            
            # 发送请求
            status, response_time, stats, note = visit_busuanzi(url, user_agent)
            
            if status == "SUCCESS":
                success_count += 1
                total_response_time += response_time
                print(f"  ✅ 访问成功 ({response_time}ms)")
                print(f"  📊 页面PV: {stats.get('page_pv', 'N/A')} | 页面UV: {stats.get('page_uv', 'N/A')}")
                print(f"  🌍 站点PV: {stats.get('site_pv', 'N/A')} | 站点UV: {stats.get('site_uv', 'N/A')}")
            else:
                print(f"  ❌ {status}: {note}")
            
            # 记录日志
            log_visit(visit_count, url, user_agent, status, response_time, stats, note)
            
            # 如果还没达到最大次数，等待下一次访问
            if max_visits == 0 or visit_count < max_visits:
                interval = get_interval()
                print(f"  ⏳ 等待 {interval:.1f} 秒...")
                time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断程序")
    
    finally:
        # 统计信息
        print(f"\n{'='*70}")
        print(f"📊 访问统计")
        print(f"{'='*70}")
        print(f"总访问次数: {visit_count}")
        print(f"成功次数: {success_count}")
        if visit_count > 0:
            print(f"成功率: {success_count/visit_count*100:.1f}%")
        if success_count > 0:
            print(f"平均响应时间: {total_response_time/success_count:.0f}ms")
        print(f"💾 日志已保存到: {log_file}")

if __name__ == "__main__":
    main()
