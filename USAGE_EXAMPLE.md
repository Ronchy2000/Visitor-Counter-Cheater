# 使用示例

## visitor-badge 攻击脚本

### 示例 1：测试本项目

```bash
# 默认配置已指向本项目
python3 visitor_badge_attack.py
```

运行后访问 https://github.com/Ronchy2000/Visitor-Counter-Cheater，查看 README 顶部徽章数字变化。

### 示例 2：测试其他 GitHub 仓库

修改 `visitor_badge_attack.py` 中的配置：

```python
CONFIG = {
    # 支持多种格式
    "TARGET_URL": "https://github.com/username/repository",
    # 或
    # "TARGET_URL": "username/repository",
    # 或
    # "TARGET_URL": "username.repository",
    
    "MAX_VISITS": 50,      # 访问50次
    "INTERVAL_MEAN": 1.0,  # 平均1秒间隔
}
```

### 示例 3：快速测试（5次访问）

```python
CONFIG = {
    "TARGET_URL": "https://github.com/Ronchy2000/Visitor-Counter-Cheater",
    "MAX_VISITS": 5,       # 只测试5次
    "INTERVAL_MEAN": 0.5,  # 快速模式
}
```

---

## 其他脚本示例

### 不蒜子攻击

```python
# 编辑 busuanzi_efficient.py
CONFIG = {
    "URL": "https://your-website.com/",
    "REFERER": "https://your-website.com/",
    "MAX_VISITS": 100,
}
```

### 西电教师主页

```python
# xidian_counter_attack.py
CONFIG = {
    "TARGET_PATH": "/TEACHERNAME/zh_CN/index.htm",
    "MAX_VISITS": 100,
}
```

### Selenium 通用方案

```python
# selenium_all_website.py
CONFIG = {
    "URL": "https://any-website.com/",
    "MAX_VISITS": 20,
    "HEADLESS": True,  # 后台运行
}
```

---

## 性能测试结果

| 脚本 | 目标 | 速度 | 成功率 | 限制 |
|------|------|------|--------|------|
| visitor_badge_attack.py | 本项目 | ~600ms | 100% | 无 |
| busuanzi_efficient.py | 不蒜子 | ~1000ms | 100% | 无 |
| xidian_counter_attack.py | 西电访问量 | ~35ms | 100% | 无 |
| xidian_like_attack.py | 西电点赞 | ~40ms | 第1次成功 | IP限制 |
| selenium_all_website.py | 通用 | ~5000ms | 95%+ | 反爬虫检测 |
