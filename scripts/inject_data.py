#!/usr/bin/env python3
"""
基于 data/reports.json 重新生成 site/assets/index-D4sgLSXZ.js 中的硬编码数据。

使用方法（每日更新流程）：
1. 编辑 data/reports.json（追加新一天的 dailyReports[0] 即可，或全量替换）
2. 运行: python3 scripts/inject_data.py
3. git add . && git commit -m "feat: 2026-MM-DD 日报" && git push
4. GitHub Actions 自动部署到 https://pls890429.github.io/aiintelhub/

原理：老站 JS bundle 里有两个数组：
- us = [...] 日报item列表（11条 → 我们替换为今日 N 条）
- Xr = [...] 文章列表（5条 → 我们替换为今日 N 篇）
脚本通过括号匹配定位这两个数组的精确范围并整体替换。
"""
import json
import re
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(REPO_ROOT, 'data', 'reports.json')
JS_PATH = os.path.join(REPO_ROOT, 'site', 'assets', 'index-D4sgLSXZ.js')
CSS_PATH = os.path.join(REPO_ROOT, 'site', 'assets', 'index-7D7zrsbW.css')
EXTRA_CSS_PATH = os.path.join(REPO_ROOT, 'data', 'detail-style.css')

VENDOR_MAP = {
    'aliyun': '阿里云',
    'tencent': '腾讯云',
    'volcano': '火山引擎',
    'ai-hotspot': 'AI热点',
    'baidu': '百度智能云',
}

DIM_MAP = {
    'price': '价格动作',
    'customer': '客户案例',
    'product': '产品/模型更新',
    'strategy': '组织与战略',
}


def vendor_to_str(v):
    if isinstance(v, list):
        return ' / '.join(VENDOR_MAP.get(x, x) for x in v)
    return VENDOR_MAP.get(v, v)


def urgency_to_action_tag(urgency, dimension):
    if urgency == 'high':
        return '💡机会把握' if dimension == 'price' else '⚔威胁应对'
    return '📋信息备用'


def to_js_literal(obj):
    """把Python对象转成JS对象字面量（key不带引号）"""
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(to_js_literal(x) for x in obj) + ']'
    if isinstance(obj, dict):
        parts = []
        for k, v in obj.items():
            key_str = k if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', k) else json.dumps(k, ensure_ascii=False)
            parts.append(f'{key_str}:{to_js_literal(v)}')
        return '{' + ','.join(parts) + '}'
    raise ValueError(f"unsupported type: {type(obj)}")


def find_array_end(text, start_idx):
    """从 [ 位置开始找到匹配的 ]"""
    depth = 0
    in_string = None
    escape = False
    i = start_idx
    while i < len(text):
        c = text[i]
        if escape:
            escape = False
            i += 1
            continue
        if c == '\\':
            escape = True
            i += 1
            continue
        if in_string:
            if c == in_string:
                in_string = None
            i += 1
            continue
        if c in ('"', "'", '`'):
            in_string = c
            i += 1
            continue
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def build_us(reports):
    """构造老站 us 数组（扁平item列表）。把所有日报的所有item铺开，按日期降序，最新的在前。"""
    items_out = []
    item_id = 1
    # 按日期降序遍历
    sorted_reports = sorted(reports, key=lambda r: r['date'], reverse=True)
    for rpt in sorted_reports:
        for it in rpt['items']:
            vendor_str = vendor_to_str(it['vendor'])
            product = DIM_MAP.get(it['dimension'], it['dimension'])
            action_tag = urgency_to_action_tag(it.get('urgency', 'medium'), it['dimension'])
            action = f"{it['hwImplication']}\n\n销售话术：「{it['anxietyScript']}」"
            items_out.append({
                'id': item_id,
                'vendor': vendor_str,
                'product': product,
                'title': it['title'],
                'summary': it.get('detail', it.get('summary', '')),
                'actionTag': action_tag,
                'action': action,
                'tags': it.get('categories', []),
                'date': it['date'],
            })
            item_id += 1

        # 把comparisonTable作为该日的特殊条目
        if rpt.get('comparisonTable'):
            md = "| 维度 | 阿里云 | 腾讯云 | 火山引擎 | 华为云机会 |\n|---|---|---|---|---|\n"
            for row in rpt['comparisonTable']:
                md += f"| {row['dimension']} | {row['aliyun']} | {row['tencent']} | {row['volcano']} | **{row['hwOpportunity']}** |\n"
            items_out.append({
                'id': item_id,
                'vendor': '阿里云 / 腾讯云 / 火山引擎',
                'product': '三家动作横向对比表',
                'title': f'🦞 {rpt["date"]} 三家友商横向对比 · 价格/客户/产品/战略',
                'summary': '今日三家友商在价格、客户、产品、战略四个维度上的横向对比，便于销售快速识别华为云的机会窗口。\n\n' + md,
                'actionTag': '💡机会把握',
                'action': '横向对比表是销售拜访客户时的核心武器，建议截图保存到手机随时调用。重点关注华为云机会列，每一个机会点都对应一个可立即建联的客户场景。',
                'tags': ['横向对比', '销售工具', '战机识别'],
                'date': rpt['date'],
            })
            item_id += 1
    return items_out


