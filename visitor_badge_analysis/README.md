# Visitor Badge 计数工具

## 服务说明

**项目地址**: [visitor-badge](https://github.com/jwenjian/visitor-badge)

**服务域名**: `visitor-badge.laobi.icu`

## 使用方法

### 1. 交互式工具（推荐）

运行 `visitor_badge_tool.py` 进行交互式操作：

```bash
python3 visitor_badge_tool.py
```

#### 功能菜单：

```
1. 查询当前访客数 (不增加计数)
2. 访问一次 (增加计数 +1)
3. 批量访问 (批量增加计数)
0. 退出
```

#### 输入格式：

支持两种输入方式：
- GitHub仓库格式：`username/repo`
- GitHub链接：`https://github.com/username/repo`

#### 使用示例：

```bash
# 运行工具
$ python3 visitor_badge_tool.py

# 输入仓库（两种格式都可以）
请输入GitHub仓库 (username/repo 或 GitHub链接): Ronchy2000/Xidian-LaTeX-Template-for-macOS
# 或
请输入GitHub仓库 (username/repo 或 GitHub链接): https://github.com/Ronchy2000/Xidian-LaTeX-Template-for-macOS

# 选择操作
请输入选项 [0-3]: 1
📊 当前访客数: 172

# 批量增加
请输入选项 [0-3]: 3
请输入访问次数: 10
请输入每次访问间隔(秒) [默认0.5]: 0.5

🚀 开始批量访问，目标次数: 10
[1/10] ✅ 成功 - 当前访客数: 173
[2/10] ✅ 成功 - 当前访客数: 174
...
```

### 2. 分析脚本（学习用）

运行 `analyze_visitor_badge.py` 查看服务工作原理：

```bash
python3 analyze_visitor_badge.py
```

该脚本会：
- 分析GitHub页面结构
- 提取visitor-badge的page_id
- 测试查询和访问功能
- 检测防护机制

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
   - 使用 `query_only=true` 参数只查询不计数
   - 无身份验证
   - 无明显速率限制
   - 计数值嵌入在 SVG 响应中

### URL 示例

```
# 正常模式（会增加计数）
https://visitor-badge.laobi.icu/badge?page_id=Ronchy2000.Xidian-LaTeX-Template-for-macOS

# 查询模式（不增加计数）
https://visitor-badge.laobi.icu/badge?page_id=Ronchy2000.Xidian-LaTeX-Template-for-macOS&query_only=true
```

### 响应示例

返回 SVG 格式图片，内容包含访客计数：

```xml
<svg>
  ...
  <text>172</text>
  ...
</svg>
```

## 技术特点

- ✅ 无防护措施
- ✅ 响应速度快（~600ms）
- ✅ 100% 成功率
- ✅ 支持查询模式（不增加计数）
- ✅ 自动从README提取page_id

## 文件说明

- `visitor_badge_tool.py` - 交互式工具（实用）
- `analyze_visitor_badge.py` - 分析脚本（学习）
- `README.md` - 使用文档
- ✓ 支持查询模式（不增加计数）
- ✓ 仅需标准 HTTP 请求

## 使用方法

参考根目录的 `visitor_badge_attack.py` 脚本。
