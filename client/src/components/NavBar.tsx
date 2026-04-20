// 暗夜情报室主题导航栏
// 深海蓝黑底色 + 朱砂红警示色

import { Link, useLocation } from "wouter";
import { Shield, Radio, Home, MessageSquare } from "lucide-react";

export default function NavBar() {
  const [location] = useLocation();

  return (
    <nav className="sticky top-0 z-50 border-b border-[#1e2d45] bg-[#0d1220]/95 backdrop-blur-sm">
      <div className="container flex items-center justify-between h-14">
        {/* Logo */}
        <Link href="/">
          <div className="flex items-center gap-2 group">
            <div className="w-7 h-7 rounded bg-[#E63946] flex items-center justify-center">
              <Shield className="w-4 h-4 text-white" />
            </div>
            <div>
              <span className="font-bold text-sm text-[#E8EDF5] font-['Noto_Serif_SC']">AI热点情报站</span>
              <span className="ml-2 text-[10px] text-[#8892A4] hidden sm:inline">云厂商竞争情报 · 持续更新</span>
            </div>
          </div>
        </Link>

        {/* Nav Links */}
        <div className="flex items-center gap-1">
          <Link href="/">
            <button className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium transition-colors ${
              location === '/' 
                ? 'bg-[#1e2d45] text-[#E8EDF5]' 
                : 'text-[#8892A4] hover:text-[#E8EDF5] hover:bg-[#1a2235]'
            }`}>
              <Home className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">情报首页</span>
            </button>
          </Link>
          <Link href="/daily-report">
            <button className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium transition-colors ${
              location === '/daily-report' 
                ? 'bg-[#1e2d45] text-[#E8EDF5]' 
                : 'text-[#8892A4] hover:text-[#E8EDF5] hover:bg-[#1a2235]'
            }`}>
              <Radio className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">竞对日报</span>
            </button>
          </Link>
          <a href="mailto:281481047@qq.com" className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium text-[#8892A4] hover:text-[#E8EDF5] hover:bg-[#1a2235] transition-colors">
            <MessageSquare className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">反馈建议</span>
          </a>
        </div>
      </div>
    </nav>
  );
}
