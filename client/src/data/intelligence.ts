// 情报站数据文件
// 设计主题：暗夜情报室 - 深海蓝黑底色 + 朱砂红警示色
// 数据从 reports.json 加载，方便 GitHub Actions 自动追加新一天的日报

import reportsData from './reports.json';

export type Vendor = 'aliyun' | 'tencent' | 'volcano' | 'ai-hotspot';
export type Dimension = 'price' | 'customer' | 'product' | 'strategy';
export type Category =
  | 'Agent框架'
  | '云厂商动态'
  | '企业数字化'
  | '信创'
  | '销售策略'
  | '竞争分析'
  | '行业趋势'
  | 'Token经济'
  | 'AI编码'
  | '大模型';

export interface NewsItem {
  id: number;
  date: string;
  vendor: Vendor[];
  dimension: Dimension;
  categories: Category[];
  title: string;
  summary: string;
  detail: string;
  hwImplication: string;
  anxietyScript: string;
  urgency: 'high' | 'medium' | 'low';
}

export interface ComparisonRow {
  dimension: string;
  aliyun: string;
  tencent: string;
  volcano: string;
  hwOpportunity: string;
}

export interface DailyReport {
  id: string;
  date: string;
  title: string;
  coreInsight: string;
  items: NewsItem[];
  comparisonTable: ComparisonRow[];
}

export interface HotspotArticle {
  id: number;
  date: string;
  categories: Category[];
  title: string;
  summary: string;
  content: string;
  readTime: number;
}

// 按日期倒序排列（最新的在前）
export const dailyReports: DailyReport[] = (reportsData.dailyReports as DailyReport[]).sort(
  (a, b) => b.date.localeCompare(a.date)
);

export const hotspotArticles: HotspotArticle[] = (reportsData.hotspotArticles as HotspotArticle[]).sort(
  (a, b) => b.date.localeCompare(a.date)
);

/**
 * 获取最新一份每日竞对日报（dailyReports 已按日期倒序排列）
 */
export function getLatestDailyReport(): DailyReport | undefined {
  return dailyReports[0];
}

/**
 * 按日期获取指定日报
 */
export function getDailyReportByDate(date: string): DailyReport | undefined {
  return dailyReports.find((r) => r.date === date);
}
