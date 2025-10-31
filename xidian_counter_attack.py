#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西电教师主页访问量刷新工具 (高效版)

原理分析：
页面加载时会调用 _tsites_updateVisit_() 函数
该函数会发送一个图片请求到：
/system/resource/tsites/click.jsp?lc={path}&hosts={host}&ac=updateVisit&vp=&os={OS}&bs={browser}

我们直接模拟这个请求即可！
"""
import urllib.request
import urllib.parse
import time
import random
import csv
import os
from datetime import datetime, timezone

# ============= 配置区域 =================
CONFIG = {
    "URL": "https://faculty.xidian.edu.cn/DANIEL/zh_CN/index.htm",
    "MAX_VISITS": 100,          # 最大访问次数
    "INTERVAL_MEAN": 1.0,       # 平均间隔（秒）
    "INTERVAL_MIN": 0.5,        # 最小间隔（秒）
    "CSV_FILE": "visits_log_xidian.csv",
    "TIMEOUT": 10,
}
# ========================================

# 操作系统列表
OS_LIST = [
    "Win10 64位",
    "Win10 32位",
    "Win7 64位",
    "Win7 32位",
    "Mac 64位",
    "Linux 64位",
    "Android 64位",
]

# 浏览器列表
BROWSER_LIST = [
    "Chrome",
    "Firefox",
    "Microsoft IE",
    "Safari",
    "Edge",
]

# User-Agent 列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def get_log_file_path():
    """获取日志文件路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    return os.path.join(logs_dir, CONFIG["CSV_FILE"])

def now_iso():
    """返回当前 UTC 时间"""
    return datetime.now(timezone.utc).isoformat()

def get_interval():
    """生成随机间隔"""
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
                "os",
                "browser",
                "status",
                "response_time_ms",
                "note"
            ])

def log_visit(visit_num, url, user_agent, os, browser, status, response_time, note=""):
    """记录访问日志"""
    log_file = get_log_file_path()
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            now_iso(),
            visit_num,
            url,
            user_agent,
            os,
            browser,
            status,
            response_time,
            note
        ])

def update_visit(target_url, user_agent, os, browser):
    """
    模拟访问量更新请求
    
    关键请求：
    /system/resource/tsites/click.jsp?lc={pathname}&hosts={host}&ac=updateVisit&vp=&os={OS}&bs={browser}
    """
    try:
        # 解析目标 URL
        from urllib.parse import urlparse
        parsed = urlparse(target_url)
        pathname = parsed.path
        hosts = parsed.netloc
        
        # 构造计数器请求的 URL
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        click_url = base_url + "/system/resource/tsites/click.jsp"
        
        # 构造参数
        params = {
            "lc": pathname,
            "hosts": hosts,
            "ac": "updateVisit",
            "vp": "",  # visite_record_collect_params，通常为空
            "os": os,
            "bs": browser
        }
        
        # 编码参数
        query_string = urllib.parse.urlencode(params)
        full_url = f"{click_url}?{query_string}"
        
        # 构造请求头
        headers = {
            "User-Agent": user_agent,
            "Referer": target_url,
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
        }
        
        # 发送请求
        req = urllib.request.Request(full_url, headers=headers)
        start_time = time.time()
        
        with urllib.request.urlopen(req, timeout=CONFIG["TIMEOUT"]) as response:
            data = response.read()
            response_time = int((time.time() - start_time) * 1000)
        
        return "SUCCESS", response_time, ""
        
    except urllib.error.HTTPError as e:
        return "HTTP_ERROR", 0, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return "URL_ERROR", 0, str(e.reason)
    except Exception as e:
        return "EXCEPTION", 0, str(e)

def main():
    """主函数"""
    url = CONFIG["URL"]
    max_visits = CONFIG["MAX_VISITS"]
    log_file = get_log_file_path()
    
    print("🎯 西电教师主页访问量刷新工具")
    print("=" * 70)
    print(f"📍 目标网址: {url}")
    print(f"🔢 最大访问次数: {max_visits if max_visits > 0 else '无限'}")
    print(f"⏱️  平均间隔: {CONFIG['INTERVAL_MEAN']} 秒")
    print(f"💾 日志文件: {log_file}")
    print(f"⚡ 原理: 直接模拟 click.jsp 请求")
    print("=" * 70)
    
    write_csv_header(log_file)
    
    visit_count = 0
    success_count = 0
    total_response_time = 0
    
    try:
        while True:
            if max_visits > 0 and visit_count >= max_visits:
                print(f"\n✅ 已完成 {visit_count} 次访问")
                break
            
            visit_count += 1
            
            # 随机选择参数
            user_agent = random.choice(USER_AGENTS)
            os = random.choice(OS_LIST)
            browser = random.choice(BROWSER_LIST)
            
            print(f"\n[访问 #{visit_count}]")
            print(f"  🖥️  OS: {os}")
            print(f"  🌐 Browser: {browser}")
            print(f"  📱 UA: {user_agent[:60]}...")
            
            # 发送请求
            status, response_time, note = update_visit(url, user_agent, os, browser)
            
            if status == "SUCCESS":
                success_count += 1
                total_response_time += response_time
                print(f"  ✅ 访问成功 ({response_time}ms)")
            else:
                print(f"  ❌ {status}: {note}")
            
            # 记录日志
            log_visit(visit_count, url, user_agent, os, browser, status, response_time, note)
            
            # 等待
            if max_visits == 0 or visit_count < max_visits:
                interval = get_interval()
                print(f"  ⏳ 等待 {interval:.1f} 秒...")
                time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断程序")
    
    finally:
        print(f"\n{'='*70}")
        print(f"📊 统计信息")
        print(f"{'='*70}")
        print(f"总访问次数: {visit_count}")
        print(f"成功次数: {success_count}")
        if visit_count > 0:
            print(f"成功率: {success_count/visit_count*100:.1f}%")
        if success_count > 0:
            print(f"平均响应时间: {total_response_time/success_count:.0f}ms")
        print(f"💾 日志: {log_file}")

if __name__ == "__main__":
    main()
