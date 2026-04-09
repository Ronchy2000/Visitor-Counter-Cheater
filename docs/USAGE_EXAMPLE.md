# 使用示例

[中文](./USAGE_EXAMPLE.md) | [English](./USAGE_EXAMPLE.en.md)

---

## 先选脚本，再改配置

如果你只想快速上手，建议先按下面这个顺序判断目标属于哪一类：

1. GitHub README 徽章：用 [`visitor_badge_attack.py`](../visitor_badge_attack.py)
2. 接入了不蒜子的博客或文档站：用 [`busuanzi_attack_efficient.py`](../busuanzi_attack_efficient.py)
3. CSDN、普通博客文章页、需要执行 JS 的网页：用 [`selenium_all_website.py`](../selenium_all_website.py)
4. 西电教师主页：用 [`xidian_counter_attack.py`](../xidian_counter_attack.py) 或 [`xidian_like_attack.py`](../xidian_like_attack.py)

---

## 相关服务官网

如果你正在寻找这些计数器本身的接入方式，也可以先看对应官网：

- visitor-badge: [https://visitor-badge.laobi.icu/](https://visitor-badge.laobi.icu/)
- 不蒜子: [https://busuanzi.ibruce.info/](https://busuanzi.ibruce.info/)

---

## visitor-badge 示例

### 示例 1：直接测试本项目

```bash
# 默认配置已指向本项目
python3 visitor_badge_attack.py
```

运行后访问 `https://github.com/Ronchy2000/Visitor-Counter-Cheater`，查看 README 顶部徽章数字变化。

### 示例 2：测试其他 GitHub 仓库

修改 `visitor_badge_attack.py` 中的配置：

```python
CONFIG = {
    "TARGET_URL": "https://github.com/username/repository",
    "MAX_VISITS": 50,
    "INTERVAL_MEAN": 1.0,
    "INTERVAL_MIN": 0.3,
}
```

`TARGET_URL` 也支持以下写法：

```python
"TARGET_URL": "username/repository"
# 或
"TARGET_URL": "username.repository"
```

### 示例 3：快速验证模式

```python
CONFIG = {
    "TARGET_URL": "https://github.com/Ronchy2000/Visitor-Counter-Cheater",
    "MAX_VISITS": 5,
    "INTERVAL_MEAN": 0.5,
    "INTERVAL_MIN": 0.3,
}
```

---

## 不蒜子示例

### 示例 1：个人博客文章页

这一类示例适合已经接入了不蒜子的博客、文档站或静态站。

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

说明：

- 只需要改 `URL`
- 脚本会自动把该地址作为 `Referer`
- 如果页面确实接入了不蒜子，通常能直接看到 `page_pv` / `site_pv` 变化

### 示例 2：文档站或静态站页面

```python
CONFIG = {
    "URL": "https://docs.example.com/guide/start.html",
    "MAX_VISITS": 50,
    "INTERVAL_MEAN": 1.2,
    "INTERVAL_MIN": 0.5,
}
```

---

## Selenium 通用示例

### 示例 1：CSDN 文章页

如果你的目标不是一个已经分析清楚的计数接口，而是一个普通网页访问行为，那么优先用 Selenium 会更稳妥。

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

适用原因：

- CSDN 这类页面通常需要浏览器完整加载
- 页面统计逻辑可能依赖前端 JS
- 脚本会模拟打开页面、等待加载、随机滚动

### 示例 2：普通博客文章页

```python
CONFIG = {
    "URL": "https://your-blog.example.com/posts/how-to-build-something/",
    "MAX_VISITS": 20,
    "INTERVAL_MEAN": 6,
    "HEADLESS": True,
    "WAIT_AFTER_LOAD": 3.5,
}
```

### 示例 3：活动页或落地页

```python
CONFIG = {
    "URL": "https://example.com/campaign/spring-launch",
    "MAX_VISITS": 30,
    "INTERVAL_MEAN": 10,
    "HEADLESS": True,
    "WAIT_AFTER_LOAD": 5.0,
}
```

如果页面加载慢、统计触发晚，可以适当调大 `WAIT_AFTER_LOAD`。

---

## 西电教师主页示例

### 访问量

```python
CONFIG = {
    "TARGET_PATH": "/TEACHERNAME/zh_CN/index.htm",
    "MAX_VISITS": 100,
}
```

运行：

```bash
python3 xidian_counter_attack.py
```

### 点赞

```bash
python3 xidian_like_attack.py
```

说明：点赞接口存在 IP 限制，更适合用于接口分析和行为验证。

---

## 常见操作流程

### 我只想先验证脚本能不能跑

```bash
python3 visitor_badge_attack.py
```

### 我已经有目标网址，想直接试

1. 打开对应脚本
2. 修改顶部 `CONFIG`
3. 运行脚本
4. 查看页面数字变化或 `logs/` 下的 CSV 文件

---

## 性能参考

| 脚本 | 场景 | 速度 | 成功率 | 限制 |
|------|------|------|--------|------|
| `visitor_badge_attack.py` | GitHub README 徽章 | ~600ms | 100% | 仅适合 visitor-badge |
| `busuanzi_attack_efficient.py` | 不蒜子博客/文档站 | ~1000ms | 100% | 仅适合不蒜子 |
| `xidian_counter_attack.py` | 西电访问量 | ~35ms | 100% | 目标专用 |
| `xidian_like_attack.py` | 西电点赞 | ~40ms | 首次成功 | IP 限制 |
| `selenium_all_website.py` | CSDN/博客/普通网页 | ~5000ms | 95%+ | 速度慢，依赖浏览器 |
