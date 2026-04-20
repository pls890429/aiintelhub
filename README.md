# 华为云 AI 热点情报站 · 浙江区域竞对日报

> 🦞 面向华为云浙江区域销售团队的 AI 热点情报知识库，每日同步阿里云 / 腾讯云 / 火山引擎竞对动态，含华为云销售含义和焦虑话术。

[![Deploy to GitHub Pages](https://github.com/pls890429/aiintelhub/actions/workflows/main.yml/badge.svg)](https://github.com/pls890429/aiintelhub/actions/workflows/main.yml)

🌐 **在线访问：** https://pls890429.github.io/aiintelhub/

---

## 项目说明

本站是 Manus 老站 `aiintelhub-alzate89.manus.space` 的 **1:1 静态克隆版本**，迁移到 GitHub Pages 长期托管，与 Manus 账号完全脱钩。

**核心特性：**
- ✅ 与老站视觉/交互完全一致（直接复用老站构建产物 `site/assets/index-D4sgLSXZ.js`）
- ✅ 数据通过 `data/reports.json` 单独维护，每天 commit 一次即可触发自动重新部署
- ✅ 零 Node 构建依赖 —— 只需 Python，纯静态文件部署
- ✅ 完全独立托管，长期可靠

---

## 仓库结构

```
aiintelhub/
├── data/
│   └── reports.json          ← ⭐ 数据源（每日唯一需要修改的文件）
├── scripts/
│   └── inject_data.py        ← 把 reports.json 注入到 JS bundle
├── site/                     ← 老站克隆产物（静态资源）
│   ├── index.html
│   └── assets/
│       ├── index-D4sgLSXZ.js  ← 内嵌数据的 JS bundle
│       └── index-7D7zrsbW.css
├── .github/workflows/
│   └── main.yml              ← GitHub Actions 部署工作流
├── package.json              ← 极简 build 脚本（包装 Python 注入命令）
└── README.md
```

---

## 部署方式

每次 push 到 `main` 分支时，GitHub Actions 自动执行：

1. `npm run build` →  实际跑 `python3 scripts/inject_data.py && cp -r site dist`
2. 复制 `dist/index.html` → `dist/404.html` 实现 SPA 路由刷新兜底
3. `actions/upload-pages-artifact@v3` 上传 `dist/` 作为 Pages 产物
4. `actions/deploy-pages@v4` 发布到 https://pls890429.github.io/aiintelhub/

整个流程约 30-60 秒完成。

---

## 数据更新流程（每日）

### 方案 A：手动追加新一天日报

```bash
# 1. 克隆仓库（首次）
gh repo clone pls890429/aiintelhub
cd aiintelhub

# 2. 编辑 data/reports.json，在 dailyReports 数组开头插入新一天的日报对象

# 3. （可选）本地预览验证
npm run build
cd dist && python3 -m http.server 8080
# 浏览器访问 http://localhost:8080/aiintelhub/

# 4. 提交并推送
git add data/reports.json
git commit -m "feat: YYYY-MM-DD 竞对日报"
git push
```

push 后约 1 分钟，新内容自动上线。

### 方案 B：Manus subtask 自动化（推荐）

每天 07:00 触发的 `浙江云竞对日报` subtask 在抓取整理完情报后，按以下流程自动 commit：

```python
import json, subprocess, os
from datetime import date

# 1. 拉取仓库
os.chdir('/tmp')
subprocess.run(['rm', '-rf', 'aiintelhub'])
subprocess.run(['gh', 'repo', 'clone', 'pls890429/aiintelhub', '--', '--depth=1'])
os.chdir('/tmp/aiintelhub')

# 2. 读取现有 reports.json
with open('data/reports.json') as f:
    data = json.load(f)

# 3. 构造新一天的日报对象（来自抓取整理结果）
today = str(date.today())
new_report = {
    "id": today,
    "date": today,
    "title": f"🦞 浙江云嗷嗷叫 · Manus竞对日报 · {today}",
    "coreInsight": "今日核心研判...",
    "items": [...],         # 9 条情报
    "comparisonTable": [...],
}

# 4. 去重并插入到数组开头
data['dailyReports'] = [r for r in data['dailyReports'] if r['id'] != today]
data['dailyReports'].insert(0, new_report)

# 5. 写回
with open('data/reports.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 6. 提交推送
subprocess.run(['git', 'config', 'user.email', 'pls890429@gmail.com'])
subprocess.run(['git', 'config', 'user.name', 'Michael'])
subprocess.run(['git', 'add', 'data/reports.json'])
subprocess.run(['git', 'commit', '-m', f'feat: {today} 竞对日报'])
subprocess.run(['git', 'push'])
```

---

## 数据结构（data/reports.json）

```jsonc
{
  "dailyReports": [
    {
      "id": "2026-04-20",
      "date": "2026-04-20",
      "title": "🦞 浙江云嗷嗷叫 · Manus竞对日报 · 2026-04-20",
      "coreInsight": "今日核心研判...",
      "items": [
        {
          "id": 1,
          "date": "2026-04-20",
          "vendor": ["aliyun", "tencent"],   // aliyun/tencent/volcano/ai-hotspot/baidu
          "dimension": "price",               // price/customer/product/strategy
          "categories": ["云厂商动态"],
          "title": "...",
          "summary": "...",
          "detail": "...",
          "hwImplication": "对华为云销售的含义...",
          "anxietyScript": "可直接用于建联的焦虑话术...",
          "urgency": "high"                   // high/medium/low
        }
      ],
      "comparisonTable": [
        {
          "dimension": "💰 价格动作",
          "aliyun": "...",
          "tencent": "...",
          "volcano": "...",
          "hwOpportunity": "..."
        }
      ]
    }
  ],
  "hotspotArticles": [
    {
      "id": "...",
      "date": "2026-04-20",
      "categories": [],
      "title": "...",
      "summary": "...",
      "content": "Markdown 内容...",
      "readTime": 5
    }
  ]
}
```

---

## 关键技术点

- **JS bundle 数据注入**：老站 React 代码是 minified 的，所有数据硬编码在 bundle 里：
  - 变量 `us = [...]` 是日报 item 列表
  - 变量 `Xr = [...]` 是文章列表
  - `scripts/inject_data.py` 通过括号匹配定位这两个数组的精确字节范围并整体替换。
- **wouter base 路径**：通过把 bundle 里 `parser:uE,base:""` 替换为 `parser:uE,base:"/aiintelhub"`，让 SPA 路由在子路径下正确工作。
- **404 fallback**：workflow 里 `cp dist/index.html dist/404.html` 让所有路径都 fallback 到 SPA 入口，避免刷新页面 404。

---

## 维护说明

- 老站 bundle 哈希：`index-D4sgLSXZ.js` / `index-7D7zrsbW.css`
- 如果老站更新了视觉/交互，重新 wget dump 一次老站，覆盖 `site/`，再跑一次 `npm run build` 验证即可。
- 如果 inject 脚本因为 bundle 结构变化失败，检查 `,us=[` / `,Xr=[` 标记是否还存在（minify 后变量名可能变化）。

---

## 联系方式

- **维护者：** Michael (华为云浙江区域销售)
- **GitHub：** [@pls890429](https://github.com/pls890429)
- **邮箱：** pls890429@gmail.com

---

## License

MIT © 2026 Michael (pls890429) · 华为云浙江区域销售内部知识库
