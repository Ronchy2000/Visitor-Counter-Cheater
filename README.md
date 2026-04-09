# 🚀 访问量计数器刷新工具

[中文](./README.md) | [English](./README.en.md)

---

> 面向常见公开计数服务的访问量测试与刷新工具，既提供高效的 HTTP 请求方案，也提供适合普通网页的 Selenium 通用方案。

<div align="center">

[![visitors](https://visitor-badge.laobi.icu/badge?page_id=ronchy2000.Visitor-Counter-Cheater&left_color=gray&right_color=blue&style=for-the-badge)](https://github.com/Ronchy2000/Visitor-Counter-Cheater)

### 📊 在线演示

#### 🌐 [点击查看实时统计效果](https://visitor-counter-cheater.vercel.app/)

**演示网址：** `https://visitor-counter-cheater.vercel.app/`

</div>

---

## 🔎 先看这个：应该运行哪个脚本？

大多数用户并不是想先研究实现细节，而是想尽快判断“我这个页面该用哪个脚本”。下面这张表就是最直接的入口：

| 场景 | 直接入口 | 说明 |
|------|----------|------|
| GitHub README 上的 visitor-badge 徽章 | [visitor_badge_attack.py](./visitor_badge_attack.py) | 适合 GitHub 仓库 README 的访客徽章，默认就可以拿本项目测试 |
| 接入了不蒜子的博客、文档站、静态站 | [busuanzi_attack_efficient.py](./busuanzi_attack_efficient.py) | 直接模拟不蒜子的 JSONP 请求，速度快，配置最简单 |
| CSDN、普通博客文章页、需要执行前端 JS 的网页 | [selenium_all_website.py](./selenium_all_website.py) | 通用方案，直接用真实浏览器访问页面，适合“先跑起来再说” |
| 西电教师主页访问量 | [xidian_counter_attack.py](./xidian_counter_attack.py) | 针对西电教师主页访问量接口的专用脚本 |
| 西电教师主页点赞 | [xidian_like_attack.py](./xidian_like_attack.py) | 点赞接口专用脚本，存在 IP 限制 |

如果你只是第一次体验这个仓库，建议先运行 [visitor_badge_attack.py](./visitor_badge_attack.py)。它已经默认指向本仓库，最容易立即看到效果。

---

## 🌐 相关计数服务官网

如果你想先了解这些计数方案本身，或者准备把对应计数器接到自己的页面上，可以先看它们的官网：

- visitor-badge: [https://visitor-badge.laobi.icu/](https://visitor-badge.laobi.icu/)
- 不蒜子: [https://busuanzi.ibruce.info/](https://busuanzi.ibruce.info/)

---

## ⚡ 快速开始

### 方式一：直接测试本项目（最推荐）

```bash
git clone https://github.com/Ronchy2000/Visitor-Counter-Cheater.git
cd Visitor-Counter-Cheater
python3 visitor_badge_attack.py
```

运行后刷新本仓库 README，顶部徽章数字会增加。

### 方式二：测试你自己的目标页面

无论目标页面是什么，整体使用流程都很简单：

1. 先根据上面的表选脚本。
2. 打开脚本顶部的 `CONFIG`，把目标 URL 改成你的页面。
3. 运行脚本，观察页面数字变化或查看 `logs/` 下的 CSV 日志。

例如，你想测试一个 CSDN 文章页，就可以直接从通用 Selenium 脚本开始：

```python
CONFIG = {
    "URL": "https://blog.csdn.net/your_name/article/details/123456789",
    "MAX_VISITS": 20,
    "INTERVAL_MEAN": 8,
    "HEADLESS": True,
    "WAIT_AFTER_LOAD": 4.0,
}
```

然后执行：

```bash
python3 selenium_all_website.py
```

---

## 🧭 最常见的使用路径

### 1. 想刷 GitHub README 徽章

直接使用 [visitor_badge_attack.py](./visitor_badge_attack.py)。

```bash
python3 visitor_badge_attack.py
```

把脚本里的 `TARGET_URL` 改成目标 GitHub 仓库地址即可：

```python
CONFIG = {
    "TARGET_URL": "https://github.com/username/repository",
    "MAX_VISITS": 50,
    "INTERVAL_MEAN": 1.0,
}
```

### 2. 想刷接入不蒜子的个人博客或文档站

如果目标站点已经接入了不蒜子，最省事的做法就是直接使用 [busuanzi_attack_efficient.py](./busuanzi_attack_efficient.py)。

```python
CONFIG = {
    "URL": "https://your-blog.example.com/post/hello-world/",
    "MAX_VISITS": 100,
    "INTERVAL_MEAN": 1.0,
    "INTERVAL_MIN": 0.3,
}
```

```bash
python3 busuanzi_attack_efficient.py
```

这个脚本会自动把 `URL` 作为 `Referer` 发送，所以大多数情况下只需要改一个地址就够了。

### 3. 想测试 CSDN、博客文章页、普通网页访问

这类页面更适合优先使用 [selenium_all_website.py](./selenium_all_website.py)。

原因很直接：这类网站往往不会像 visitor-badge 或不蒜子那样暴露一个清晰的计数接口，但页面在真实浏览器中完成加载、执行 JavaScript、产生滚动或停留行为后，常常就会触发统计逻辑。Selenium 脚本正是为这种场景准备的。

适用例子：

- CSDN 文章页
- 个人博客文章页
- 活动落地页
- 文档站页面
- 任何“打开页面就可能触发计数”的普通网页

示例配置：

```python
CONFIG = {
    "URL": "https://blog.csdn.net/your_name/article/details/123456789",
    "MAX_VISITS": 20,
    "INTERVAL_MEAN": 8,
    "HEADLESS": True,
    "WAIT_AFTER_LOAD": 4.0,
}
```

```bash
python3 selenium_all_website.py
```

### 4. 想看更具体的使用示例

如果你想直接照着例子修改配置，可以继续看下面这些文档：

- [docs/USAGE_EXAMPLE.md](./docs/USAGE_EXAMPLE.md)
- [docs/visitor_badge_analysis.md](./docs/visitor_badge_analysis.md)
- [docs/xidian_analysis.md](./docs/xidian_analysis.md)
- [docs/XIDIAN_ANALYSIS_REPORT.md](./docs/XIDIAN_ANALYSIS_REPORT.md)

---

## 💡 技术原理

### HTTP 请求方式（推荐）

直接向计数服务后端发送请求。这种方式速度快、资源消耗低，适合已经分析清楚接口的服务。

**优势**：

- 速度快
- 无需浏览器依赖
- 资源占用低
- 适合批量测试

**限制**：

- 只适合服务端可直接请求的计数接口
- 遇到纯前端统计逻辑时不适用

### Selenium 浏览器模拟（通用）

使用真实浏览器访问页面、执行 JavaScript，并模拟滚动和停留行为，是覆盖范围最广的方案。

**优势**：

- 不需要先完全搞懂对方接口
- 适合 CSDN、博客、落地页、普通网页
- 支持前端 JS 统计逻辑
- 支持设备和 User-Agent 伪装

**限制**：

- 速度比 HTTP 方案慢
- 需要安装浏览器依赖
- 对资源占用更高

---

## 🎯 支持的脚本与场景

### 1. visitor-badge

**脚本**： [visitor_badge_attack.py](./visitor_badge_attack.py)

**目标**：GitHub README 上的访客徽章

**官网**： [https://visitor-badge.laobi.icu/](https://visitor-badge.laobi.icu/)

**特点**：

- 基于 SVG 图片计数
- 无需浏览器
- 性能约 `~600ms/次`
- 适合快速验证和演示

### 2. 不蒜子

**脚本**： [busuanzi_attack_efficient.py](./busuanzi_attack_efficient.py)

**目标**：接入了不蒜子的博客、静态站、文档站

**官网**： [https://busuanzi.ibruce.info/](https://busuanzi.ibruce.info/)

**特点**：

- 直接模拟 JSONP 请求
- 无需第三方依赖
- 性能约 `~1000ms/次`
- 适合博客访问量演示

### 3. 西安电子科技大学教师主页

**脚本**：

- 访问量： [xidian_counter_attack.py](./xidian_counter_attack.py)
- 点赞： [xidian_like_attack.py](./xidian_like_attack.py)

**说明**：

- 访问量脚本更稳定，性能约 `~35ms/次`
- 点赞脚本存在 IP 限制，更适合研究接口行为

### 4. 通用网页方案

**脚本**： [selenium_all_website.py](./selenium_all_website.py)

**适用场景**：

- CSDN 文章页
- 普通博客文章页
- 文档站、落地页
- 需要执行 JS 才能触发统计的页面
- 你还没来得及分析接口，但想先验证“访问是否会计数”

**依赖安装**：

```bash
pip install selenium webdriver-manager numpy
```

---

## 📚 文档入口

- 使用示例（中文）: [docs/USAGE_EXAMPLE.md](./docs/USAGE_EXAMPLE.md)
- Usage Examples (English): [docs/USAGE_EXAMPLE.en.md](./docs/USAGE_EXAMPLE.en.md)
- Visitor Badge 分析（中文）: [docs/visitor_badge_analysis.md](./docs/visitor_badge_analysis.md)
- 西电分析（中文）: [docs/xidian_analysis.md](./docs/xidian_analysis.md)
- 西电点赞分析报告（中文）: [docs/XIDIAN_ANALYSIS_REPORT.md](./docs/XIDIAN_ANALYSIS_REPORT.md)

---

## 📊 性能对比

| 方法 | 耗时 | 资源占用 | 适用范围 |
|------|------|----------|----------|
| HTTP 请求 | 35-1000ms | 极低 | 已知接口、服务端计数 |
| Selenium | 3000-8000ms | 高 | CSDN、博客、普通网页、前端 JS 统计 |

---

## 📁 项目结构

```text
.
├── README.md
├── README.en.md
├── docs/
│   ├── USAGE_EXAMPLE.md
│   ├── USAGE_EXAMPLE.en.md
│   ├── visitor_badge_analysis.md
│   ├── visitor_badge_analysis.en.md
│   ├── xidian_analysis.md
│   ├── xidian_analysis.en.md
│   ├── XIDIAN_ANALYSIS_REPORT.md
│   └── XIDIAN_ANALYSIS_REPORT.en.md
├── visitor_badge_attack.py
├── busuanzi_attack_efficient.py
├── xidian_counter_attack.py
├── xidian_like_attack.py
├── selenium_all_website.py
└── html/
```

---

## 📊 日志记录

所有脚本都会在 `logs/` 目录下生成 CSV 日志，方便你观察访问结果、响应时间和成功率。

---

## ⚠️ 注意事项

- 建议先小规模测试，再逐步提高访问次数
- 部分目标存在 IP 限制或频率限制
- 如果 HTTP 专用脚本无效，再切换到 Selenium 通用方案
- 请遵守目标网站条款与当地法律法规

代理池构建及使用方法：

- 自建代理 IP 池：[Dynamic-Proxy-Pool](https://github.com/Ronchy2000/Dynamic-Proxy-Pool)
- 购买代理 IP：[快代理](https://www.kuaidaili.com/login/?next=/cart2%3Ft%3Dtps_c%26period%3D0)

---

## 📄 免责声明

本工具仅供学习和技术研究使用，请勿用于任何违反网站服务条款或法律法规的行为。使用者需自行承担使用本工具产生的一切后果。

---

## 📜 License

MIT License
