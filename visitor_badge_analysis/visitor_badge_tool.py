#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visitor-badge 访客计数器工具

服务: https://visitor-badge.laobi.icu
功能: 查询访客数 / 增加访客数
"""
import urllib.request
import urllib.parse
import json
import re
import time

def extract_visitor_count(svg_data):
    """从SVG数据中提取访客数"""
    if svg_data.startswith(b'<svg'):
        svg_text = svg_data.decode('utf-8')
        numbers = re.findall(r'>(\d+)<', svg_text)
        if numbers:
            return numbers[-1]
    return None

def parse_github_repo(input_str):
    """解析GitHub仓库输入，支持 username/repo 或 GitHub链接"""
    input_str = input_str.strip()
    
    # 如果是GitHub URL，提取username/repo
    if 'github.com' in input_str:
        # 匹配 github.com/username/repo 格式
        match = re.search(r'github\.com/([^/]+)/([^/?#]+)', input_str)
        if match:
            username, repo = match.groups()
            return f"{username}/{repo}"
    
    # 否则假定已经是 username/repo 格式
    return input_str

def get_page_id(github_repo):
    """从GitHub仓库获取page_id"""
    github_url = f"https://github.com/{github_repo}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(github_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # 匹配visitor-badge链接，提取page_id参数
        # 处理HTML实体编码 (&amp; 和 \u0026)
        pattern = r'visitor-badge\.laobi\.icu/badge\?page_id=([^"\'&\\]+)'
        matches = re.findall(pattern, html, re.IGNORECASE)
        
        if matches:
            page_id = matches[0]
            # 清理可能的尾部符号
            page_id = page_id.rstrip('\\').rstrip()
            print(f"📍 从README中提取到 page_id: {page_id}")
            return page_id
        else:
            # 使用默认格式
            page_id = github_repo.replace('/', '.')
            print(f"⚠️  未找到visitor-badge，使用默认格式: {page_id}")
            return page_id
    except Exception as e:
        print(f"❌ 获取page_id失败: {e}")
        # 使用默认格式
        return github_repo.replace('/', '.')

def query_visitor_count(page_id):
    """查询访客数（不增加计数）"""
    url = f"https://visitor-badge.laobi.icu/badge?page_id={page_id}&query_only=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            count = extract_visitor_count(data)
            if count:
                print(f"📊 当前访客数: {count}")
                return count
            else:
                print("❌ 无法提取访客数")
                return None
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return None

def visit_once(page_id):
    """访问一次（增加计数）"""
    url = f"https://visitor-badge.laobi.icu/badge?page_id={page_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            count = extract_visitor_count(data)
            return count
    except Exception as e:
        print(f"❌ 访问失败: {e}")
        return None

def visit_multiple(page_id, times, delay=0.5):
    """批量访问（增加计数）"""
    success_count = 0
    print(f"\n🚀 开始批量访问，目标次数: {times}")
    print("-" * 60)
    
    for i in range(times):
        count = visit_once(page_id)
        if count:
            success_count += 1
            print(f"[{i+1}/{times}] ✅ 成功 - 当前访客数: {count}")
        else:
            print(f"[{i+1}/{times}] ❌ 失败")
        
        if i < times - 1:  # 最后一次不需要延迟
            time.sleep(delay)
    
    print("-" * 60)
    print(f"📊 完成！成功: {success_count}/{times}")

def main():
    print("=" * 60)
    print("🎯 visitor-badge 访客计数器工具")
    print("=" * 60)
    
    # 获取GitHub仓库信息
    user_input = input("\n请输入GitHub仓库 (username/repo 或 GitHub链接): ").strip()
    if not user_input:
        github_repo = "Ronchy2000/Xidian-LaTeX-Template-for-macOS"
        print(f"使用默认仓库: {github_repo}")
    else:
        github_repo = parse_github_repo(user_input)
        print(f"✅ 解析仓库: {github_repo}")
    
    print(f"\n📥 正在获取 page_id...")
    page_id = get_page_id(github_repo)
    print(f"✅ Page ID: {page_id}")
    
    while True:
        print("\n" + "=" * 60)
        print("请选择操作:")
        print("1. 查询当前访客数 (不增加计数)")
        print("2. 访问一次 (增加计数 +1)")
        print("3. 批量访问 (批量增加计数)")
        print("0. 退出")
        print("=" * 60)
        
        choice = input("请输入选项 [0-3]: ").strip()
        
        if choice == '1':
            print("\n🔍 查询模式...")
            query_visitor_count(page_id)
        
        elif choice == '2':
            print("\n🚀 访问一次...")
            count = visit_once(page_id)
            if count:
                print(f"✅ 成功！当前访客数: {count}")
        
        elif choice == '3':
            try:
                times = int(input("\n请输入访问次数: ").strip())
                if times <= 0:
                    print("❌ 次数必须大于0")
                    continue
                
                delay = input("请输入每次访问间隔(秒) [默认0.5]: ").strip()
                delay = float(delay) if delay else 0.5
                
                visit_multiple(page_id, times, delay)
            except ValueError:
                print("❌ 输入无效，请输入数字")
        
        elif choice == '0':
            print("\n👋 再见！")
            break
        
        else:
            print("\n❌ 无效选项，请重新选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已取消，再见！")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
