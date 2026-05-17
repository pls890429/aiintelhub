import json

# 读取现有reports.json
with open('/tmp/aiintelhub/data/reports.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

reports = data.get('reports', [])

# 添加新报告
new_report = {
    "id": "20260518",
    "title": "🦞 浙江云嗷嗷叫 · 扣子竞对日报 · 20260518",
    "date": "2026-05-18",
    "weekday": "星期一",
    "summary": "火山引擎Agent Plan发布 · Kimi WebBridge亮相 · 豆包付费引发算力讨论",
    "vendor_tags": ["火山引擎", "Kimi", "豆包", "阿里云", "DeepSeek"],
    "key_highlights": [
        "火山引擎发布Agent Plan，首个Agent套餐包搅局MaaS市场",
        "Kimi发布WebBridge，让Agent像真人一样操作浏览器",
        "豆包付费订阅引发行业讨论，Token经济学成焦点"
    ],
    "file": "20260518_竞对日报.html",
    "url": "https://www.coze.cn/s/Wof-k1SxmK8/"
}

# 检查是否已存在今天的报告
exists = False
for i, report in enumerate(reports):
    if report.get('id') == '20260518':
        reports[i] = new_report
        exists = True
        break

if not exists:
    # 添加到最前面
    reports.insert(0, new_report)

# 保存
data['reports'] = reports
with open('/tmp/aiintelhub/data/reports.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"更新完成，共{len(reports)}条报告")
