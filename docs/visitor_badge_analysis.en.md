# Visitor Badge Counter Guide

[English](./visitor_badge_analysis.en.md) | [中文](./visitor_badge_analysis.md)

---

## Service Overview

- Project: [visitor-badge](https://github.com/jwenjian/visitor-badge)
- Service host: `visitor-badge.laobi.icu`

## Usage

### 1. Interactive tool (recommended)

Run `visitor_badge_tool.py`:

```bash
python3 visitor_badge_tool.py
```

Menu:

```text
1. Query current visits (no increment)
2. Visit once (+1)
3. Batch visits
0. Exit
```

Accepted input:
- Repository format: `username/repo`
- Full URL: `https://github.com/username/repo`

### 2. Analysis script

Run `analyze_visitor_badge.py`:

```bash
python3 analyze_visitor_badge.py
```

It will:
- Analyze GitHub page structure
- Extract `page_id`
- Test query and increment behavior
- Check basic anti-abuse behavior

## Counting Mechanism

`visitor-badge` is an SVG-based counter mostly used in GitHub README badges.

How it works:
1. Send a GET request and receive SVG.
2. Main parameters:
- `page_id`: page identifier (for example `username.repository`)
- `style`: badge style (for example `flat`, `for-the-badge`)
- `color`: badge color
- `query_only`: query without increment
3. Behavior:
- Normal request increments by `+1`
- `query_only=true` returns current value only
- No auth required
- No obvious rate limit in basic tests

Example URLs:

```text
# increments
https://visitor-badge.laobi.icu/badge?page_id=Ronchy2000.Xidian-LaTeX-Template-for-macOS

# query only
https://visitor-badge.laobi.icu/badge?page_id=Ronchy2000.Xidian-LaTeX-Template-for-macOS&query_only=true
```

## Key Characteristics

- No obvious protection found
- Fast response (~600ms)
- High success rate in basic tests
- Supports query-only mode

## Files

- `visitor_badge_tool.py` - interactive tool
- `analyze_visitor_badge.py` - analysis script
- `visitor_badge_analysis.md` - Chinese doc
- `visitor_badge_analysis.en.md` - English doc

## Related Script

Use the root script: `visitor_badge_attack.py`.

