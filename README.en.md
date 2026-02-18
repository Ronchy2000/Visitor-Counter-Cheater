# 🚀 Visitor Counter Booster Toolkit

[English](./README.en.md) | [中文](./README.md)

---

> A toolkit for testing and boosting public counter services with efficient HTTP requests, Selenium browser simulation, and device fingerprint rotation.

<div align="center">

[![visitors](https://visitor-badge.laobi.icu/badge?page_id=ronchy2000.Visitor-Counter-Cheater&left_color=gray&right_color=blue&style=for-the-badge)](https://github.com/Ronchy2000/Visitor-Counter-Cheater)

### 📊 Online Demo

#### 🌐 [Open Live Counter Demo](https://visitor-counter-cheater.vercel.app/)

**Demo URL:** `https://visitor-counter-cheater.vercel.app/`

</div>

---

## ⚡ Quick Start

### Option 1: Test this repository (recommended)

```bash
git clone https://github.com/Ronchy2000/Visitor-Counter-Cheater.git
cd Visitor-Counter-Cheater
python3 visitor_badge_attack.py
```

Expected result: refresh the README page and the badge number increases.

### Option 2: Test the online demo page

```bash
python3 busuanzi_attack_efficient.py
# or
python3 selenium_all_website.py
```

Example config:

```python
CONFIG = {
    "TARGET_URL": "https://visitor-counter-cheater.vercel.app/",
    "MAX_VISITS": 50,
}
```

---

## 🌐 Documentation

- Usage Examples (English): [docs/USAGE_EXAMPLE.en.md](./docs/USAGE_EXAMPLE.en.md)
- Visitor Badge Analysis (English): [docs/visitor_badge_analysis.en.md](./docs/visitor_badge_analysis.en.md)
- Xidian Analysis (English): [docs/xidian_analysis.en.md](./docs/xidian_analysis.en.md)
- Xidian Like Analysis Report (English): [docs/XIDIAN_ANALYSIS_REPORT.en.md](./docs/XIDIAN_ANALYSIS_REPORT.en.md)

---

## 💡 How It Works

### HTTP request mode (fastest)

Send direct HTTP requests to the counter backend. This is typically much faster and lighter than browser automation.

Pros:
- Very fast throughput
- Low resource usage
- Easy to scale with concurrency

Cons:
- Works only for server-side counters
- Some JS-only front-end counters need browser execution

### Selenium browser mode (most compatible)

Use a real browser to execute page JavaScript and mimic human visits.

Pros:
- High compatibility
- Simulates real user behavior
- Works for complex JS counter logic

Cons:
- Slower than HTTP mode
- Higher CPU/memory usage
- Needs browser and driver setup

---

## 🎯 Supported Targets

### 1. `visitor-badge`

- Script: `visitor_badge_attack.py`
- Use case: README badge counters
- Typical speed: ~600ms/request

### 2. `busuanzi`

- Script: `busuanzi_attack_efficient.py`
- Use case: Busuanzi page/site counters
- Typical speed: ~1000ms/request

### 3. Xidian teacher page counters/likes

- Scripts:
- Counter: `xidian_counter_attack.py`
- Like: `xidian_like_attack.py`

### 4. Generic Selenium method

- Script: `selenium_all_website.py`
- Use when specialized scripts are not applicable

---

## 📁 Project Structure

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

## ⚠️ Notes

- Use responsible request frequency.
- Some targets may apply anti-abuse rules (IP limits/rate limits).
- Please follow the target website terms and local laws.

---

## 📄 Disclaimer

This project is for educational and research purposes only.  
You are fully responsible for your own usage and any consequences.

---

## 📜 License

MIT License
