#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度分析西电点赞接口的防护机制

目标：找出为什么第一次成功，后面都失败
"""
import urllib.request
import urllib.parse
import http.cookiejar
import json
import time

def test_like_with_details():
    """
    测试点赞请求并显示详细信息
    """
    # 创建Cookie管理器
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    
    praise_url = "https://faculty.xidian.edu.cn/system/resource/tsites/praise.jsp"
    
    params = {
        "uid": "6799",
        "homepageid": "24515",
        "apptype": "teacher",
        "contentid": "0",
        "pdtype": "0",
        "ac": "updatePraise"
    }
    
    data = urllib.parse.urlencode(params).encode('utf-8')
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://faculty.xidian.edu.cn/DANIEL/zh_CN/index.htm",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    print("🧪 测试点赞请求")
    print("=" * 70)
    
    for i in range(5):
        print(f"\n第 {i+1} 次尝试:")
        
        try:
            req = urllib.request.Request(praise_url, data=data, headers=headers)
            response = opener.open(req, timeout=10)
            
            # 查看响应头
            print(f"  响应头:")
            for key, value in response.headers.items():
                print(f"    {key}: {value}")
            
            # 查看响应内容
            response_data = response.read().decode('utf-8')
            print(f"  响应体: {response_data}")
            
            result = json.loads(response_data)
            print(f"  解析结果: {result}")
            
            # 查看Cookie
            print(f"  Cookie:")
            for cookie in cookie_jar:
                print(f"    {cookie.name} = {cookie.value}")
            
        except Exception as e:
            print(f"  错误: {e}")
        
        if i < 4:
            time.sleep(2)

def test_get_praise():
    """
    测试获取点赞数
    """
    praise_url = "https://faculty.xidian.edu.cn/system/resource/tsites/praise.jsp"
    
    params = {
        "uid": "6799",
        "homepageid": "24515",
        "apptype": "teacher",
        "contentid": "0",
        "pdtype": "0",
        "basenum": "0",
        "ac": "getPraise"
    }
    
    data = urllib.parse.urlencode(params).encode('utf-8')
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    
    print("\n\n🔍 测试获取点赞数")
    print("=" * 70)
    
    try:
        req = urllib.request.Request(praise_url, data=data, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            response_data = response.read().decode('utf-8')
            print(f"响应: {response_data}")
            
            result = json.loads(response_data)
            print(f"当前点赞数: {result.get('praise')}")
            
    except Exception as e:
        print(f"错误: {e}")

def test_ip_based_limit():
    """
    测试是否基于 IP 限制
    """
    print("\n\n🌐 测试 IP 限制")
    print("=" * 70)
    print("分析：如果服务器基于 IP 限制，那么：")
    print("1. 清空Cookie也无法绕过")
    print("2. 需要等待24小时或更换IP")
    print("3. 可能需要使用代理池")
    
    print("\n尝试使用完全不同的Session...")
    test_like_with_details()

if __name__ == "__main__":
    test_get_praise()
    test_ip_based_limit()
