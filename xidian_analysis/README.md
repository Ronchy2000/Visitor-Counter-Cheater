# 西安电子科技大学教师主页计数分析

## 目标网站

**示例页面**: https://faculty.xidian.edu.cn/DANDAN1/zh_CN/index.htm

## 计数系统

该网站包含两种计数功能：

### 1. 访问量计数器

- **接口**: `/system/resource/tsites/click.jsp`
- **方法**: GET 请求
- **参数**:
  - `lc`: 教师主页路径
  - `hosts`: 主机名
  - `ac`: 操作类型（updateVisit）
  - `os`: 操作系统
  - `bs`: 浏览器类型
  - `vp`: 视口大小（可选）

- **防护程度**: 无
- **响应速度**: ~35ms
- **成功率**: 100%

### 2. 点赞功能

- **接口**: `/system/resource/tsites/praise.jsp`
- **方法**: POST 请求
- **参数**:
  - `uid`: 教师 ID
  - `homepageid`: 主页 ID
  - `ac`: 操作类型（updatePraise）

- **防护措施**: IP 地址限制
- **限制周期**: 约 24 小时
- **绕过难度**: 需要代理池

## 攻击特点

### 访问量攻击
- ✓ 无任何限制
- ✓ 响应极快
- ✓ 参数简单

### 点赞攻击
- ✗ IP 级别限制
- ✓ Cookie 无关联
- ⚠ 需要代理池突破

## 使用方法

- 访问量攻击: 参考根目录的 `xidian_counter_attack.py`
- 点赞攻击: 参考根目录的 `xidian_like_attack.py`

## 技术细节

本目录包含该系统的完整 JavaScript 逆向分析文件，包括：
- 访问统计核心代码
- 点赞系统实现
- 请求参数构造逻辑
