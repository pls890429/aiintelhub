// 暗夜情报室主题 - 首页
// 深海蓝黑底色 + 朱砂红警示色 + IBM Plex Sans技术感字体

import { useState } from "react";
import { Link } from "wouter";
import NavBar from "@/components/NavBar";
import { hotspotArticles, type Category } from "@/data/intelligence";
import { Calendar, Clock, ChevronRight, Radio, Zap } from "lucide-react";

const CATEGORIES: { label: string; value: Category | 'all' }[] = [
  { label: '全部', value: 'all' },
  { label: 'Agent框架', value: 'Agent框架' },
  { label: '云厂商动态', value: '云厂商动态' },
  { label: '企业数字化', value: '企业数字化' },
  { label: '信创', value: '信创' },
  { label: '销售策略', value: '销售策略' },
  { label: '竞争分析', value: '竞争分析' },
  { label: '行业趋势', value: '行业趋势' },
  { label: 'Token经济', value: 'Token经济' },
  { label: 'AI编码', value: 'AI编码' },
  { label: '大模型', value: '大模型' },
];

const CATEGORY_COLORS: Record<string, string> = {
  'Agent框架': 'bg-blue-900/40 text-blue-300 border border-blue-700/40',
  '云厂商动态': 'bg-orange-900/40 text-orange-300 border border-orange-700/40',
  '企业数字化': 'bg-teal-900/40 text-teal-300 border border-teal-700/40',
  '信创': 'bg-purple-900/40 text-purple-300 border border-purple-700/40',
  '销售策略': 'bg-green-900/40 text-green-300 border border-green-700/40',
  '竞争分析': 'bg-red-900/40 text-red-300 border border-red-700/40',
  '行业趋势': 'bg-yellow-900/40 text-yellow-300 border border-yellow-700/40',
  'Token经济': 'bg-pink-900/40 text-pink-300 border border-pink-700/40',
  'AI编码': 'bg-cyan-900/40 text-cyan-300 border border-cyan-700/40',
  '大模型': 'bg-indigo-900/40 text-indigo-300 border border-indigo-700/40',
};

export default function Home() {
  const [activeCategory, setActiveCategory] = useState<Category | 'all'>('all');

  const filtered = activeCategory === 'all'
    ? hotspotArticles
    : hotspotArticles.filter(a => a.categories.includes(activeCategory));

  return (
    <div className="min-h-screen bg-[#0A0E1A]">
      <NavBar />

      {/* Hero Section */}
      <div className="relative overflow-hidden border-b border-[#1e2d45]">
        <div className="absolute inset-0 bg-gradient-to-br from-[#0d1220] via-[#0A0E1A] to-[#0d1a2e]" />
        {/* 网格背景 */}
        <div className="absolute inset-0 opacity-5"
          style={{
            backgroundImage: 'linear-gradient(#E63946 1px, transparent 1px), linear-gradient(90deg, #E63946 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
        <div className="relative container py-12 lg:py-16">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
            <div className="max-w-2xl">
              <div className="flex items-center gap-2 mb-4">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#E63946]/15 border border-[#E63946]/30 text-[#E63946] text-xs font-medium">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E63946] animate-pulse" />
                  INTELLIGENCE HUB
                </span>
              </div>
              <h1 className="text-3xl lg:text-4xl font-bold text-[#E8EDF5] font-['Noto_Serif_SC'] leading-tight mb-3">
                AI热点云厂商机会方案分析
              </h1>
              <p className="text-[#8892A4] text-sm lg:text-base leading-relaxed">
                追踪AI行业热点，洞察云厂商竞争格局，分析机会与方案
              </p>
              <div className="mt-4 flex items-center gap-4 text-xs text-[#8892A4]">
                <span className="flex items-center gap-1">
                  <Zap className="w-3.5 h-3.5 text-[#F4A261]" />
                  已收录 {hotspotArticles.length} 条热点情报
                </span>
              </div>
            </div>

            {/* 日报入口卡片 */}
            <Link href="/daily-report">
              <div className="intel-card p-5 lg:w-72 cursor-pointer group border-[#E63946]/20 hover:border-[#E63946]/40">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-lg bg-[#E63946]/15 flex items-center justify-center flex-shrink-0">
                    <Radio className="w-5 h-5 text-[#E63946]" />
                  </div>
                  <div>
                    <div className="font-semibold text-[#E8EDF5] text-sm mb-0.5">每日竞对日报</div>
                    <div className="text-[10px] text-[#8892A4] mb-2">每天 8:00 自动更新</div>
                    <p className="text-xs text-[#8892A4] leading-relaxed">
                      追踪阿里云、腾讯云、火山引擎等友商最新动态，助力销售团队知己知彼。
                    </p>
                  </div>
                </div>
                <div className="mt-4 flex items-center gap-1 text-[#E63946] text-xs font-medium group-hover:gap-2 transition-all">
                  查看日报 <ChevronRight className="w-3.5 h-3.5" />
                </div>
              </div>
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container py-8">
        {/* Category Filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          {CATEGORIES.map(cat => (
            <button
              key={cat.value}
              onClick={() => setActiveCategory(cat.value)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                activeCategory === cat.value
                  ? 'bg-[#E63946] text-white'
                  : 'bg-[#1e2d45] text-[#8892A4] hover:text-[#E8EDF5] hover:bg-[#2d4a6e]'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Articles Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((article, idx) => (
            <Link key={article.id} href={`/article/${article.id}`}>
              <div
                className="intel-card p-5 h-full flex flex-col cursor-pointer animate-fade-in-up"
                style={{ animationDelay: `${idx * 60}ms` }}
              >
                {/* Date badge */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-1.5 text-[#8892A4] text-xs">
                    <Calendar className="w-3 h-3" />
                    <span className="font-mono">{article.date.split('-').slice(1).join('.')} 2026</span>
                  </div>
                  <div className="w-8 h-8 rounded bg-[#1e2d45] flex items-center justify-center">
                    <span className="text-xs font-bold text-[#E63946] font-mono">{article.id}</span>
                  </div>
                </div>

                {/* Categories */}
                <div className="flex flex-wrap gap-1.5 mb-3">
                  {article.categories.map(cat => (
                    <span key={cat} className={`text-[10px] px-2 py-0.5 rounded-full ${CATEGORY_COLORS[cat] || 'bg-[#1e2d45] text-[#8892A4]'}`}>
                      {cat}
                    </span>
                  ))}
                </div>

                {/* Title */}
                <h3 className="text-sm font-semibold text-[#E8EDF5] font-['Noto_Serif_SC'] leading-snug mb-2 flex-1">
                  {article.title}
                </h3>

                {/* Summary */}
                <p className="text-xs text-[#8892A4] leading-relaxed line-clamp-3 mb-4">
                  {article.summary}
                </p>

                {/* Footer */}
                <div className="flex items-center justify-between mt-auto pt-3 border-t border-[#1e2d45]">
                  <div className="flex items-center gap-1 text-[#8892A4] text-xs">
                    <Clock className="w-3 h-3" />
                    <span>{article.readTime} 分钟阅读</span>
                  </div>
                  <span className="text-[#E63946] text-xs flex items-center gap-0.5 font-medium">
                    阅读详情 <ChevronRight className="w-3 h-3" />
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-16 text-[#8892A4]">
            <p className="text-sm">暂无该分类的情报内容</p>
          </div>
        )}
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
