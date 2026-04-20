// 暗夜情报室主题 - 每日竞对日报页面
// 深海蓝黑底色 + 朱砂红警示色

import { useState } from "react";
import NavBar from "@/components/NavBar";
import { getLatestDailyReport, type Dimension } from "@/data/intelligence";
import { AlertTriangle, Users, Package, TrendingUp, ChevronDown, ChevronUp, Zap, Target } from "lucide-react";

const DIMENSIONS: { label: string; value: Dimension | 'all'; icon: React.ReactNode; color: string }[] = [
  { label: '全部', value: 'all', icon: <Zap className="w-3.5 h-3.5" />, color: 'text-[#E8EDF5]' },
  { label: '价格动作', value: 'price', icon: <AlertTriangle className="w-3.5 h-3.5" />, color: 'text-[#F4A261]' },
  { label: '客户案例', value: 'customer', icon: <Users className="w-3.5 h-3.5" />, color: 'text-[#2A9D8F]' },
  { label: '产品/模型更新', value: 'product', icon: <Package className="w-3.5 h-3.5" />, color: 'text-[#457B9D]' },
  { label: '组织与战略', value: 'strategy', icon: <TrendingUp className="w-3.5 h-3.5" />, color: 'text-[#E63946]' },
];

const VENDOR_LABELS: Record<string, { label: string; className: string }> = {
  aliyun: { label: '阿里云', className: 'vendor-ali' },
  tencent: { label: '腾讯云', className: 'vendor-tencent' },
  volcano: { label: '火山引擎', className: 'vendor-volcano' },
  'ai-hotspot': { label: 'AI热点', className: 'bg-purple-900/40 text-purple-300 border border-purple-700/40' },
};

const URGENCY_CONFIG = {
  high: { label: '⚡ 高优先级', className: 'bg-[#E63946]/15 text-[#E63946] border border-[#E63946]/30' },
  medium: { label: '● 中优先级', className: 'bg-[#F4A261]/15 text-[#F4A261] border border-[#F4A261]/30' },
  low: { label: '○ 低优先级', className: 'bg-[#8892A4]/15 text-[#8892A4] border border-[#8892A4]/30' },
};

const DIM_COLORS: Record<Dimension, string> = {
  price: 'dim-price',
  customer: 'dim-customer',
  product: 'dim-product',
  strategy: 'dim-strategy',
};

