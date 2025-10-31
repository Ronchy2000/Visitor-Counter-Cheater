#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visitor-badge 访客计数器刷新工具

服务: https://visitor-badge.laobi.icu
原理: 每次请求badge的SVG图片URL，服务器都会增加访客计数

特点:
- 无需Selenium
- 纯HTTP请求
- 速度极快
- 支持任意URL输入（自动提取page_id）
"""
import urllib.request
import urllib.parse
import time
import random
import csv
import os
import re
from datetime import datetime, timezone

# ============= 配置区域 =================
CONFIG = {
    # 目标URL（支持GitHub仓库地址或直接的page_id）
    # 示例: "https://github.com/Ronchy2000/Visitor-Counter-Cheater"
    # 或: "ronchy2000.Visitor-Counter-Cheater"
    "TARGET_URL": "https://github.com/Ronchy2000/Visitor-Counter-Cheater",
    
    # 可选的样式参数
    "STYLE": "for-the-badge",  # 或 "flat", "flat-square", "plastic"
    "COLOR": "00d4ff",         # 徽章颜色
    
    "MAX_VISITS": 100,         # 最大访问次数
    "INTERVAL_MEAN": 1.0,      # 平均间隔（秒）
    "INTERVAL_MIN": 0.3,       # 最小间隔（秒）
    "CSV_FILE": "visitor_badge_log.csv",
    "TIMEOUT": 10,
}
# ========================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
]

def extract_page_id(target_url):
    """
    从URL或字符串中提取page_id
    
    支持格式:
    - https://github.com/用户名/项目名
    - github.com/用户名/项目名
    - 用户名/项目名
    - 用户名.项目名
    
    返回: page_id (格式: 用户名.项目名)
    """
    target_url = target_url.strip()
    
    # 如果已经是 用户名.项目名 格式
    if '.' in target_url and '/' not in target_url and 'http' not in target_url:
        return target_url
    
    # 移除协议和域名
    target_url = re.sub(r'^https?://', '', target_url)
    target_url = re.sub(r'^(www\.)?github\.com/', '', target_url)
    
    # 提取 用户名/项目名
    match = re.match(r'^([^/]+)/([^/]+)', target_url)
    if match:
        username, repo = match.groups()
        # 移除可能的 .git 后缀
        repo = re.sub(r'\.git$', '', repo)
        return f"{username}.{repo}"
    
    # 如果无法解析，返回原始字符串
    return target_url

def get_log_file_path():
    """获取日志文件路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    return os.path.join(logs_dir, CONFIG["CSV_FILE"])

def now_iso():
    """返回当前时间"""
    return datetime.now(timezone.utc).isoformat()

def get_interval():
    """生成随机间隔"""
    interval = random.expovariate(1.0 / CONFIG["INTERVAL_MEAN"])
    return max(CONFIG["INTERVAL_MIN"], interval)

def write_csv_header(csvfile):
    """写入CSV文件头"""
    file_exists = os.path.exists(csvfile) and os.path.getsize(csvfile) > 0
    if not file_exists:
        with open(csvfile, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp_utc",
                "visit_number",
                "page_id",
                "user_agent",
                "status",
                "response_time_ms",
                "visitor_count",
                "note"
            ])

def log_visit(visit_num, page_id, user_agent, status, response_time, visitor_count, note=""):
    """记录访问日志"""
    log_file = get_log_file_path()
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            now_iso(),
            visit_num,
            page_id,
            user_agent,
            status,
            response_time,
            visitor_count,
            note
        ])

def get_visitor_count(page_id, user_agent, update_count=True):
    """
    访问visitor-badge服务
    
    参数:
        page_id: GitHub页面ID (格式: 用户名.项目名)
        user_agent: User-Agent字符串
        update_count: True=增加计数, False=只查询
    
    返回:
        (status, response_time, visitor_count, note)
    """
    try:
        # 构造URL
        base_url = "https://visitor-badge.laobi.icu/badge"
        
        params = {
            "page_id": page_id,
        }
        
        # 添加样式参数（可选）
        if CONFIG.get("STYLE"):
            params["style"] = CONFIG["STYLE"]
        if CONFIG.get("COLOR"):
            params["color"] = CONFIG["COLOR"]
        
        # 只查询模式
        if not update_count:
            params["query_only"] = "true"
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{query_string}"
        
        # 构造请求头
        headers = {
            "User-Agent": user_agent,
            "Accept": "image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": f"https://github.com/{page_id.replace('.', '/')}",
        }
        
        # 发送请求
        req = urllib.request.Request(full_url, headers=headers)
        start_time = time.time()
        
        with urllib.request.urlopen(req, timeout=CONFIG["TIMEOUT"]) as response:
            data = response.read()
            response_time = int((time.time() - start_time) * 1000)
        
        # 解析SVG，提取访客数
        if data.startswith(b'<svg') or data.startswith(b'<?xml'):
            svg_text = data.decode('utf-8')
            # 从SVG中提取数字（通常是最后一个数字）
            numbers = re.findall(r'>(\d+)<', svg_text)
            if numbers:
                visitor_count = int(numbers[-1])
                return "SUCCESS", response_time, visitor_count, ""
            else:
                return "ERROR", response_time, None, "无法从SVG中提取访客数"
        else:
            return "ERROR", response_time, None, f"返回的不是SVG格式: {data[:50]}"
        
    except urllib.error.HTTPError as e:
        return "HTTP_ERROR", 0, None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return "URL_ERROR", 0, None, str(e.reason)
    except Exception as e:
        return "EXCEPTION", 0, None, str(e)

