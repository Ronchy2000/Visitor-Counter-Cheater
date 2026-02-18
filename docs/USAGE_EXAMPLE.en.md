# Usage Examples

[English](./USAGE_EXAMPLE.en.md) | [中文](./USAGE_EXAMPLE.md)

---

## `visitor-badge` attack script

### Example 1: test this repository

```bash
# Default config already points to this repo
python3 visitor_badge_attack.py
```

After running, open https://github.com/Ronchy2000/Visitor-Counter-Cheater and check the badge number in README.

### Example 2: test another GitHub repository

Edit config in `visitor_badge_attack.py`:

```python
CONFIG = {
    # Supported formats
    "TARGET_URL": "https://github.com/username/repository",
    # or
    # "TARGET_URL": "username/repository",
    # or
    # "TARGET_URL": "username.repository",

    "MAX_VISITS": 50,
    "INTERVAL_MEAN": 1.0,
}
```

### Example 3: quick test (5 visits)

```python
CONFIG = {
    "TARGET_URL": "https://github.com/Ronchy2000/Visitor-Counter-Cheater",
    "MAX_VISITS": 5,
    "INTERVAL_MEAN": 0.5,
}
```

---

## Other script examples

### Busuanzi attack

```python
# Edit busuanzi_attack_efficient.py
CONFIG = {
    "URL": "https://your-website.com/",
    "REFERER": "https://your-website.com/",
    "MAX_VISITS": 100,
}
```

### Xidian teacher page

```python
# xidian_counter_attack.py
CONFIG = {
    "TARGET_PATH": "/TEACHERNAME/zh_CN/index.htm",
    "MAX_VISITS": 100,
}
```

### Generic Selenium solution

```python
# selenium_all_website.py
CONFIG = {
    "URL": "https://any-website.com/",
    "MAX_VISITS": 20,
    "HEADLESS": True,
}
```

---

## Performance benchmark

| Script | Target | Speed | Success Rate | Limitation |
|------|------|------|--------|------|
| visitor_badge_attack.py | this repo | ~600ms | 100% | none |
| busuanzi_attack_efficient.py | busuanzi | ~1000ms | 100% | none |
| xidian_counter_attack.py | xidian counter | ~35ms | 100% | none |
| xidian_like_attack.py | xidian like | ~40ms | first request succeeds | IP limit |
| selenium_all_website.py | generic | ~5000ms | 95%+ | anti-bot checks |
