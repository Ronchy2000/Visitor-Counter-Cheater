#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visitor-badge 访客计数器分析工具（学习用）

目标: https://github.com/Ronchy2000/Raspi-ImmortalWrt
服务: https://visitor-badge.laobi.icu
当前访客数: 3339

分析服务工作原理
"""
import urllib.request
import urllib.parse
import json
import re

# GitHub项目信息
GITHUB_REPO = "Ronchy2000/Xidian-LaTeX-Template-for-macOS"
GITHUB_URL = f"https://github.com/{GITHUB_REPO}"

print("🔍 visitor-badge 服务分析")
print("=" * 80)
print(f"目标项目: {GITHUB_REPO}")
print()

# 步骤1: 获取GitHub README页面
print("📥 步骤1: 获取 GitHub README 页面...")
try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    req = urllib.request.Request(GITHUB_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
    
    print(f"✅ 成功获取页面 (大小: {len(html)} 字符)")
    
    # 查找visitor-badge的URL
    print("\n📍 步骤2: 查找 visitor-badge URL...")
    
    # 匹配visitor-badge链接
    patterns = [
        r'visitor-badge\.laobi\.icu/badge\?page_id=([^"\'&\\]+)',
        r'https?://visitor-badge\.laobi\.icu/badge\?[^"\'>\s]+',
    ]
    
    found_urls = []
    page_ids = []
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            if 'page_id=' in pattern:
                page_ids.extend(matches)
            else:
                found_urls.extend(matches)
    
    if page_ids:
        print(f"✅ 找到 page_id: {page_ids}")
        page_id = page_ids[0].rstrip('\\').rstrip()
    else:
        print("⚠️  未在HTML中找到page_id，尝试常见格式...")
        # 常见格式：用户名.项目名
        page_id = GITHUB_REPO.replace('/', '.')
        print(f"   猜测的 page_id: {page_id}")
    
    if found_urls:
        print(f"✅ 找到完整URL: {found_urls[0]}")
    
    # 步骤3: 构造badge URL并测试
    print(f"\n🧪 步骤3: 测试 visitor-badge 服务...")
    
    # 测试1: 只查询不增加计数
    badge_url_query = f"https://visitor-badge.laobi.icu/badge?page_id={page_id}&query_only=true"
    print(f"\n[测试1] 查询模式 (query_only=true)")
    print(f"URL: {badge_url_query}")
    
    try:
        req = urllib.request.Request(badge_url_query, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content_type = response.headers.get('Content-Type')
            data = response.read()
            
            print(f"✅ 响应成功")
            print(f"   Content-Type: {content_type}")
            print(f"   大小: {len(data)} 字节")
            
            # 如果是SVG，尝试提取访客数
            if 'svg' in content_type or data.startswith(b'<svg'):
                svg_text = data.decode('utf-8')
                # 从SVG中提取数字
                numbers = re.findall(r'>(\d+)<', svg_text)
                if numbers:
                    print(f"   📊 当前访客数: {numbers[-1]}")
    
    except Exception as e:
        print(f"❌ 查询失败: {e}")
    
    # 测试2: 正常访问（会增加计数）
    badge_url_normal = f"https://visitor-badge.laobi.icu/badge?page_id={page_id}"
    print(f"\n[测试2] 正常模式 (会增加计数)")
    print(f"URL: {badge_url_normal}")
    
    try:
        req = urllib.request.Request(badge_url_normal, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            
            print(f"✅ 响应成功")
            
            # 提取访客数
            if data.startswith(b'<svg'):
                svg_text = data.decode('utf-8')
                numbers = re.findall(r'>(\d+)<', svg_text)
                if numbers:
                    print(f"   📊 访问后的访客数: {numbers[-1]}")
    
    except Exception as e:
        print(f"❌ 访问失败: {e}")
    
    # 步骤4: 分析防护机制
    print(f"\n🔒 步骤4: 测试防护机制...")
    print("尝试连续访问多次...")
    
    success_count = 0
    for i in range(5):
        try:
            req = urllib.request.Request(badge_url_normal, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
                if data.startswith(b'<svg'):
                    svg_text = data.decode('utf-8')
                    numbers = re.findall(r'>(\d+)<', svg_text)
                    if numbers:
                        success_count += 1
                        print(f"  [{i+1}] ✅ 成功 - 当前访客数: {numbers[-1]}")
        except Exception as e:
            print(f"  [{i+1}] ❌ 失败: {e}")
    
    print(f"\n📊 测试结果: {success_count}/5 成功")
    
    # 总结
    print(f"\n" + "=" * 80)
    print("📋 分析总结")
    print("=" * 80)
    print(f"Page ID: {page_id}")
    print(f"Badge URL: {badge_url_normal}")
    print(f"查询URL (不计数): {badge_url_query}")
    print()
    print("💡 关键发现:")
    print("1. 每次请求badge URL都会增加计数")
    print("2. 返回的是SVG图片，包含访客数")
    print("3. query_only=true 参数可以只查询不增加")
    print()
    print("🎯 攻击策略:")
    print("- 直接循环请求badge URL即可增加计数")
    print("- 需要测试是否有IP限制或频率限制")
    print("- 如果有限制，可能需要代理池")
    print()
    print("💻 实用工具:")
    print("- 使用 visitor_badge_tool.py 进行交互式操作")

except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
