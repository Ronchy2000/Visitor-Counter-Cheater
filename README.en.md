# 🚀 Visitor Counter Booster Toolkit

[English](./README.en.md) | [中文](./README.md)

---

> A practical toolkit for testing public counter services, with both fast HTTP request flows and a generic Selenium workflow for regular web pages.

<div align="center">

[![visitors](https://visitor-badge.laobi.icu/badge?page_id=ronchy2000.Visitor-Counter-Cheater&left_color=gray&right_color=blue&style=for-the-badge)](https://github.com/Ronchy2000/Visitor-Counter-Cheater)

### 📊 Online Demo

#### 🌐 [Open Live Counter Demo](https://visitor-counter-cheater.vercel.app/)

**Demo URL:** `https://visitor-counter-cheater.vercel.app/`

</div>

---

## 🔎 Start Here: Which Script Should You Run?

Most readers do not want to start with implementation details. They first want to know which script fits their target page. Use this table as the direct entry point:

| Scenario | Direct Entry | Notes |
|------|------|------|
| GitHub README visitor badge | [visitor_badge_attack.py](./visitor_badge_attack.py) | Best for `visitor-badge` counters in GitHub repositories |
| Blog/docs/static site using Busuanzi | [busuanzi_attack_efficient.py](./busuanzi_attack_efficient.py) | Direct JSONP request, fast and lightweight |
| CSDN article pages, blogs, JS-driven pages | [selenium_all_website.py](./selenium_all_website.py) | Generic browser-based workflow for regular web pages |
| Xidian teacher page counters | [xidian_counter_attack.py](./xidian_counter_attack.py) | Specialized script for the Xidian counter endpoint |
| Xidian teacher page likes | [xidian_like_attack.py](./xidian_like_attack.py) | Specialized like script, IP-limited |

If you only want to try the repository quickly, start with [visitor_badge_attack.py](./visitor_badge_attack.py). It already points to this repo by default, so the result is easy to verify.

---

## 🌐 Counter Service Websites

If you want to learn about these counter methods themselves, or you plan to add them to your own site, these official pages are useful references:

- visitor-badge: [https://visitor-badge.laobi.icu/](https://visitor-badge.laobi.icu/)
- Busuanzi: [https://busuanzi.ibruce.info/](https://busuanzi.ibruce.info/)

---

## ⚡ Quick Start

### Option 1: test this repository

```bash
git clone https://github.com/Ronchy2000/Visitor-Counter-Cheater.git
cd Visitor-Counter-Cheater
python3 visitor_badge_attack.py
```

Refresh the README page and the badge number should increase.

### Option 2: test your own target page

No matter what page you want to test, the overall workflow is the same:

1. Pick a script from the table above.
2. Edit the `CONFIG` block at the top of that script.
3. Run the script and check the page or the CSV logs in `logs/`.

For example, if you want to test a CSDN article page, you can start directly with the generic Selenium script:

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

---

## 🧭 Common Usage Paths

### 1. GitHub README badge counters

Use [visitor_badge_attack.py](./visitor_badge_attack.py):

```bash
python3 visitor_badge_attack.py
```

Then change `TARGET_URL` if needed:

```python
CONFIG = {
    "TARGET_URL": "https://github.com/username/repository",
    "MAX_VISITS": 50,
    "INTERVAL_MEAN": 1.0,
}
```

### 2. Busuanzi-powered blogs or docs sites

If the target site already uses Busuanzi, the simplest path is [busuanzi_attack_efficient.py](./busuanzi_attack_efficient.py):

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

In most cases, only `URL` needs to be changed. The script automatically uses it as the `Referer`.

### 3. CSDN, blogs, and regular web pages

Use [selenium_all_website.py](./selenium_all_website.py).

This is the general-purpose option when the page counter depends on real browser loading, JavaScript execution, scrolling, or other front-end behavior.

Typical targets:

- CSDN article pages
- Personal blog posts
- Landing pages
- Documentation pages
- Any regular page where opening the page may trigger a view counter

Example config:

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

### 4. More examples

If you want more concrete examples, open these docs directly:

- [docs/USAGE_EXAMPLE.en.md](./docs/USAGE_EXAMPLE.en.md)
- [docs/visitor_badge_analysis.en.md](./docs/visitor_badge_analysis.en.md)
- [docs/xidian_analysis.en.md](./docs/xidian_analysis.en.md)
- [docs/XIDIAN_ANALYSIS_REPORT.en.md](./docs/XIDIAN_ANALYSIS_REPORT.en.md)

---

## 💡 How It Works

### HTTP request mode

Send direct requests to the counter backend. This is the fastest option when the counter API is already known.

Pros:

- Fast
- Lightweight
- No browser dependency
- Good for batch testing

Cons:

- Works only when the counter service exposes a direct request path
- Not suitable for JS-only front-end counters

### Selenium browser mode

Open a real browser, load the page, execute JavaScript, and simulate browsing behavior. This is the broadest and most flexible option.

Pros:

- Best general compatibility
- Good for CSDN, blogs, docs pages, and other regular websites
- Works when view counting depends on front-end JS

Cons:

- Slower than HTTP mode
- Requires browser dependencies
- Higher resource usage

---

## 🎯 Supported Scripts

### 1. `visitor-badge`

- Script: [visitor_badge_attack.py](./visitor_badge_attack.py)
- Use case: GitHub README visitor badges
- Website: [https://visitor-badge.laobi.icu/](https://visitor-badge.laobi.icu/)
- Typical speed: `~600ms/request`

### 2. `busuanzi`

- Script: [busuanzi_attack_efficient.py](./busuanzi_attack_efficient.py)
- Use case: blogs/docs sites that use Busuanzi
- Website: [https://busuanzi.ibruce.info/](https://busuanzi.ibruce.info/)
- Typical speed: `~1000ms/request`

### 3. Xidian teacher page scripts

- Counter: [xidian_counter_attack.py](./xidian_counter_attack.py)
- Like: [xidian_like_attack.py](./xidian_like_attack.py)

### 4. Generic Selenium workflow

- Script: [selenium_all_website.py](./selenium_all_website.py)
- Use case: CSDN pages, blogs, landing pages, JS-driven counters

Install dependencies:

```bash
pip install selenium webdriver-manager numpy
```

---

## 📚 Documentation

- Usage Examples (Chinese): [docs/USAGE_EXAMPLE.md](./docs/USAGE_EXAMPLE.md)
- Usage Examples (English): [docs/USAGE_EXAMPLE.en.md](./docs/USAGE_EXAMPLE.en.md)
- Visitor Badge Analysis (English): [docs/visitor_badge_analysis.en.md](./docs/visitor_badge_analysis.en.md)
- Xidian Analysis (English): [docs/xidian_analysis.en.md](./docs/xidian_analysis.en.md)
- Xidian Like Analysis Report (English): [docs/XIDIAN_ANALYSIS_REPORT.en.md](./docs/XIDIAN_ANALYSIS_REPORT.en.md)

---

## 📊 Performance

| Method | Speed | Resource Usage | Best For |
|------|------|------|------|
| HTTP requests | 35-1000ms | Very low | Known back-end counters |
| Selenium | 3000-8000ms | High | CSDN, blogs, general web pages, JS-driven counters |

---

## ⚠️ Notes

- Start with small test volumes first
- Some targets may enforce IP or rate limits
- If a dedicated HTTP script does not apply, move to the Selenium workflow
- Follow site terms and local laws

---

## 📄 Disclaimer

This project is for educational and research purposes only. You are fully responsible for your own usage and any consequences.

---

## 📜 License

MIT License
