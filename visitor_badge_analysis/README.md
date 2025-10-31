# Visitor Badge 计数分析

## 服务说明

**项目地址**: [visitor-badge](https://github.com/jwenjian/visitor-badge)

**服务域名**: `visitor-badge.laobi.icu`

## 计数原理

visitor-badge 是一个基于 SVG 的访客计数服务，主要用于 GitHub README 页面展示访客数量。

### 工作机制

1. **请求方式**: GET 请求返回 SVG 图片
2. **参数格式**: 
   - `page_id`: 页面标识符（如 `username.repository`）
   - `style`: 徽章样式（如 `flat`, `for-the-badge`）
   - `color`: 徽章颜色（十六进制）
   - `query_only`: 是否仅查询（不增加计数）

3. **计数机制**:
   - 每次正常请求自动 +1
   - 无身份验证
   - 无明显速率限制
   - 计数值嵌入在 SVG 响应中

### URL 示例

```
https://visitor-badge.laobi.icu/badge?page_id=ronchy2000.Raspi-ImmortalWrt&style=for-the-badge&color=00d4ff
```

### 响应示例

返回 SVG 格式图片，内容包含访客计数：

```xml
<svg>
  ...
  <text>3455</text>
  ...
</svg>
```

## 攻击特点

- ✓ 无防护措施
- ✓ 响应速度快（~600ms）
- ✓ 100% 成功率
- ✓ 支持查询模式（不增加计数）
- ✓ 仅需标准 HTTP 请求

## 使用方法

参考根目录的 `visitor_badge_attack.py` 脚本。
