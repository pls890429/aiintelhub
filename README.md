# 华为云浙江区域 AI 热点情报站

> 🦞 **每日竞对日报自动同步** — 追踪阿里云、腾讯云、火山引擎三家友商动态，洞察国内 AI 热点（Token 经济、Agent、算力、大模型出海、AI 编码），为华为云浙江区域销售制造战机。

[![Deploy to GitHub Pages](https://github.com/pls890429/aiintelhub/actions/workflows/deploy.yml/badge.svg)](https://github.com/pls890429/aiintelhub/actions/workflows/deploy.yml)

🌐 **在线访问：** https://pls890429.github.io/aiintelhub/

---

## 项目简介

这是一个零后端的纯静态情报站，基于 **React 19 + Vite 7 + TailwindCSS 4** 构建，设计主题为 **暗夜情报室**（深海蓝黑底色 + 朱砂红警示色，IBM Plex Sans 技术感字体），完全托管在 GitHub Pages 上。

主要功能：

- **情报首页**：按"Agent 框架 / 云厂商动态 / Token 经济 / AI 编码"等多维标签展示历史热点文章；
- **每日竞对日报**：每日 08:00 自动抓取过去 24 小时阿里云、腾讯云、火山引擎及国内 AI 头部厂商的最新动态，按"价格动作 / 客户案例 / 产品·模型更新 / 组织与战略"四维度整理，每条情报都附**对华为云浙江区域销售的含义** + **可直接使用的客户建联焦虑话术**；
- **三家动作对比表**：当日阿里云 vs 腾讯云 vs 火山引擎横向对照，配套华为云机会洞察一栏；
- **文章详情页**：完整阅读情报全文，支持 Markdown 渲染。

---

## 本地开发

```bash
# 安装依赖（Node.js >= 22）
npm install

# 启动开发服务器（默认 http://localhost:3000）
npm run dev

# 类型检查
npm run check

# 生产构建
npm run build

# 本地预览生产版本
npm run preview
```

---

## 项目结构

```
aiintelhub/
├── .github/workflows/deploy.yml   # GitHub Actions 自动部署配置
├── client/
│   ├── index.html                 # HTML 入口（含 Google Fonts）
│   └── src/
│       ├── App.tsx                # 路由配置（适配 /aiintelhub/ 子路径）
│       ├── main.tsx               # React 入口
│       ├── index.css              # 全局样式（暗夜情报室主题 token）
│       ├── components/            # NavBar、ErrorBoundary、shadcn/ui
│       ├── contexts/              # ThemeContext
│       ├── pages/
│       │   ├── Home.tsx           # 情报首页
│       │   ├── DailyReport.tsx    # 每日竞对日报页
│       │   ├── ArticleDetail.tsx  # 文章详情页
│       │   └── NotFound.tsx       # 404 页
│       └── data/
│           ├── intelligence.ts    # 数据加载层（导出类型定义 + 排序）
│           └── reports.json       # ⭐ 所有日报与文章数据，每日通过 git push 追加
├── vite.config.ts                 # Vite 配置（base="/aiintelhub/"）
├── tsconfig.json
└── package.json
```

---

## 部署方式

每次 `push` 到 `main` 分支会自动触发 GitHub Actions：

1. `actions/checkout@v4` 拉取代码；
2. `actions/setup-node@v4` 安装 Node.js 22 + npm 缓存；
3. `npm install` → `npm run build` 生成静态资源到 `dist/`；
4. 复制 `dist/index.html` 为 `dist/404.html` 实现 SPA 路由刷新兜底；
5. `actions/upload-pages-artifact@v3` 上传产物；
6. `actions/deploy-pages@v4` 部署到 GitHub Pages。

部署完成后约 30 秒内即可在 https://pls890429.github.io/aiintelhub/ 访问。

> **首次启用：** 在仓库 Settings → Pages 将 Source 设为 **GitHub Actions**（不是 Branch deploy），首次推送后等待 Actions 运行完毕即可。

---

## 数据更新

### 🎯 设计原则

为了支持每日 07:00 子任务自动追加新一天的日报，**所有可变内容都集中存放在一个 JSON 文件中**：

📄 `client/src/data/reports.json`

这个 JSON 包含两个顶层字段：

| 字段 | 说明 |
| --- | --- |
| `dailyReports` | 每日竞对日报列表（按日期倒序自动排列），每条包含当日 9 条情报 + 三家对比表 |
| `hotspotArticles` | 长篇热点文章列表（用于情报首页展示） |

### 📅 每日新增一份日报（推荐方式）

明早 07:00 子任务触发后，只需要按以下步骤即可发布新一天的日报，**无需修改任何源码**：

```bash
# 1. 在沙箱中克隆或更新仓库
gh repo clone pls890429/aiintelhub
cd aiintelhub

# 2. 用 Python/Node 脚本读取 reports.json，将新一天的 DailyReport 追加到 dailyReports 数组开头
python3 - <<'PY'
import json
from pathlib import Path

p = Path("client/src/data/reports.json")
data = json.loads(p.read_text(encoding="utf-8"))

new_report = {
    "id": "2026-04-21",
    "date": "2026-04-21",
    "title": "🦞 浙江云嗷嗷叫 · Manus竞对日报 · 2026-04-21",
    "coreInsight": "...",
    "items": [ ... ],            # 当日 9 条情报
    "comparisonTable": [ ... ]   # 三家对比表
}

# 去重：如果同一天的日报已存在，先移除再追加
data["dailyReports"] = [r for r in data["dailyReports"] if r["id"] != new_report["id"]]
data["dailyReports"].insert(0, new_report)

p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
PY

# 3. 提交并推送 — GitHub Actions 会自动构建并发布
git add client/src/data/reports.json
git commit -m "feat(daily): 2026-04-21 竞对日报"
git push origin main
```

整个过程一条 commit 就够了，GitHub Actions 大约 1-2 分钟内完成构建+部署。

### 📰 新增热点长文

将文章对象追加到 `reports.json` 的 `hotspotArticles` 数组即可，字段结构与现有数据一致：

```json
{
  "id": 21,
  "date": "2026-04-21",
  "categories": ["云厂商动态", "Token经济"],
  "title": "...",
  "summary": "...",
  "content": "## Markdown 正文...",
  "readTime": 6
}
```

### 🔄 数据加载逻辑

`client/src/data/intelligence.ts` 通过 `import reportsData from './reports.json'` 编译时引入数据，并在导出时按日期倒序排列。Vite 会把整个 JSON 内联到打包后的 JS 中，**首屏无网络请求**，加载速度最优。

如未来数据量超过 200KB，建议改为运行时 `fetch('/aiintelhub/reports.json')` 加载，相应地把 `reports.json` 移动到 `client/public/` 目录。

---

## 设计哲学

**暗夜情报室（Dark Intelligence Room）：**

- **色彩：** 深海蓝黑（`#0a0e1a`）作为主背景，朱砂红（`#dc2626`）作为高优先级警示色，金色（`#f59e0b`）作为价格动作标识；
- **字体：** 标题使用 `Noto Serif SC`（思源宋体）传递权威感，正文使用 `IBM Plex Sans` 营造技术感，代码使用 `IBM Plex Mono`；
- **氛围：** 模仿专业情报机构内部工作台，营造"24 小时实时情报"的紧迫感，强调数据可信度与决策时效性。

---

## 邮件订阅

如需每日 08:00 接收日报邮件，请联系 Michael 加入分发列表（当前邮件由独立 Manus subtask 通过 SMTP 直接发送至 281481047@qq.com）。

---

## License

MIT © 2026 Michael (pls890429) · 华为云浙江区域销售内部知识库
