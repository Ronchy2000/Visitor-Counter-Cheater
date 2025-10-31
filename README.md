# 🚀 访问量计数器刷新工具

> 支持多种计数服务的访问量提升工具 • 高效 HTTP 请求 • Selenium 浏览器模拟 • 多设备伪装

<div align="center">

[![visitors](https://visitor-badge.laobi.icu/badge?page_id=ronchy2000.Visitor-Counter-Cheater&left_color=gray&right_color=blue&style=for-the-badge)](https://github.com/Ronchy2000/Visitor-Counter-Cheater)

### 📊 在线演示

#### 🌐 [点击查看实时统计效果](https://visitor-counter-cheater.vercel.app/)

**演示网址：** `https://visitor-counter-cheater.vercel.app/`

</div>

---

## ⚡ 快速开始

### 方式一：测试本项目（推荐）

直接运行脚本，观察上方徽章数字变化：

```bash
# 克隆项目
git clone https://github.com/Ronchy2000/Visitor-Counter-Cheater.git
cd Visitor-Counter-Cheater

# 运行脚本（默认配置已指向本项目）
python3 visitor_badge_attack.py
```

**效果**: 刷新本页面，顶部徽章数字立即增加！

### 方式二：测试在线演示

使用不同的攻击脚本测试演示站点：

```bash
# visitor-badge 方式（修改配置指向演示站点）
python3 busuanzi_attack_efficient.py

# 或使用 Selenium 通用方式
python3 selenium_all_website.py
```

配置示例：
```python
CONFIG = {
    "TARGET_URL": "https://visitor-counter-cheater.vercel.app/",
    "MAX_VISITS": 50,
    # ... 其他配置
}
```

**效果**: 访问 [演示页面](https://visitor-counter-cheater.vercel.app/)，刷新后看到访问量增加！

---

## 💡 技术原理

### HTTP 请求方式（推荐）

直接发送 HTTP 请求到计数服务后端，**速度快、资源消耗低**，适用于大部分公开计数服务。

**优势**：
- 速度快（10-50倍于浏览器模拟）
- 无需浏览器依赖
- 资源占用极小
- 支持高并发

**限制**：
- 仅适用于服务端计数（如 visitor-badge）
- 不适用于纯前端 JS 统计（如不蒜子的某些部署）

### Selenium 浏览器模拟（通用）

使用真实浏览器访问页面，执行 JavaScript 统计代码，**兼容性最强**。

**优势**：
- 完全模拟真实用户行为
- 支持多种设备伪装
- 支持所有基于 JS 的统计服务
- 可绕过简单的反爬虫机制

**限制**：
- 速度较慢（需要完整加载页面）
- 需要安装浏览器驱动
- 资源占用较高

---

## 🎯 支持的计数服务

### 1. visitor-badge（推荐）

**服务**: GitHub README 徽章计数服务

**脚本**: `visitor_badge_attack.py`

**特点**:
- 基于 SVG 图片计数
- 无身份验证
- 无速率限制
- 性能：~600ms/次，100% 成功率
- 支持任意 GitHub 仓库 URL

**使用方法**:

```bash
python3 visitor_badge_attack.py
```

**配置说明**:

修改脚本中的 `TARGET_URL` 为目标 GitHub 仓库地址：

```python
CONFIG = {
    # 支持多种格式:
    # "https://github.com/username/repository"
    # "github.com/username/repository"
    # "username/repository"
    # "username.repository"
    "TARGET_URL": "https://github.com/Ronchy2000/Visitor-Counter-Cheater",
    # ... 其他配置
}
```

**测试效果**:

- 运行脚本后，访问目标仓库的 README
- 如果 README 中有 visitor-badge 徽章，数字会增加
- 本项目 README 顶部就有徽章，可直接测试

**详细说明**: 查看 `visitor_badge_analysis/README.md`

---

### 2. 不蒜子（busuanzi）

**服务**: 轻量级访客统计服务

**脚本**: `busuanzi_efficient.py`

**特点**:
- 基于 JSONP 回调
- 需要正确的 Referer 头
- 无明显限制
- 性能：~1000ms/次

```bash
python3 busuanzi_efficient.py
```

配置修改 `URL` 和 `REFERER` 为目标站点。

---

### 3. 西安电子科技大学教师主页

**目标**: 教师个人主页的访问量和点赞功能

**脚本**: 
- 访问量: `xidian_counter_attack.py`
- 点赞: `xidian_like_attack.py`

**特点**:
- 访问量：无限制，35ms/次
- 点赞：⚠️ IP 限制（24小时），需代理池

```bash
# 访问量攻击
python3 xidian_counter_attack.py

# 点赞攻击（注意 IP 限制）
python3 xidian_like_attack.py
```

**详细说明**: 查看 `xidian_analysis/README.md`

---

### 4. 通用方案（Selenium）

**脚本**: `selenium_all_website.py`

**适用场景**:
- 以上专用脚本都不适用时
- 需要执行复杂 JS 逻辑
- 需要模拟真实用户交互

**依赖安装**:
```bash
pip install selenium webdriver-manager numpy
```

**配置示例**:
```python
CONFIG = {
    "URL": "https://your-target-site.com/",
    "MAX_VISITS": 50,
    "INTERVAL_MEAN": 5,
    "HEADLESS": True,
}
```

**运行**:
```bash
python3 selenium_github.py
```

---

## 📚 使用建议

**选择攻击脚本的优先级**：

1. **优先使用专用 HTTP 脚本**：如果目标使用 visitor-badge、不蒜子等已知服务
2. **其次尝试分析接口**：使用浏览器开发者工具抓包，编写针对性脚本
3. **最后使用 Selenium**：当以上方法都不可行时的通用方案

**性能对比**（单次请求）：

| 方法 | 耗时 | 资源占用 | 适用范围 |
|------|------|----------|----------|
| HTTP 请求 | 35-1000ms | 极低 | 服务端计数 |
| Selenium | 3000-8000ms | 高 | 所有类型 |

---

## 📁 项目结构

```
.
├── README.md                       # 本文件
├── visitor_badge_attack.py         # visitor-badge 攻击脚本
├── busuanzi_efficient.py           # 不蒜子攻击脚本
├── xidian_counter_attack.py        # 西电访问量攻击
├── xidian_like_attack.py           # 西电点赞攻击
├── selenium_github.py              # Selenium 通用脚本
├── logs/                           # 日志目录
├── html/                           # 演示页面
├── visitor_badge_analysis/         # visitor-badge 分析资料
└── xidian_analysis/                # 西电系统分析资料
```

---

## 📊 日志记录

所有脚本都会在 `logs/` 目录生成 CSV 日志文件，记录每次访问的详细信息：

- 时间戳
- 访问序号
- 目标 URL
- User-Agent
- 状态（成功/失败）
- 响应时间

---

## ⚠️ 注意事项

- 合理控制访问频率，避免对目标服务造成压力
- 部分服务可能有 IP 限制，需要使用代理池
- 使用前建议先小规模测试
- 遵守目标网站的使用条款

代理池构建及使用方法：
- 自建代理ip池：[ynamic-Proxy-Pool](https://github.com/Ronchy2000/Dynamic-Proxy-Pool)
- 购买代理ip：[https://www.kuaidaili.com/login/?next=/cart2%3Ft%3Dtps_c%26period%3D0](https://www.kuaidaili.com/login/?next=/cart2%3Ft%3Dtps_c%26period%3D0)

---

## 📄 免责声明

本工具仅供学习和技术研究使用，请勿用于任何违反网站服务条款或法律法规的行为。使用者需自行承担使用本工具产生的一切后果。

---

## 📜 License

MIT License




