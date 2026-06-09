#!/usr/bin/env python3
"""
基于 data/reports.json 重新生成 site/assets/index-D4sgLSXZ.js 中的硬编码数据。

使用方法（每日更新流程）：
1. 编辑 data/reports.json（追加新一天的 reports[0] / dailyReports[0] 即可，或全量替换）
2. 运行: python3 scripts/inject_data.py
3. git add . && git commit -m "feat: 2026-MM-DD 日报" && git push
4. GitHub Actions 自动部署到 https://pls890429.github.io/aiintelhub/

原理：老站 JS bundle 里有两个数组：
- Xr = [...] 首页热点文章列表；Home 页面通过 BE()/kE() 读取该数组并生成统计和标签筛选
- us = [...] 每日竞对日报 item 列表；DailyReport 页面按 vendor 精确分组渲染
脚本通过括号匹配定位这两个数组的精确范围并整体替换。
"""
import html
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
    '阿里': '阿里云',
    '阿里云': '阿里云',
    '腾讯': '腾讯云',
    '腾讯云': '腾讯云',
    '火山': '火山引擎',
    '火山引擎': '火山引擎',
    '字节': '火山引擎',
    '字节跳动': '火山引擎',
    '豆包': '火山引擎',
    '扣子': '火山引擎',
    'Coze': '火山引擎',
    'coze': '火山引擎',
}

DIM_MAP = {
    'price': '价格动作',
    'customer': '客户案例',
    'product': '产品/模型更新',
    'strategy': '组织与战略',
}

DAILY_VENDOR_BUCKETS = ['阿里云', '腾讯云', '火山引擎', '大模型厂商']
DEFAULT_COVER_IMAGE = 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&q=80'


def normalize_vendor(v):
    if not v:
        return None
    if isinstance(v, list):
        normalized = [normalize_vendor(x) for x in v]
        normalized = [x for x in normalized if x]
        if len(normalized) == 1:
            return normalized[0]
        return ' / '.join(normalized) if normalized else None
    return VENDOR_MAP.get(str(v), str(v))


def vendor_to_str(v):
    return normalize_vendor(v) or 'AI热点'


def infer_vendor_from_text(text, fallback_vendors=None):
    """根据标题/摘要推断日报页使用的四类 vendor，确保命中前端精确分组。"""
    text = text or ''
    rules = [
        ('腾讯云', ['腾讯云', '腾讯', 'Tencent']),
        ('阿里云', ['阿里云', '阿里', '通义', 'Qwen', 'PAI', '百炼', '千问']),
        ('火山引擎', ['火山引擎', '火山', '字节跳动', '字节', '豆包', '扣子', 'Coze', 'coze', '赛豆']),
        ('大模型厂商', ['DeepSeek', 'Kimi', '月之暗面', 'OpenAI', '微软', '智谱', 'MiniMax', '商汤', '百度', '小米', 'Anthropic', 'Claude', 'Gemini']),
    ]
    for vendor, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return vendor

    for raw in fallback_vendors or []:
        normalized = normalize_vendor(raw)
        if normalized in DAILY_VENDOR_BUCKETS:
            return normalized
    return '大模型厂商'


def infer_product_from_text(text, dimension=None):
    if dimension:
        return DIM_MAP.get(dimension, dimension)
    text = text or ''
    if any(k in text for k in ['降价', '涨价', '价格', '收费', '免费', 'Token Plan', 'API', '成本', '定价']):
        return '价格动作'
    if any(k in text for k in ['客户', '案例', '中标', '合作', '签约', '落地', '行业', '汽车', '医疗', '政务', '金融']):
        return '客户案例'
    if any(k in text for k in ['发布', '上线', '开源', '升级', '模型', '平台', '工具', 'Agent', '智能体', '套件', '能力']):
        return '产品/模型更新'
    return '组织与战略'


def infer_urgency(text, product):
    text = text or ''
    if product == '价格动作' or any(k in text for k in ['降价', '涨价', '收费', '融资', '上市', '中标', '客户']):
        return 'high'
    if any(k in text for k in ['发布', '上线', '开源', '升级', '大会']):
        return 'medium'
    return 'low'


