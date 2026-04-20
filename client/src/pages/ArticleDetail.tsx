// 暗夜情报室主题 - 文章详情页面
// 深海蓝黑底色 + 朱砂红警示色

import { useParams, Link } from "wouter";
import NavBar from "@/components/NavBar";
import { hotspotArticles } from "@/data/intelligence";
import { Calendar, Clock, ChevronLeft, ChevronRight } from "lucide-react";

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

function renderContent(content: string) {
  const lines = content.split('\n');
  const elements: React.ReactNode[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith('## ')) {
      elements.push(
        <h2 key={i} className="text-lg font-bold text-[#E8EDF5] font-['Noto_Serif_SC'] mt-6 mb-3 pb-2 border-b border-[#1e2d45]">
          {line.slice(3)}
        </h2>
      );
    } else if (line.startsWith('### ')) {
      elements.push(
        <h3 key={i} className="text-sm font-bold text-[#E8EDF5] font-['Noto_Serif_SC'] mt-4 mb-2 flex items-center gap-2">
          <span className="w-1 h-3.5 bg-[#E63946] rounded-full inline-block" />
          {line.slice(4)}
        </h3>
      );
    } else if (line.startsWith('**') && line.endsWith('**')) {
      elements.push(
        <p key={i} className="text-sm font-semibold text-[#F4A261] mb-2">{line.slice(2, -2)}</p>
      );
    } else if (line.trim() === '') {
      elements.push(<div key={i} className="h-2" />);
    } else {
      // Process inline bold
      const parts = line.split(/(\*\*[^*]+\*\*)/g);
      const rendered = parts.map((part, j) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={j} className="text-[#E8EDF5] font-semibold">{part.slice(2, -2)}</strong>;
        }
        return part;
      });
      elements.push(
        <p key={i} className="text-sm text-[#C5CDD8] leading-relaxed mb-2">{rendered}</p>
      );
    }
    i++;
  }
  return elements;
}

export default function ArticleDetail() {
  const { id } = useParams<{ id: string }>();
  const article = hotspotArticles.find(a => a.id === parseInt(id || '0'));

  if (!article) {
    return (
      <div className="min-h-screen bg-[#0A0E1A]">
        <NavBar />
        <div className="container py-16 text-center">
          <p className="text-[#8892A4]">文章不存在</p>
          <Link href="/">
            <button className="mt-4 text-[#E63946] text-sm flex items-center gap-1 mx-auto">
              <ChevronLeft className="w-4 h-4" /> 返回首页
            </button>
          </Link>
        </div>
      </div>
    );
  }

  const currentIdx = hotspotArticles.findIndex(a => a.id === article.id);
  const prevArticle = currentIdx < hotspotArticles.length - 1 ? hotspotArticles[currentIdx + 1] : null;
  const nextArticle = currentIdx > 0 ? hotspotArticles[currentIdx - 1] : null;

  return (
    <div className="min-h-screen bg-[#0A0E1A]">
      <NavBar />

      <div className="container py-6 max-w-3xl">
        {/* Back button */}
        <Link href="/">
          <button className="flex items-center gap-1 text-[#8892A4] hover:text-[#E8EDF5] text-xs mb-6 transition-colors">
            <ChevronLeft className="w-3.5 h-3.5" /> 返回情报首页
          </button>
        </Link>

        {/* Article Header */}
        <div className="intel-card p-6 mb-6">
          {/* Meta */}
          <div className="flex flex-wrap items-center gap-3 mb-4">
            <div className="flex items-center gap-1.5 text-[#8892A4] text-xs">
              <Calendar className="w-3 h-3" />
              <span className="font-mono">{article.date}</span>
            </div>
            <div className="flex items-center gap-1.5 text-[#8892A4] text-xs">
              <Clock className="w-3 h-3" />
              <span>{article.readTime} 分钟阅读</span>
            </div>
          </div>

          {/* Categories */}
          <div className="flex flex-wrap gap-1.5 mb-4">
            {article.categories.map(cat => (
              <span key={cat} className={`text-[10px] px-2 py-0.5 rounded-full ${CATEGORY_COLORS[cat] || 'bg-[#1e2d45] text-[#8892A4]'}`}>
                {cat}
              </span>
            ))}
          </div>

          {/* Title */}
          <h1 className="text-xl lg:text-2xl font-bold text-[#E8EDF5] font-['Noto_Serif_SC'] leading-tight mb-4">
            {article.title}
          </h1>

          {/* Summary */}
          <div className="rounded-lg bg-[#1e2d45] p-3 border-l-2 border-[#E63946]">
            <p className="text-sm text-[#C5CDD8] leading-relaxed">{article.summary}</p>
          </div>
        </div>

        {/* Article Content */}
        <div className="intel-card p-6 mb-6">
          {renderContent(article.content)}
        </div>

        {/* Navigation */}
        <div className="grid grid-cols-2 gap-3">
          {prevArticle ? (
            <Link href={`/article/${prevArticle.id}`}>
              <div className="intel-card p-4 cursor-pointer">
                <div className="text-[10px] text-[#8892A4] mb-1 flex items-center gap-1">
                  <ChevronLeft className="w-3 h-3" /> 上一篇
                </div>
                <p className="text-xs text-[#E8EDF5] line-clamp-2 font-['Noto_Serif_SC']">{prevArticle.title}</p>
              </div>
            </Link>
          ) : <div />}

          {nextArticle ? (
            <Link href={`/article/${nextArticle.id}`}>
              <div className="intel-card p-4 cursor-pointer text-right">
                <div className="text-[10px] text-[#8892A4] mb-1 flex items-center gap-1 justify-end">
                  下一篇 <ChevronRight className="w-3 h-3" />
                </div>
                <p className="text-xs text-[#E8EDF5] line-clamp-2 font-['Noto_Serif_SC']">{nextArticle.title}</p>
              </div>
            </Link>
          ) : <div />}
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