def md_to_html(md):
    """极简 markdown → HTML（仅处理 ##/###/段落/列表/加粗）"""
    if not md:
        return '<p></p>'
    lines = md.split('\n')
    out = []
    in_ul = False
    for ln in lines:
        s = ln.rstrip()
        if not s:
            if in_ul:
                out.append('</ul>'); in_ul = False
            continue
        if s.startswith('### '):
            if in_ul: out.append('</ul>'); in_ul = False
            out.append(f'<h3>{s[4:]}</h3>')
        elif s.startswith('## '):
            if in_ul: out.append('</ul>'); in_ul = False
            out.append(f'<h3>{s[3:]}</h3>')
        elif s.startswith('- ') or s.startswith('* '):
            if not in_ul: out.append('<ul>'); in_ul = True
            out.append(f'<li>{s[2:]}</li>')
        else:
            if in_ul: out.append('</ul>'); in_ul = False
            # 加粗
            t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
            out.append(f'<p>{t}</p>')
    if in_ul: out.append('</ul>')
    return '\n'.join(out)


def build_xr(articles):
    """构造老站 Xr 数组（文章列表）。如果 article 已带 sections，直接用；否则 fallback 把 content 当 markdown 渲染"""
    out = []
    for art in articles:
        if art.get('sections'):
            sections = art['sections']
        else:
            sections = [{
                'title': '正文',
                'content': md_to_html(art.get('content', '')),
            }]
        out.append({
            'id': str(art['id']),
            'title': art['title'],
            'summary': art['summary'],
            'tags': art.get('categories', []),
            'date': art['date'],
            'coverImage': art.get('coverImage', 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&q=80'),
            'sections': sections,
        })
    return out


def merge_extra_css():
    """把 data/detail-style.css 合并到主 CSS 末尾（去重幂等）"""
    if not os.path.exists(EXTRA_CSS_PATH):
        return
    extra = open(EXTRA_CSS_PATH).read().strip()
    base = open(CSS_PATH).read()
    marker = '/* ============================================'
    if marker in base:
        # 已有附加CSS，先去掉再追加最新
        base = base[:base.index(marker)].rstrip() + '\n'
    open(CSS_PATH, 'w').write(base + '\n' + extra + '\n')
    print(f"✓ CSS 合并完成: +{len(extra)} 字节")


def main():
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)

    us_arr = build_us(data['dailyReports'])
    xr_arr = build_xr(data.get('hotspotArticles', []))

    us_js = to_js_literal(us_arr)
    xr_js = to_js_literal(xr_arr)

    with open(JS_PATH, 'r') as f:
        bundle = f.read()

    # 定位 us 和 Xr 的范围（每次都重新搜索，因为bundle可能变化）
    us_marker = ',us=['
    xr_marker = ',Xr=['
    us_pos = bundle.find(us_marker)
    xr_pos = bundle.find(xr_marker)
    assert us_pos > 0 and xr_pos > 0, "未找到 us 或 Xr 标记"

    us_start = us_pos + len(us_marker) - 1
    us_end = find_array_end(bundle, us_start)
    xr_start = xr_pos + len(xr_marker) - 1
    xr_end = find_array_end(bundle, xr_start)

    assert us_end > 0 and xr_end > 0, "数组结尾匹配失败"
    assert xr_start < us_start, "假设Xr在us前面，请检查"

    new_bundle = (
        bundle[:xr_start] + xr_js +
        bundle[xr_end + 1:us_start] + us_js +
        bundle[us_end + 1:]
    )

    # ===== 替换日报页硬编码的日期和核心研判 =====
    # 取最新一天的日报作为标题日期/核心研判源
    latest = sorted(data['dailyReports'], key=lambda r: r['date'], reverse=True)[0]
    y, m, d = latest['date'].split('-')
    new_date_label = f"{y}年{int(m)}月{int(d)}日"
    new_subtitle = f"{new_date_label} · 追踪阿里云、腾讯云、火山引擎及大模型厂商最新动态 · 每天 8:00 自动更新"
    new_insight = latest.get('coreInsight', latest.get('summary', ''))

    # 替换副标题（匹配任意日期前缀）
    new_bundle = re.sub(
        r'\d{4}年\d{1,2}月\d{1,2}日 · 追踪阿里云、腾讯云、火山引擎及大模型厂商最新动态 · 每天 8:00 自动更新',
        new_subtitle,
        new_bundle
    )
    # 替换核心研判（替换原老站固定那段）
    OLD_INSIGHT = '阿里云四天三次涨价 + 腾讯云AI算力涨价5%，行业进入「算力通胀」周期。华为云基于昇腾国产算力的供应链自主可控优势凸显，是争取价格敏感客户迁移的最佳窗口期。同时，DeepSeek V4已完成华为昇腾芯片适配，将成为华为云差异化竞争的重要筹码。'
    if OLD_INSIGHT in new_bundle:
        new_bundle = new_bundle.replace(OLD_INSIGHT, new_insight)

    with open(JS_PATH, 'w') as f:
        f.write(new_bundle)

    print(f"✓ 注入完成")
    print(f"  日报 items: {len(us_arr)} 条")
    print(f"  文章: {len(xr_arr)} 篇")
    print(f"  bundle 大小: {len(bundle)} → {len(new_bundle)} 字节")

    # 合并附加 CSS
    merge_extra_css()


if __name__ == '__main__':
    main()
