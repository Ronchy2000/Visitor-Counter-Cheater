# 🚀 访问量计数器刷新工具

> 使用 Selenium 模拟真实浏览器访问，支持多种设备伪装和智能访问间隔控制

<div align="center">

## 📊 在线演示

### 🌐 [点击查看实时统计效果](https://visitor-counter-cheater.vercel.app/)

**演示网址：** `https://visitor-counter-cheater.vercel.app/`

运行脚本时将 URL 设置为上面的网址，然后刷新页面即可看到访问量增加！

```python
CONFIG = {
    "URL": "https://visitor-counter-cheater.vercel.app/",
    # ... 其他配置
}
```

</div>

---

## ✨ 功能特点

- 使用真实浏览器（Chrome）访问，完全模拟人类行为
- 支持 12+ 种设备伪装（桌面、手机、平板）
- 泊松分布控制访问间隔，更自然的访问节奏
- 随机滚动页面，模拟真实用户阅读
- 详细的 CSV 日志记录
- 支持无头模式，后台静默运行

## 📋 实测结果

| 脚本文件 | 方法 | 是否有效 |
|---------|------|---------|
| `selenium_github.py` | 真实浏览器模拟 | ✅ **成功** |
| `request_github.py` | HTTP 请求 | ❌ 失效 |
| `requset_github2.py` | HTTP 请求 | ❌ 失效 |

> ⚠️ 纯 HTTP 请求无法触发 JS 统计代码，只有真实浏览器访问才有效

## 🛠️ 安装依赖

```bash
pip install selenium webdriver-manager numpy
```

## 🚀 快速开始

### 1. 修改配置

编辑 `selenium_github.py` 文件的 `CONFIG` 字典：

```python
CONFIG = {
    "URL": "https://visitor-counter-cheater.vercel.app/",  # 修改为你要刷的页面
    "MAX_VISITS": 15,            # 访问次数（0 = 无限）
    "INTERVAL_MEAN": 5,          # 平均间隔秒数
    "HEADLESS": True,            # True = 后台运行
    "WAIT_AFTER_LOAD": 3.0,      # 页面加载后等待时间
}
```

### 2. 运行脚本

```bash
python selenium_github.py
```

### 3. 查看效果

- 脚本运行完成后，访问 [演示页面](https://visitor-counter-cheater.vercel.app/)
- 刷新页面，即可看到访问量和访客数增加
- 查看 `logs/visits_log_selenium.csv` 了解详细访问记录

## 📊 日志字段说明

| 字段 | 说明 |
|-----|------|
| timestamp_utc | 访问时间（UTC） |
| visit_number | 访问序号 |
| url | 目标网址 |
| user_agent | 使用的 User-Agent |
| screen_width/height | 模拟的屏幕分辨率 |
| status | 访问状态（SUCCESS/ERROR） |
| note | 备注信息 |

## ⚙️ 高级配置

### 泊松分布间隔

脚本使用泊松分布（更准确说是指数分布）来控制访问间隔，使访问时间更自然、更难被检测。

- `INTERVAL_MEAN = 5`：平均每 5 秒访问一次
- 实际间隔会在 2 秒到 15 秒之间随机波动

### 设备伪装

脚本内置 12 种设备配置：
- 桌面设备（Windows/Mac/Linux + Chrome/Firefox/Safari）
- 移动设备（iPhone/Android 多种型号）
- 平板设备（iPad/Android Tablet）

每次访问会随机选择设备和分辨率。

## 🔧 常见问题

**Q: 为什么要用 Selenium 而不是 requests？**  
A: 访问统计通过 JavaScript 实现，必须执行 JS 代码才能计数。

**Q: 无头模式会被检测吗？**  
A: 脚本已经做了反检测处理（修改 webdriver 属性、随机 UA 等），但没有 100% 保证。

**Q: 如何停止脚本？**  
A: 按 `Ctrl+C` 即可安全停止。

**Q: 日志文件在哪里？**  
A: 在脚本同目录下的 `logs/visits_log_selenium.csv`。

## ⚠️ 免责声明

本工具仅供学习和测试使用，请勿用于任何违反网站服务条款或法律法规的行为。使用者需自行承担使用本工具产生的一切后果。

## 📄 许可证

MIT License




