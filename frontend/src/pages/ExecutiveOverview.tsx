import React, { useEffect, useState } from 'react';
import {
  DollarSign,
  PieChart,
  ShoppingBag,
  Users,
  Percent,
  Sparkles,
  TrendingUp,
  Lightbulb
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar
} from 'recharts';

import { api } from '../services/api';
import { ExecutiveSummary, MonthlyTrend, RegionalMetric, CategoryMetric, BusinessRecommendation } from '../types';
import { KPICard } from '../components/KPICard';

const COLORS = ['#0ea5e9', '#6366f1', '#8b5cf6', '#ec4899', '#f59e0b'];

export const ExecutiveOverview: React.FC = () => {
  const [summary, setSummary] = useState<ExecutiveSummary | null>(null);
  const [monthlyTrends, setMonthlyTrends] = useState<MonthlyTrend[]>([]);
  const [regions, setRegions] = useState<RegionalMetric[]>([]);
  const [categories, setCategories] = useState<CategoryMetric[]>([]);
  const [recommendations, setRecommendations] = useState<BusinessRecommendation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [sumRes, trendsRes, regRes, catRes, recRes] = await Promise.all([
          api.getExecutiveSummary(),
          api.getSalesTrends(),
          api.getRegionalSales(),
          api.getCategorySales(),
          api.getRecommendations(),
        ]);
        setSummary(sumRes);
        setMonthlyTrends(trendsRes);
        setRegions(regRes);
        setCategories(catRes);
        setRecommendations(recRes);
      } catch (err) {
        console.error('Error fetching executive metrics:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading || !summary) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-sky-500/20 border-t-sky-500 rounded-full animate-spin"></div>
          <p className="text-sm text-gray-400 font-medium">Aggregating enterprise metrics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-12">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-sky-950/40 via-indigo-950/30 to-purple-950/30 border border-sky-500/20 rounded-2xl p-6">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-xs font-semibold text-sky-400 mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Executive Briefing</span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            Enterprise Performance Summary
          </h2>
          <p className="text-xs text-gray-300 max-w-2xl mt-1">
            RetailPulse AI data warehouse processed 57k+ transactions across 12,000 customers.
            Gross profit margin stands at <span className="text-emerald-400 font-semibold">{summary.overall_margin_pct}%</span> with strong regional contribution from West and East territories.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <div className="text-right">
            <p className="text-[11px] text-gray-400 uppercase font-semibold">Latest Month</p>
            <p className="text-sm font-bold text-white">{summary.latest_month}</p>
          </div>
          <div className="h-8 w-px bg-gray-800"></div>
          <div className="text-right">
            <p className="text-[11px] text-gray-400 uppercase font-semibold">MoM Growth</p>
            <p className={`text-sm font-bold ${summary.mom_revenue_growth_pct >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {summary.mom_revenue_growth_pct > 0 ? `+${summary.mom_revenue_growth_pct}%` : `${summary.mom_revenue_growth_pct}%`}
            </p>
          </div>
        </div>
      </div>

      {/* 6 Metric KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <KPICard
          title="Total Revenue"
          value={`$${(summary.total_revenue / 1e6).toFixed(2)}M`}
          subtitle={`$${summary.total_revenue.toLocaleString()}`}
          change={summary.mom_revenue_growth_pct}
          icon={DollarSign}
          color="sky"
        />
        <KPICard
          title="Gross Profit"
          value={`$${(summary.total_profit / 1e6).toFixed(2)}M`}
          subtitle={`$${summary.total_profit.toLocaleString()}`}
          change={summary.mom_profit_growth_pct}
          icon={TrendingUp}
          color="emerald"
        />
        <KPICard
          title="Profit Margin"
          value={`${summary.overall_margin_pct}%`}
          subtitle="Gross margin ratio"
          icon={Percent}
          color="indigo"
        />
        <KPICard
          title="Total Orders"
          value={summary.total_orders.toLocaleString()}
          subtitle="Completed transactions"
          icon={ShoppingBag}
          color="purple"
        />
        <KPICard
          title="Total Customers"
          value={summary.total_customers.toLocaleString()}
          subtitle={`${summary.active_customers.toLocaleString()} active buyers`}
          icon={Users}
          color="amber"
        />
        <KPICard
          title="Avg Order Value"
          value={`$${summary.average_order_value.toFixed(2)}`}
          subtitle="AOV across all channels"
          icon={PieChart}
          color="rose"
        />
      </div>

      {/* Main Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Revenue & Profit Area Chart */}
        <div className="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">
                Revenue & Profit Trajectory
              </h3>
              <p className="text-xs text-gray-400">Monthly historical revenue vs gross profit trend</p>
            </div>
            <div className="flex items-center gap-4 text-xs">
              <span className="flex items-center gap-1.5 text-sky-400 font-medium">
                <span className="w-2.5 h-2.5 rounded-full bg-sky-500"></span> Revenue
              </span>
              <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Profit
              </span>
            </div>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthlyTrends} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="colorProf" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="year_month" stroke="#6B7280" fontSize={11} tickLine={false} />
                <YAxis
                  stroke="#6B7280"
                  fontSize={11}
                  tickLine={false}
                  tickFormatter={(val) => `$${(val / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.75rem', fontSize: '12px' }}
                  formatter={(val: any) => [`$${Number(val).toLocaleString()}`, '']}
                />
                <Area type="monotone" dataKey="total_revenue" name="Revenue" stroke="#0ea5e9" strokeWidth={2} fillOpacity={1} fill="url(#colorRev)" />
                <Area type="monotone" dataKey="total_profit" name="Profit" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorProf)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Regional Performance Share */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">
              Regional Revenue Distribution
            </h3>
            <p className="text-xs text-gray-400 mb-6">Revenue share & margin by territory</p>

            <div className="space-y-4">
              {regions.map((reg, idx) => (
                <div key={reg.region} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-gray-200">{reg.region}</span>
                    <span className="text-gray-400">
                      ${(reg.total_revenue / 1e3).toFixed(1)}k ({reg.revenue_share_pct}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-800 rounded-full h-2 overflow-hidden flex">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${reg.revenue_share_pct}%`,
                        backgroundColor: COLORS[idx % COLORS.length]
                      }}
                    ></div>
                  </div>
                  <div className="flex justify-between text-[10px] text-gray-400">
                    <span>{reg.total_orders.toLocaleString()} orders</span>
                    <span className="text-emerald-400 font-medium">{reg.profit_margin_pct}% margin</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-gray-800 text-xs text-gray-400 flex items-center justify-between">
            <span>Leading Territory:</span>
            <span className="font-semibold text-sky-400">{regions[0]?.region} (${(regions[0]?.total_revenue / 1e6).toFixed(2)}M)</span>
          </div>
        </div>
      </div>

      {/* Category Performance & Prescriptive Recommendations Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Category Breakdown Bar Chart */}
        <div className="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">
                Category Revenue & Profit Breakdown
              </h3>
              <p className="text-xs text-gray-400">Sales volume and gross profitability per product category</p>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categories} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="category_name" stroke="#6B7280" fontSize={11} tickLine={false} />
                <YAxis
                  stroke="#6B7280"
                  fontSize={11}
                  tickLine={false}
                  tickFormatter={(val) => `$${(val / 1e6).toFixed(1)}M`}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.75rem', fontSize: '12px' }}
                  formatter={(val: any) => [`$${Number(val).toLocaleString()}`, '']}
                />
                <Bar dataKey="total_revenue" name="Revenue" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                <Bar dataKey="total_profit" name="Gross Profit" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Executive Action Directives */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-4 h-4 text-amber-400" />
            <h3 className="text-base font-bold text-white tracking-tight">
              Prescriptive Directives
            </h3>
          </div>
          <p className="text-xs text-gray-400 mb-4">Top data-grounded strategic recommendations</p>

          <div className="space-y-3">
            {recommendations.slice(0, 3).map((rec) => (
              <div key={rec.id} className="p-3.5 rounded-xl bg-gray-950/70 border border-gray-800 space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                    {rec.category}
                  </span>
                  <span className="text-[10px] font-semibold text-amber-400">
                    {rec.priority} Priority
                  </span>
                </div>
                <h4 className="text-xs font-bold text-gray-100">{rec.title}</h4>
                <p className="text-[11px] text-gray-400 line-clamp-2 leading-relaxed">{rec.recommended_action}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
