# Xidian Faculty Page Counter Analysis

[English](./xidian_analysis.en.md) | [中文](./xidian_analysis.md)

---

## Target Site

Sample page: https://faculty.xidian.edu.cn/DANDAN1/zh_CN/index.htm

## Counter System

The site has two independent mechanisms:

### 1. Visit Counter

- Endpoint: `/system/resource/tsites/click.jsp`
- Method: `GET`
- Core params:
- `lc` (faculty page path)
- `hosts`
- `ac` (`updateVisit`)
- `os`, `bs`, `vp` (optional environment info)

Observed behavior:
- Protection: none obvious
- Response time: ~35ms
- Success rate: high in basic tests

### 2. Like Action

- Endpoint: `/system/resource/tsites/praise.jsp`
- Method: `POST`
- Core params:
- `uid`
- `homepageid`
- `ac` (`updatePraise`)

Observed behavior:
- Protection: IP-based restriction
- Cooldown: around 24 hours
- Bypass usually needs proxy IP pool

## Attack Characteristics

Visit counter:
- No obvious limit
- Fast response
- Simple parameters

Like action:
- IP-level limitation exists
- Cookie alone is not enough
- Requires proxy rotation for scale

## Related Scripts

- Visit counter: `xidian_counter_attack.py`
- Like action: `xidian_like_attack.py`

## Technical Assets

Raw reverse-engineering files remain in `xidian_analysis/`, including:
- Visit tracking JavaScript
- Like logic JavaScript
- Request construction details

