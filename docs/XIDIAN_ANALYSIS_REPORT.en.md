# Xidian Faculty Like Function Analysis Report

[English](./XIDIAN_ANALYSIS_REPORT.en.md) | [中文](./XIDIAN_ANALYSIS_REPORT.md)

---

## Summary

### Completed
1. Visit counter refresh: working reliably
- Script: `xidian_counter_attack.py`
- Method: direct `click.jsp` request
- Speed: ~35-40ms/request
- Protection: none obvious

2. Like action: partially successful
- Script: `xidian_like_attack.py`
- First like can succeed
- Repeated likes are blocked by IP-level control

## Protection Analysis

### 1. Client-side cookie gate

Front-end JS sets a cookie key similar to `tsites_praise_<uid>` with about 24h TTL.
Clearing browser cookies bypasses only the client-side check.

### 2. Server-side IP limit

Backend `praise.jsp` appears to validate source IP.
Even with different cookies/sessions, repeated requests from same IP are rejected.

### 3. Session-related cookies

Observed cookies include:
- `JSESSIONID`
- Additional site-specific token-like cookie

## Practical Bypass Options

### Option 1: Proxy pool (recommended)

Rotate outbound IP per like request.

Pros:
- Can bypass IP-based single-like limit
- Good scalability

Cons:
- Requires proxy source
- Has operational cost

### Option 2: Slow mode

Send one like per cooldown period (about 24h).

Pros:
- Simple

Cons:
- Very low throughput

### Option 3: Deep backend reverse-engineering

Higher complexity and time cost; only for deep research scenarios.

## Demo Commands

```bash
python3 xidian_counter_attack.py
python3 xidian_like_attack.py
```

## Security Comparison

| Feature | Protection | Automation Feasibility |
|---|---|---|
| Visit counter | Low | High |
| Like action | Medium | Needs IP rotation |

## Takeaways

1. Front-end checks are usually easy to bypass.
2. Backend IP throttling is the real blocker for repeated likes.
3. Multi-layer protections require multi-layer bypass strategy.

## Main Files

```text
xidian_counter_attack.py
xidian_like_attack.py
debug_like_protection.py
analyze_xidian.py
TsitesPraiseUtil.js
counter_js_*.js
xidian_page.html
```

