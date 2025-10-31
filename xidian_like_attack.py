#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西电教师主页点赞刷新工具

原理分析：
页面使用 TsitesPraiseUtil.js 实现点赞功能
点赞请求发送到：/system/resource/tsites/praise.jsp

关键发现：
1. 使用 Cookie 限制（key: tsites_praise_{uid}）
2. 24小时内同一Cookie不能重复点赞
3. 但我们可以：
   - 每次使用不同的 Session（清空Cookie）
   - 模拟不同的设备/浏览器
   
参数：
- uid: 6799
- homepageid: 24515
- apptype: teacher
- contentid: 0
- pdtype: 0
- ac: updatePraise
"""
import urllib.request
import urllib.parse
import http.cookiejar
import time
import random
import csv
import os
import json
from datetime import datetime, timezone

# ============= 配置区域 =================
CONFIG = {
    "URL": "https://faculty.xidian.edu.cn/DANIEL/zh_CN/index.htm",
    "MAX_LIKES": 100,            # 最大点赞次数
    "INTERVAL_MEAN": 2.0,        # 平均间隔（秒）
    "INTERVAL_MIN": 1.0,         # 最小间隔（秒）
    "CSV_FILE": "likes_log_xidian.csv",
    "TIMEOUT": 10,
    
    # 从页面中提取的参数
    "UID": "6799",
    "HOMEPAGEID": "24515",
    "APPTYPE": "teacher",
    "CONTENTID": "0",
    "PDTYPE": "0",
}
# ========================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
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
                "like_number",
                "user_agent",
                "status",
                "response_time_ms",
                "result",
                "praise_count",
                "note"
            ])

def log_like(like_num, user_agent, status, response_time, result, praise_count, note=""):
    """记录点赞日志"""
    log_file = get_log_file_path()
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            now_iso(),
            like_num,
            user_agent,
            status,
            response_time,
            result,
            praise_count,
            note
        ])

def send_like(user_agent):
    """
    发送点赞请求
    
    关键：每次创建新的 CookieJar，模拟不同的用户
    """
    try:
        # 创建新的 Cookie 管理器（每次都是新的 Session）
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        
        # 点赞接口
        praise_url = "https://faculty.xidian.edu.cn/system/resource/tsites/praise.jsp"
        
        # 构造 POST 参数
        params = {
            "uid": CONFIG["UID"],
            "homepageid": CONFIG["HOMEPAGEID"],
            "apptype": CONFIG["APPTYPE"],
            "contentid": CONFIG["CONTENTID"],
            "pdtype": CONFIG["PDTYPE"],
            "ac": "updatePraise"
        }
        
        data = urllib.parse.urlencode(params).encode('utf-8')
        
        # 构造请求头
        headers = {
            "User-Agent": user_agent,
            "Referer": CONFIG["URL"],
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://faculty.xidian.edu.cn",
            "Connection": "keep-alive",
        }
        
        # 发送请求
        req = urllib.request.Request(praise_url, data=data, headers=headers)
        start_time = time.time()
        
        response = opener.open(req, timeout=CONFIG["TIMEOUT"])
        response_data = response.read().decode('utf-8')
        response_time = int((time.time() - start_time) * 1000)
        
        # 解析响应
        try:
            result = json.loads(response_data)
            # 响应格式：{"result": true/false, "praise": 点赞数}
            if result.get("result"):
                praise_count = result.get("praise", "N/A")
                return "SUCCESS", response_time, result, praise_count, ""
            else:
                return "FAILED", response_time, result, "N/A", "服务器返回 result=false"
        except json.JSONDecodeError:
            return "ERROR", response_time, {}, "N/A", f"JSON解析失败: {response_data[:100]}"
        
    except urllib.error.HTTPError as e:
        return "HTTP_ERROR", 0, {}, "N/A", f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return "URL_ERROR", 0, {}, "N/A", str(e.reason)
    except Exception as e:
        return "EXCEPTION", 0, {}, "N/A", str(e)

def get_current_likes():
    """
    获取当前的点赞数
    """
    try:
        praise_url = "https://faculty.xidian.edu.cn/system/resource/tsites/praise.jsp"
        
        params = {
            "uid": CONFIG["UID"],
            "homepageid": CONFIG["HOMEPAGEID"],
            "apptype": CONFIG["APPTYPE"],
            "contentid": CONFIG["CONTENTID"],
            "pdtype": CONFIG["PDTYPE"],
            "basenum": "0",
            "ac": "getPraise"
        }
        
        data = urllib.parse.urlencode(params).encode('utf-8')
        
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        
        req = urllib.request.Request(praise_url, data=data, headers=headers)
        
        with urllib.request.urlopen(req, timeout=CONFIG["TIMEOUT"]) as response:
            response_data = response.read().decode('utf-8')
            result = json.loads(response_data)
            return result.get("praise", "N/A")
            
    except Exception as e:
        return f"ERROR: {e}"

def main():
    """主函数"""
    max_likes = CONFIG["MAX_LIKES"]
    log_file = get_log_file_path()
    
    print("👍 西电教师主页点赞刷新工具")
    print("=" * 70)
    print(f"📍 目标: {CONFIG['URL']}")
    print(f"👤 UID: {CONFIG['UID']}")
    print(f"🏠 Homepage ID: {CONFIG['HOMEPAGEID']}")
    
    # 获取当前点赞数
    print(f"\n🔍 正在查询当前点赞数...")
    current_likes = get_current_likes()
    print(f"📊 当前点赞数: {current_likes}")
    
    print(f"\n🔢 目标点赞次数: {max_likes}")
    print(f"⏱️  平均间隔: {CONFIG['INTERVAL_MEAN']} 秒")
    print(f"💾 日志文件: {log_file}")
    print(f"⚡ 策略: 每次使用新 Session（清空 Cookie）")
    print("=" * 70)
    
    write_csv_header(log_file)
    
    like_count = 0
    success_count = 0
    total_response_time = 0
    
    try:
        while True:
            if max_likes > 0 and like_count >= max_likes:
                print(f"\n✅ 已完成 {like_count} 次点赞")
                break
            
            like_count += 1
            
            # 随机选择 User-Agent
            user_agent = random.choice(USER_AGENTS)
            
            print(f"\n[点赞 #{like_count}]")
            print(f"  📱 UA: {user_agent[:60]}...")
            
            # 发送点赞
            status, response_time, result, praise_count, note = send_like(user_agent)
            
            if status == "SUCCESS":
                success_count += 1
                total_response_time += response_time
                print(f"  ✅ 点赞成功 ({response_time}ms)")
                print(f"  📊 当前总点赞数: {praise_count}")
            else:
                print(f"  ❌ {status}: {note}")
                if result:
                    print(f"     响应: {result}")
            
            # 记录日志
            log_like(like_count, user_agent, status, response_time, result, praise_count, note)
            
            # 等待
            if max_likes == 0 or like_count < max_likes:
                interval = get_interval()
                print(f"  ⏳ 等待 {interval:.1f} 秒...")
                time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断程序")
    
    finally:
        # 再次查询最终点赞数
        print(f"\n🔍 查询最终点赞数...")
        final_likes = get_current_likes()
        
        print(f"\n{'='*70}")
        print(f"📊 点赞统计")
        print(f"{'='*70}")
        print(f"初始点赞数: {current_likes}")
        print(f"最终点赞数: {final_likes}")
        if isinstance(current_likes, int) and isinstance(final_likes, int):
            print(f"增加数量: +{final_likes - current_likes}")
        print(f"\n尝试点赞次数: {like_count}")
        print(f"成功次数: {success_count}")
        if like_count > 0:
            print(f"成功率: {success_count/like_count*100:.1f}%")
        if success_count > 0:
            print(f"平均响应时间: {total_response_time/success_count:.0f}ms")
        print(f"💾 日志: {log_file}")

if __name__ == "__main__":
    main()