def urgency_to_action_tag(urgency, dimension_or_product):
    if urgency == 'high':
        return '💡机会把握' if dimension_or_product in ('price', '价格动作', '客户案例') else '⚔威胁应对'
    return '📋信息备用'


def infer_tags(text, vendor=None, product=None, report=None):
    text = text or ''
    tags = []
    if vendor in ['阿里云', '腾讯云', '火山引擎'] or any(k in text for k in ['云', '火山', '阿里', '腾讯']):
        tags.append('云厂商动态')
    else:
        tags.append('大模型')
    tags.append('竞争分析')

    if any(k in text for k in ['Agent', '智能体', '扣子', 'Coze', 'coze', '工具集']):
        tags.append('Agent框架')
    if any(k in text for k in ['Token', 'API', '降价', '涨价', '收费', '成本', '价格']):
        tags.append('Token经济')
    if any(k in text for k in ['客户', '案例', '行业', '汽车', '医疗', '政务', '金融', '电商']):
        tags.append('销售策略')
    if any(k in text for k in ['融资', '上市', '份额', '市场', '大会', '战略', '预算', '全球', '出海']):
        tags.append('行业趋势')
    if product == '产品/模型更新' or any(k in text for k in ['模型', '发布', '升级', '开源', 'Qwen', 'DeepSeek', '豆包', 'Kimi']):
        tags.append('大模型')

    for raw in (report or {}).get('categories', []) or []:
        if raw not in tags:
            tags.append(raw)

    # 保持顺序去重，并控制卡片标签数量。
    deduped = []
    for tag in tags:
        if tag and tag not in deduped:
            deduped.append(tag)
    return deduped[:4]