def main():
    """主函数"""
    target_url = CONFIG["TARGET_URL"]
    page_id = extract_page_id(target_url)
    max_visits = CONFIG["MAX_VISITS"]
    log_file = get_log_file_path()
    
    print("🎯 visitor-badge 访客计数器刷新工具")
    print("=" * 70)
    print(f"🌐 目标URL: {target_url}")
    print(f"📍 Page ID: {page_id}")
    print(f"🔗 服务: visitor-badge.laobi.icu")
    print(f"🎨 样式: {CONFIG.get('STYLE', '默认')}")
    print(f"🎨 颜色: #{CONFIG.get('COLOR', '默认')}")
    
    # 查询当前访客数
    print(f"\n🔍 查询当前访客数...")
    status, _, current_count, note = get_visitor_count(page_id, random.choice(USER_AGENTS), update_count=False)
    
    if status == "SUCCESS":
        print(f"📊 当前访客数: {current_count}")
    else:
        print(f"⚠️  查询失败: {note}")
        current_count = "未知"
    
    print(f"\n🔢 目标访问次数: {max_visits}")
    print(f"⏱️  平均间隔: {CONFIG['INTERVAL_MEAN']} 秒")
    print(f"💾 日志文件: {log_file}")
    print(f"⚡ 策略: 直接请求badge URL")
    print("=" * 70)
    
    write_csv_header(log_file)
    
    visit_count = 0
    success_count = 0
    total_response_time = 0
    last_visitor_count = current_count if isinstance(current_count, int) else 0
    
    try:
        while True:
            if max_visits > 0 and visit_count >= max_visits:
                print(f"\n✅ 已完成 {visit_count} 次访问")
                break
            
            visit_count += 1
            
            # 随机选择User-Agent
            user_agent = random.choice(USER_AGENTS)
            
            print(f"\n[访问 #{visit_count}]")
            print(f"  📱 UA: {user_agent[:60]}...")
            
            # 发送请求（会增加计数）
            status, response_time, visitor_count_val, note = get_visitor_count(
                page_id, user_agent, update_count=True
            )
            
            if status == "SUCCESS":
                success_count += 1
                total_response_time += response_time
                print(f"  ✅ 访问成功 ({response_time}ms)")
                print(f"  📊 访客数: {visitor_count_val}")
                
                if isinstance(last_visitor_count, int) and isinstance(visitor_count_val, int):
                    increase = visitor_count_val - last_visitor_count
                    if increase > 0:
                        print(f"  📈 增加: +{increase}")
                
                last_visitor_count = visitor_count_val
            else:
                print(f"  ❌ {status}: {note}")
            
            # 记录日志
            log_visit(visit_count, page_id, user_agent, status, response_time, visitor_count_val, note)
            
            # 等待
            if max_visits == 0 or visit_count < max_visits:
                interval = get_interval()
                print(f"  ⏳ 等待 {interval:.1f} 秒...")
                time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断程序")
    
    finally:
        # 查询最终访客数
        print(f"\n🔍 查询最终访客数...")
        status, _, final_count, _ = get_visitor_count(page_id, random.choice(USER_AGENTS), update_count=False)
        
        print(f"\n{'='*70}")
        print(f"📊 访问统计")
        print(f"{'='*70}")
        print(f"初始访客数: {current_count}")
        print(f"最终访客数: {final_count}")
        
        if isinstance(current_count, int) and isinstance(final_count, int):
            print(f"增加数量: +{final_count - current_count}")
        
        print(f"\n尝试访问次数: {visit_count}")
        print(f"成功次数: {success_count}")
        if visit_count > 0:
            print(f"成功率: {success_count/visit_count*100:.1f}%")
        if success_count > 0:
            print(f"平均响应时间: {total_response_time/success_count:.0f}ms")
        print(f"💾 日志: {log_file}")

if __name__ == "__main__":
    main()
