# AI热点情报站 设计方案

## 设计背景
面向华为云浙江区域销售团队的竞对情报工具，需要专业、严肃、信息密度高，同时移动端友好。

<response>
<text>
**设计方案A：暗夜情报室（Dark Intelligence Room）**

- **Design Movement**: 暗色系信息密度美学，参考Bloomberg Terminal + 军事情报系统
- **Core Principles**: 深色背景强调信息权威感；红色/橙色高亮警示竞对动态；数据密度高但层次分明；移动端优先
- **Color Philosophy**: 深海蓝黑(#0A0E1A)为底，朱砂红(#E63946)为警示色，金属银(#8892A4)为辅助文字，纯白为主文字
- **Layout Paradigm**: 左侧固定导航栏 + 右侧内容区，卡片式情报条目，顶部日期横幅
- **Signature Elements**: 红色竖线分隔符、数字编号徽章、"CLASSIFIED"风格标签
- **Interaction Philosophy**: 悬停时卡片轻微上浮，点击展开详情，平滑过渡
- **Animation**: 页面加载时情报卡片从下方淡入，数字计数动画
- **Typography System**: 标题用Noto Serif SC（权威感），正文用IBM Plex Sans（技术感）
</text>
<probability>0.08</probability>
</response>

<response>
<text>
**设计方案B：战情室仪表盘（War Room Dashboard）**

- **Design Movement**: 军事指挥中心美学，参考CIA情报仪表盘
- **Core Principles**: 网格布局展示多维度数据；颜色编码区分三家友商；实时感强；信息层级清晰
- **Color Philosophy**: 深炭灰(#1C1C1E)为底，阿里橙(#FF6A00)/腾讯蓝(#0052D9)/火山红(#FF3B30)三色区分友商，绿色为华为云机会色
- **Layout Paradigm**: 顶部状态栏 + 三列友商对比 + 底部AI热点流
- **Signature Elements**: 友商Logo色块标识、实时更新时间戳、机会评分仪表盘
- **Interaction Philosophy**: 点击友商切换视角，筛选器实时过滤
- **Animation**: 数据加载时扫描线动画，卡片展开时弹性动画
- **Typography System**: 标题用Source Han Sans CN Bold，正文用Roboto Mono
</text>
<probability>0.07</probability>
</response>

<response>
<text>
**设计方案C：极简情报卡片流（Minimal Intelligence Feed）**

- **Design Movement**: 极简主义 + 新闻媒体美学，参考The Information + 路透社
- **Core Principles**: 白底黑字最大化可读性；色彩仅用于分类标签；卡片间距宽松；移动端阅读体验优先
- **Color Philosophy**: 纯白(#FFFFFF)为底，深墨(#1A1A2E)为主文字，警示红(#D62828)为重要标签，天蓝(#457B9D)为链接色
- **Layout Paradigm**: 单列时间轴式情报流，右侧浮动筛选面板
- **Signature Elements**: 左侧彩色竖条分类标识、时间戳徽章、"对华为云意义"折叠展开区块
- **Interaction Philosophy**: 滚动加载，点击展开详情，长按收藏
- **Animation**: 新内容滑入动画，展开/折叠弹性动画
- **Typography System**: 标题用Noto Serif SC，正文用Noto Sans SC
</text>
<probability>0.06</probability>
</response>

## 选定方案
**选定方案A：暗夜情报室**，最符合情报工具的专业气质，深色背景降低长时间阅读疲劳，红色警示色突出竞对威胁。