def build_action(vendor, title, product):
    if product == '价格动作':
        implication = f'{vendor}在价格/成本侧出现新动作，建议优先排查浙江区域价格敏感型客户，围绕华为云稳定供给、国产算力和综合 TCO 优势开展迁移测算。'
        script = '最近友商价格和计费策略变化比较频繁，您这边 AI 训练或推理成本是否有压力？我们可以用华为云方案帮您做一次成本与迁移收益测算。'
    elif product == '客户案例':
        implication = f'{vendor}在重点行业或标杆客户上强化攻势，华为云需尽快识别同类客户场景，准备昇腾算力、ModelArts及行业解决方案的替代话术。'
        script = '友商已经在类似行业释放标杆案例，建议我们尽快交流贵司 AI 场景规划，看看华为云是否能提供更稳、更安全、更贴近行业的方案。'
    elif product == '产品/模型更新':
        implication = f'{vendor}产品/模型能力持续更新，销售侧应关注客户是否因此重新评估云厂商能力，并及时同步华为云昇腾、ModelArts 等方案进展。'
        script = '近期友商模型和工具更新较快，您如果在做选型，我们也可以同步华为云最新能力，特别是国产算力适配、安全合规和企业级落地支持。'
    else:
        implication = f'{vendor}释放组织、资本或战略层面的新信号，建议持续跟踪其对客户预算、技术路线和云厂商选型的影响。'
        script = '近期行业格局变化很快，建议我们提前评估对您 AI 建设路线的影响，华为云可以结合现有业务给出更稳妥的推进建议。'
    return f'{implication}\n\n销售话术：「{script}」'


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
    """构造老站 us 数组（扁平日报 item 列表），字段需匹配 DailyReport 页面。"""
    items_out = []
    item_id = 1
    sorted_reports = sorted(reports, key=lambda r: r['date'], reverse=True)
    for rpt in sorted_reports:
        report_vendors = rpt.get('vendors') or rpt.get('vendor_tags') or []
        items = rpt.get('items')
        if items is None:
            items = []
            highlights_list = rpt.get('key_highlights', []) or rpt.get('highlights', [])
            for hl in highlights_list:
                vendor = infer_vendor_from_text(hl, report_vendors)
                product = infer_product_from_text(hl)
                tags = infer_tags(hl, vendor=vendor, product=product, report=rpt)
                items.append({
                    'vendor': vendor,
                    'product': product,
                    'title': hl,
                    'detail': hl,
                    'hwImplication': None,
                    'anxietyScript': None,
                    'date': rpt['date'],
                    'categories': tags,
                    'urgency': infer_urgency(hl, product),
                })
        for it in items:
            title = it.get('title', '')
            raw_vendor = it.get('vendor')
            vendor_str = vendor_to_str(raw_vendor)
            if vendor_str == 'AI热点' or vendor_str not in DAILY_VENDOR_BUCKETS:
                inferred = infer_vendor_from_text(title + ' ' + it.get('detail', it.get('summary', '')), report_vendors)
                # 若老格式本身是多个厂商联合项，保留联合展示；新格式回落项必须命中日报页分组。
                vendor_str = inferred if vendor_str == 'AI热点' else vendor_str
            product = it.get('product') or infer_product_from_text(title + ' ' + it.get('detail', it.get('summary', '')), it.get('dimension'))
            action_tag = urgency_to_action_tag(it.get('urgency', infer_urgency(title, product)), it.get('dimension') or product)
            fallback_action = build_action(vendor_str, title, product)
            if it.get('hwImplication') and it.get('anxietyScript'):
                action = f"{it['hwImplication']}\n\n销售话术：「{it['anxietyScript']}」"
            else:
                action = fallback_action
            tags = it.get('categories') or it.get('tags') or infer_tags(title + ' ' + it.get('detail', it.get('summary', '')), vendor=vendor_str, product=product, report=rpt)
            items_out.append({
                'id': item_id,
                'vendor': vendor_str,
                'product': product,
                'title': title,
                'summary': it.get('detail', it.get('summary', '')),
                'actionTag': action_tag,
                'action': action,
                'tags': tags,
                'date': it.get('date', rpt['date']),
            })
            item_id += 1

        # 把 comparisonTable 作为该日的特殊条目
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
            out.append(f'<h3>{html.escape(s[4:])}</h3>')
        elif s.startswith('## '):
            if in_ul: out.append('</ul>'); in_ul = False
            out.append(f'<h3>{html.escape(s[3:])}</h3>')
        elif s.startswith('- ') or s.startswith('* '):
            if not in_ul: out.append('<ul>'); in_ul = True
            out.append(f'<li>{html.escape(s[2:])}</li>')
        else:
            if in_ul: out.append('</ul>'); in_ul = False
            t = html.escape(s)
            t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
            out.append(f'<p>{t}</p>')
    if in_ul: out.append('</ul>')
    return '\n'.join(out)


def report_to_article(rpt):
    highlights = rpt.get('key_highlights', []) or rpt.get('highlights', [])
    text_blob = ' '.join([rpt.get('title', ''), rpt.get('summary', ''), ' '.join(highlights)])
    primary_vendor = infer_vendor_from_text(text_blob, rpt.get('vendors') or rpt.get('vendor_tags') or [])
    tags = infer_tags(text_blob, vendor=primary_vendor, product='产品/模型更新', report=rpt)
    date_compact = rpt['date'].replace('-', '')
    escaped_summary = html.escape(rpt.get('summary', ''))
    list_html = ''.join(f'<li>{html.escape(x)}</li>' for x in highlights)
    full_url = rpt.get('url', '')
    link_html = f'<p><a href="{html.escape(full_url)}" target="_blank" rel="noopener noreferrer">查看完整竞对日报</a></p>' if full_url else ''
    content = (
        f'<h3>日报摘要</h3><p>{escaped_summary}</p>'
        f'<h3>重点情报</h3><ul>{list_html}</ul>'
        f'<h3>销售使用建议</h3><p>建议围绕上述友商动态，结合浙江区域客户当前 AI 应用、算力成本和大模型选型节奏，优先识别价格敏感、行业标杆和国产化诉求明确的客户，形成可执行的拜访话术与迁移测算。</p>'
        f'{link_html}'
    )
    return {
        'id': f'report-{date_compact}',
        'title': rpt.get('title', f'{rpt["date"]} 竞对日报'),
        'summary': rpt.get('summary', ''),
        'tags': tags,
        'date': rpt['date'],
        'coverImage': rpt.get('coverImage', DEFAULT_COVER_IMAGE),
        'sections': [{
            'title': '正文',
            'content': content,
        }],
    }