export default function DailyReport() {
  const report = getLatestDailyReport();
  const [activeDim, setActiveDim] = useState<Dimension | 'all'>('all');
  const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set());
  const [showTable, setShowTable] = useState(true);

  const toggleItem = (id: number) => {
    setExpandedItems(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const filtered = activeDim === 'all'
    ? report.items
    : report.items.filter(item => item.dimension === activeDim);

  return (
    <div className="min-h-screen bg-[#0A0E1A]">
      <NavBar />

      {/* Report Header */}
      <div className="border-b border-[#1e2d45] bg-[#0d1220]">
        <div className="container py-6">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-lg bg-[#E63946]/15 flex items-center justify-center flex-shrink-0 mt-0.5">
              <Target className="w-5 h-5 text-[#E63946]" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs text-[#8892A4] font-mono">{report.date}</span>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-[#E63946]/15 border border-[#E63946]/30 text-[#E63946] text-[10px]">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E63946] animate-pulse" />
                  最新日报
                </span>
              </div>
              <h1 className="text-xl lg:text-2xl font-bold text-[#E8EDF5] font-['Noto_Serif_SC'] mb-2">
                🦞 浙江云嗷嗷叫 · Manus竞对日报 · {report.date}
              </h1>
              <p className="text-sm text-[#8892A4] leading-relaxed max-w-3xl">
                <span className="text-[#F4A261] font-medium">核心研判：</span>{report.coreInsight}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="container py-6">
        {/* Dimension Filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          {DIMENSIONS.map(dim => (
            <button
              key={dim.value}
              onClick={() => setActiveDim(dim.value)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                activeDim === dim.value
                  ? 'bg-[#E63946] text-white'
                  : 'bg-[#1e2d45] text-[#8892A4] hover:text-[#E8EDF5] hover:bg-[#2d4a6e]'
              }`}
            >
              <span className={activeDim === dim.value ? 'text-white' : dim.color}>{dim.icon}</span>
              {dim.label}
            </button>
          ))}
        </div>

        {/* News Items */}
        <div className="space-y-3 mb-8">
          {filtered.map((item, idx) => (
            <div
              key={item.id}
              className="intel-card overflow-hidden animate-fade-in-up"
              style={{ animationDelay: `${idx * 60}ms` }}
            >
              {/* Card Header */}
              <div
                className="p-4 cursor-pointer"
                onClick={() => toggleItem(item.id)}
              >
                <div className="flex items-start gap-3">
                  <div className="flex-1 min-w-0">
                    {/* Meta row */}
                    <div className="flex flex-wrap items-center gap-2 mb-2">
                      {/* Vendors */}
                      {item.vendor.map(v => (
                        <span key={v} className={`text-[10px] px-2 py-0.5 rounded-full ${VENDOR_LABELS[v]?.className}`}>
                          {VENDOR_LABELS[v]?.label}
                        </span>
                      ))}
                      {/* Dimension */}
                      <span className={`text-[10px] px-2 py-0.5 rounded-full ${DIM_COLORS[item.dimension]}`}>
                        {DIMENSIONS.find(d => d.value === item.dimension)?.label}
                      </span>
                      {/* Urgency */}
                      <span className={`text-[10px] px-2 py-0.5 rounded-full ${URGENCY_CONFIG[item.urgency].className}`}>
                        {URGENCY_CONFIG[item.urgency].label}
                      </span>
                    </div>

                    {/* Title */}
                    <h3 className="text-sm font-semibold text-[#E8EDF5] font-['Noto_Serif_SC'] leading-snug mb-1">
                      {item.title}
                    </h3>
                    <p className="text-xs text-[#8892A4] leading-relaxed line-clamp-2">
                      {item.summary}
                    </p>
                  </div>

                  {/* Expand toggle */}
                  <div className="flex-shrink-0 w-6 h-6 rounded bg-[#1e2d45] flex items-center justify-center mt-0.5">
                    {expandedItems.has(item.id)
                      ? <ChevronUp className="w-3.5 h-3.5 text-[#8892A4]" />
                      : <ChevronDown className="w-3.5 h-3.5 text-[#8892A4]" />
                    }
                  </div>
                </div>
              </div>

              {/* Expanded Content */}
              {expandedItems.has(item.id) && (
                <div className="border-t border-[#1e2d45] px-4 pb-4 pt-3 space-y-4">
                  {/* Detail */}
                  <div>
                    <h4 className="text-xs font-semibold text-[#8892A4] uppercase tracking-wider mb-2">事件详情</h4>
                    <p className="text-xs text-[#C5CDD8] leading-relaxed">{item.detail}</p>
                  </div>

                  {/* HW Implication */}
                  <div className="rounded-lg bg-[#2A9D8F]/10 border border-[#2A9D8F]/20 p-3">
                    <h4 className="text-xs font-semibold text-[#2A9D8F] mb-1.5 flex items-center gap-1.5">
                      <Target className="w-3.5 h-3.5" />
                      对华为云浙江区域的含义
                    </h4>
                    <p className="text-xs text-[#C5CDD8] leading-relaxed">{item.hwImplication}</p>
                  </div>

                  {/* Anxiety Script */}
                  <div className="rounded-lg bg-[#E63946]/10 border border-[#E63946]/20 p-3">
                    <h4 className="text-xs font-semibold text-[#E63946] mb-1.5 flex items-center gap-1.5">
                      <Zap className="w-3.5 h-3.5" />
                      建联焦虑话术（可直接使用）
                    </h4>
                    <p className="text-xs text-[#E8EDF5] leading-relaxed italic">
                      "{item.anxietyScript}"
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Comparison Table */}
        <div className="intel-card overflow-hidden">
          <button
            className="w-full flex items-center justify-between p-4 text-left"
            onClick={() => setShowTable(v => !v)}
          >
            <h2 className="text-sm font-bold text-[#E8EDF5] font-['Noto_Serif_SC'] flex items-center gap-2">
              <span className="w-1 h-4 bg-[#E63946] rounded-full inline-block" />
              三家动作对比表 · {report.date}
            </h2>
            {showTable
              ? <ChevronUp className="w-4 h-4 text-[#8892A4]" />
              : <ChevronDown className="w-4 h-4 text-[#8892A4]" />
            }
          </button>

          {showTable && (
            <div className="overflow-x-auto border-t border-[#1e2d45]">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-[#1e2d45] bg-[#0d1220]">
                    <th className="text-left px-4 py-3 text-[#8892A4] font-medium w-28">维度</th>
                    <th className="text-left px-4 py-3 font-medium" style={{ color: '#FF6A00' }}>阿里云</th>
                    <th className="text-left px-4 py-3 font-medium" style={{ color: '#4d8ef5' }}>腾讯云</th>
                    <th className="text-left px-4 py-3 font-medium" style={{ color: '#ff6b63' }}>火山引擎</th>
                    <th className="text-left px-4 py-3 text-[#2A9D8F] font-medium">华为云机会</th>
                  </tr>
                </thead>
                <tbody>
                  {report.comparisonTable.map((row, idx) => (
                    <tr key={idx} className="border-b border-[#1e2d45] hover:bg-[#1a2235] transition-colors">
                      <td className="px-4 py-3 font-medium text-[#E8EDF5] whitespace-nowrap">{row.dimension}</td>
                      <td className="px-4 py-3 text-[#C5CDD8] leading-relaxed">{row.aliyun}</td>
                      <td className="px-4 py-3 text-[#C5CDD8] leading-relaxed">{row.tencent}</td>
                      <td className="px-4 py-3 text-[#C5CDD8] leading-relaxed">{row.volcano}</td>
                      <td className="px-4 py-3 text-[#2A9D8F] leading-relaxed">{row.hwOpportunity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-[#1e2d45] mt-8 py-6">
        <div className="container text-center text-xs text-[#8892A4]">
          华为云AI热点情报站 · 浙江区域销售专用 · 仅供内部参考
        </div>
      </footer>
    </div>
  );
}
