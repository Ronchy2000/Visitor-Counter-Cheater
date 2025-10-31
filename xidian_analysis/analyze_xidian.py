#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析西电教师主页的访问量计数器
目标：https://faculty.xidian.edu.cn/DANIEL/zh_CN/index.htm
"""
import urllib.request
import urllib.parse
import re
import json

target_url = "https://faculty.xidian.edu.cn/DANIEL/zh_CN/index.htm"

print("=" * 80)
print("🔍 步骤1: 获取页面 HTML")
print("=" * 80)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

try:
    req = urllib.request.Request(target_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
    
    print(f"✅ 成功获取页面 (大小: {len(html)} 字符)")
    
    # 保存 HTML 到文件
    with open("xidian_page.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("💾 已保存到 xidian_page.html")
    
    print("\n" + "=" * 80)
    print("🔍 步骤2: 查找访问量计数器")
    print("=" * 80)
    
    # 查找包含访问量的文本
    patterns = [
        r'访问量[：:]\s*(\d+)',
        r'访问[：:](\d+)',
        r'visit[s]?[：:]\s*(\d+)',
        r'(\d{7,})',  # 7位以上的数字
        r'<.*?>\s*0*(\d+)\s*次',
        r'pageviews?[：:]\s*(\d+)',
        r'pv[：:]\s*(\d+)',
    ]
    
    found_counters = []
    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            print(f"✅ 模式 '{pattern}' 找到: {matches}")
            found_counters.extend(matches)
    
    print("\n" + "=" * 80)
    print("🔍 步骤3: 查找 JavaScript 文件")
    print("=" * 80)
    
    # 查找所有 script 标签
    script_patterns = [
        r'<script[^>]*src=["\']([^"\']+)["\']',
        r'<script[^>]*>(.*?)</script>',
    ]
    
    js_files = []
    inline_scripts = []
    
    # 外部 JS 文件
    for match in re.finditer(r'<script[^>]*src=["\']([^"\']+)["\']', html, re.IGNORECASE):
        js_url = match.group(1)
        if not js_url.startswith('http'):
            if js_url.startswith('//'):
                js_url = 'https:' + js_url
            elif js_url.startswith('/'):
                js_url = 'https://faculty.xidian.edu.cn' + js_url
            else:
                js_url = 'https://faculty.xidian.edu.cn/DANIEL/zh_CN/' + js_url
        js_files.append(js_url)
        print(f"📄 外部JS: {js_url}")
    
    # 内联 JS
    for match in re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE):
        script_content = match.group(1).strip()
        if script_content and len(script_content) > 50:  # 忽略很短的脚本
            inline_scripts.append(script_content)
    
    print(f"\n找到 {len(js_files)} 个外部JS文件")
    print(f"找到 {len(inline_scripts)} 个内联JS脚本")
    
    print("\n" + "=" * 80)
    print("🔍 步骤4: 分析内联JS中的计数器逻辑")
    print("=" * 80)
    
    counter_keywords = ['visit', 'counter', 'count', 'pv', 'pageview', '访问', '计数']
    
    for i, script in enumerate(inline_scripts[:5]):  # 只看前5个
        for keyword in counter_keywords:
            if keyword.lower() in script.lower():
                print(f"\n📍 内联脚本 #{i+1} 包含关键词 '{keyword}':")
                print("-" * 80)
                print(script[:500])  # 只显示前500字符
                print("-" * 80)
                break
    
    print("\n" + "=" * 80)
    print("🔍 步骤5: 下载并分析外部JS文件")
    print("=" * 80)
    
    for js_url in js_files[:10]:  # 只分析前10个
        try:
            print(f"\n📥 下载: {js_url}")
            req = urllib.request.Request(js_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                js_content = response.read().decode('utf-8', errors='ignore')
            
            # 检查是否包含计数器相关代码
            for keyword in counter_keywords:
                if keyword.lower() in js_content.lower():
                    print(f"  ✅ 包含关键词: {keyword}")
                    
                    # 查找 AJAX 请求
                    ajax_patterns = [
                        r'\.ajax\({([^}]+)}\)',
                        r'fetch\(["\']([^"\']+)["\']',
                        r'XMLHttpRequest.*?open\(["\']([^"\']+)["\']',
                        r'post\(["\']([^"\']+)["\']',
                        r'get\(["\']([^"\']+)["\']',
                    ]
                    
                    for pattern in ajax_patterns:
                        matches = re.findall(pattern, js_content, re.IGNORECASE)
                        if matches:
                            print(f"    🔗 发现请求: {matches}")
                    
                    # 保存包含计数器的JS文件
                    filename = f"counter_js_{js_url.split('/')[-1]}"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(js_content)
                    print(f"    💾 已保存到: {filename}")
                    break
                    
        except Exception as e:
            print(f"  ❌ 下载失败: {e}")
    
    print("\n" + "=" * 80)
    print("🔍 步骤6: 查找页面中的数字显示元素")
    print("=" * 80)
    
    # 查找可能显示访问量的元素
    counter_element_patterns = [
        r'<span[^>]*id=["\']([^"\']*count[^"\']*)["\']',
        r'<div[^>]*id=["\']([^"\']*visit[^"\']*)["\']',
        r'<span[^>]*class=["\']([^"\']*count[^"\']*)["\']',
    ]
    
    for pattern in counter_element_patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            print(f"✅ 找到计数器元素: {matches}")
    
    print("\n" + "=" * 80)
    print("📊 分析总结")
    print("=" * 80)
    print(f"页面大小: {len(html)} 字符")
    print(f"找到的可能计数值: {set(found_counters)}")
    print(f"外部JS文件数: {len(js_files)}")
    print(f"内联JS脚本数: {len(inline_scripts)}")
    
    print("\n💡 下一步：")
    print("1. 检查保存的 xidian_page.html 文件")
    print("2. 检查保存的 counter_js_*.js 文件")
    print("3. 使用浏览器开发者工具监控网络请求")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