def build_xr(articles, reports=None):
    """构造首页 Xr 数组。仅使用 hotspotArticles，避免日报条目覆盖深度文章。"""
    out = []
    if not articles:
        print('! data/reports.json 未找到 hotspotArticles，首页 Xr 将保持为空，避免用日报条目覆盖深度文章。', file=sys.stderr)
        return out
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
            'tags': art.get('categories', art.get('tags', [])),
            'date': art['date'],
            'coverImage': art.get('coverImage', DEFAULT_COVER_IMAGE),
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

    reports = data.get('dailyReports') or data.get('reports', [])
    if not reports:
        raise ValueError('data/reports.json 中未找到 dailyReports 或 reports 数据')

    us_arr = build_us(reports)
    xr_arr = build_xr(data.get('hotspotArticles', []), reports)

    us_js = to_js_literal(us_arr)
    xr_js = to_js_literal(xr_arr)

    with open(JS_PATH, 'r') as f:
        bundle = f.read()

    # 定位 us 和 Xr 的范围（每次都重新搜索，因为 bundle 可能变化）
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
    assert xr_start < us_start, "假设 Xr 在 us 前面，请检查"

    new_bundle = (
        bundle[:xr_start] + xr_js +
        bundle[xr_end + 1:us_start] + us_js +
        bundle[us_end + 1:]
    )

    # ===== 替换日报页硬编码的日期和核心研判 =====
    latest = sorted(reports, key=lambda r: r['date'], reverse=True)[0]
    y, m, d = latest['date'].split('-')
    new_date_label = f"{y}年{int(m)}月{int(d)}日"
    new_subtitle = f"{new_date_label} · 追踪阿里云、腾讯云、火山引擎及大模型厂商最新动态 · 每天 8:00 自动更新"
    new_insight = latest.get('coreInsight', latest.get('summary', ''))

    new_bundle = re.sub(
        r'\d{4}年\d{1,2}月\d{1,2}日 · 追踪阿里云、腾讯云、火山引擎及大模型厂商最新动态 · 每天 8:00 自动更新',
        new_subtitle,
        new_bundle
    )
    # 尝试替换“今日核心研判”固定内容。不同历史版本可能已被替换，故采用宽松匹配。
    new_bundle = re.sub(
        r'children:"[^"]{0,260}?(?:算力|DeepSeek|腾讯|阿里|火山|豆包|Kimi)[^"]{0,260}?"\}\)\]\}\),s\.map',
        lambda m: m.group(0).replace(re.search(r'children:"(.*?)"', m.group(0)).group(1), new_insight) if re.search(r'children:"(.*?)"', m.group(0)) else m.group(0),
        new_bundle,
        count=1
    )

    # GitHub Pages 部署基路径为 /aiintelhub/。wouter 的 Link 会自动叠加 base，
    # 因此首页 14 号 DRP/ERP 专题卡片的 href 需保持应用内路径 /drp-erp/，
    # 点击时再用 window.location.href 跳到真实静态专题页，避免渲染为 /aiintelhub/aiintelhub/drp-erp/。
    new_bundle = new_bundle.replace(
        'href:(String(n.id)==="14"?"/aiintelhub/drp-erp/":`/hotspot/${n.id}`)',
        'href:(String(n.id)==="14"?"/drp-erp/":`/hotspot/${n.id}`)'
    )

    with open(JS_PATH, 'w') as f:
        f.write(new_bundle)

    print(f"✓ 注入完成")
    print(f"  首页 Xr articles: {len(xr_arr)} 条")
    print(f"  日报 us items: {len(us_arr)} 条")
    print(f"  bundle 大小: {len(bundle)} → {len(new_bundle)} 字节")

    merge_extra_css()


if __name__ == '__main__':
    main()
