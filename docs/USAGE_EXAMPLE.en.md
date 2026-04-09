# Usage Examples

[English](./USAGE_EXAMPLE.en.md) | [中文](./USAGE_EXAMPLE.md)

---

## Pick the Script First

If you want to get started quickly, use this simple rule first:

1. GitHub README badge: [`visitor_badge_attack.py`](../visitor_badge_attack.py)
2. Busuanzi-powered blog/docs site: [`busuanzi_attack_efficient.py`](../busuanzi_attack_efficient.py)
3. CSDN, blogs, JS-driven pages: [`selenium_all_website.py`](../selenium_all_website.py)
4. Xidian teacher pages: [`xidian_counter_attack.py`](../xidian_counter_attack.py) or [`xidian_like_attack.py`](../xidian_like_attack.py)

---

## Counter Service Websites

If you are also looking for the counter services themselves, these pages are useful references:

- visitor-badge: [https://visitor-badge.laobi.icu/](https://visitor-badge.laobi.icu/)
- Busuanzi: [https://busuanzi.ibruce.info/](https://busuanzi.ibruce.info/)

---

## `visitor-badge` Examples

### Example 1: test this repository

```bash
python3 visitor_badge_attack.py
```

Then open `https://github.com/Ronchy2000/Visitor-Counter-Cheater` and check the badge count in the README.

### Example 2: another GitHub repository

```python
CONFIG = {
    "TARGET_URL": "https://github.com/username/repository",
    "MAX_VISITS": 50,
    "INTERVAL_MEAN": 1.0,
    "INTERVAL_MIN": 0.3,
}
```

Also supported:

```python
"TARGET_URL": "username/repository"
# or
"TARGET_URL": "username.repository"
```

### Example 3: quick verification

```python
CONFIG = {
    "TARGET_URL": "https://github.com/Ronchy2000/Visitor-Counter-Cheater",
    "MAX_VISITS": 5,
    "INTERVAL_MEAN": 0.5,
    "INTERVAL_MIN": 0.3,
}
```

---

## Busuanzi Examples

### Example 1: personal blog post

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

Notes:

- Usually only `URL` needs to be changed
- The script automatically uses that page as the `Referer`
- If the page really uses Busuanzi, you should see `page_pv` / `site_pv` updates

### Example 2: documentation or static site page

```python
CONFIG = {
    "URL": "https://docs.example.com/guide/start.html",
    "MAX_VISITS": 50,
    "INTERVAL_MEAN": 1.2,
    "INTERVAL_MIN": 0.5,
}
```

---

## Generic Selenium Examples

### Example 1: CSDN article page

Use Selenium when your target is a normal page visit and there is no clear public counter API to call directly.

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

Why this works well here:

- The page needs a full browser load
- Counter logic may depend on front-end JavaScript
- The script simulates loading, waiting, and scrolling

### Example 2: regular blog post

```python
CONFIG = {
    "URL": "https://your-blog.example.com/posts/how-to-build-something/",
    "MAX_VISITS": 20,
    "INTERVAL_MEAN": 6,
    "HEADLESS": True,
    "WAIT_AFTER_LOAD": 3.5,
}
```

### Example 3: campaign or landing page

```python
CONFIG = {
    "URL": "https://example.com/campaign/spring-launch",
    "MAX_VISITS": 30,
    "INTERVAL_MEAN": 10,
    "HEADLESS": True,
    "WAIT_AFTER_LOAD": 5.0,
}
```

Increase `WAIT_AFTER_LOAD` if the page is slow or if analytics fires late.

---

## Xidian Teacher Page Examples

### Counter

```python
CONFIG = {
    "TARGET_PATH": "/TEACHERNAME/zh_CN/index.htm",
    "MAX_VISITS": 100,
}
```

Run:

```bash
python3 xidian_counter_attack.py
```

### Like

```bash
python3 xidian_like_attack.py
```

Note: the like endpoint has IP limits, so it is more useful for analysis and verification than for sustained testing.

---

## Common Workflow

### I just want to verify that the repo works

```bash
python3 visitor_badge_attack.py
```

### I already have a target URL

1. Open the matching script
2. Edit the `CONFIG` block at the top
3. Run the script
4. Check the page or the CSV files in `logs/`

---

## Performance Reference

| Script | Scenario | Speed | Success Rate | Limitation |
|------|------|------|--------|------|
| `visitor_badge_attack.py` | GitHub README badge | ~600ms | 100% | only for `visitor-badge` |
| `busuanzi_attack_efficient.py` | Busuanzi blog/docs site | ~1000ms | 100% | only for Busuanzi |
| `xidian_counter_attack.py` | Xidian counter | ~35ms | 100% | target-specific |
| `xidian_like_attack.py` | Xidian like | ~40ms | first request succeeds | IP limit |
| `selenium_all_website.py` | CSDN/blog/general pages | ~5000ms | 95%+ | slower, browser required |
