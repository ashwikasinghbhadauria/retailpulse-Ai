import React, { useEffect, useState } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';

import { api } from '../services/api';
import { MonthlyTrend, RegionalMetric, CategoryMetric } from '../types';

export const SalesAnalytics: React.FC = () => {
  const [trends, setTrends] = useState<MonthlyTrend[]>([]);
  const [regions, setRegions] = useState<RegionalMetric[]>([]);
  const [categories, setCategories] = useState<CategoryMetric[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [trendsData, regData, catData] = await Promise.all([
          api.getSalesTrends(),
          api.getRegionalSales(),
          api.getCategorySales(),
        ]);
        setTrends(trendsData);
        setRegions(regData);
        setCategories(catData);
      } catch (err) {
        console.error('Failed to load sales analytics:', err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-sky-500/20 border-t-sky-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  const filteredTrends = trends.filter(t => t.year_month.includes(searchTerm));

  return (
    <div className="space-y-8 pb-12">
      {/* Header & Filter Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <div>
          <h2 className="text-lg font-bold text-white tracking-tight">
            Sales & Revenue Analytics
          </h2>
          <p className="text-xs text-gray-400">
            Deep-dive time-series trends, MoM growth rates, and category dynamics
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <input
              type="text"
              placeholder="Filter by Year/Month (e.g. 2025)..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="px-3.5 py-2 bg-gray-950 border border-gray-800 rounded-xl text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-sky-500 w-64"
            />
          </div>
        </div>
      </div>

      {/* Main MoM Growth & Revenue Line Chart */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">
              Monthly Revenue Trajectory & MoM Growth Rate
            </h3>
            <p className="text-xs text-gray-400">
              Total monthly gross revenue vs month-over-month percentage growth
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs font-medium">
            <span className="flex items-center gap-1.5 text-sky-400">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-500"></span> Monthly Revenue
            </span>
            <span className="flex items-center gap-1.5 text-emerald-400">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> MoM Growth %
            </span>
          </div>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={filteredTrends} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
              <XAxis dataKey="year_month" stroke="#6B7280" fontSize={11} tickLine={false} />
              <YAxis
                yAxisId="left"
                stroke="#6B7280"
                fontSize={11}
                tickLine={false}
                tickFormatter={(val) => `$${(val / 1000).toFixed(0)}k`}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                stroke="#6B7280"
                fontSize={11}
                tickLine={false}
                tickFormatter={(val) => `${val}%`}
              />
              <Tooltip
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.75rem', fontSize: '12px' }}
                formatter={(val: any, name: any) => [
                  name === 'MoM Growth' ? `${val}%` : `$${Number(val).toLocaleString()}`,
                  name
                ]}
              />
              <Line yAxisId="left" type="monotone" dataKey="total_revenue" name="Revenue" stroke="#0ea5e9" strokeWidth={2.5} dot={{ r: 3 }} />
              <Line yAxisId="right" type="monotone" dataKey="mom_revenue_growth_pct" name="MoM Growth" stroke="#10b981" strokeWidth={2} strokeDasharray="4 4" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Regional & Category Detailed Comparisons */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Regional Breakdown Table */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <h3 className="text-base font-bold text-white tracking-tight mb-1">
            Regional Sales Breakdown
          </h3>
          <p className="text-xs text-gray-400 mb-4">Volume, revenue share, and average order values by territory</p>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-gray-400 uppercase text-[10px] tracking-wider border-b border-gray-800 bg-gray-950/50">
                <tr>
                  <th className="py-3 px-3">Region</th>
                  <th className="py-3 px-3">Orders</th>
                  <th className="py-3 px-3">Revenue</th>
                  <th className="py-3 px-3">Profit Margin</th>
                  <th className="py-3 px-3">AOV</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60 font-medium">
                {regions.map((reg) => (
                  <tr key={reg.region} className="hover:bg-gray-800/40 transition">
                    <td className="py-3 px-3 font-semibold text-white">{reg.region}</td>
                    <td className="py-3 px-3 text-gray-300">{reg.total_orders.toLocaleString()}</td>
                    <td className="py-3 px-3 text-sky-400">${reg.total_revenue.toLocaleString()}</td>
                    <td className="py-3 px-3 text-emerald-400">{reg.profit_margin_pct}%</td>
                    <td className="py-3 px-3 text-gray-300">${reg.average_order_value.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Category Discount & Volume Matrix */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <h3 className="text-base font-bold text-white tracking-tight mb-1">
            Category Discount & Margin Matrix
          </h3>
          <p className="text-xs text-gray-400 mb-4">Assessing discounting impact on gross profit margins</p>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-gray-400 uppercase text-[10px] tracking-wider border-b border-gray-800 bg-gray-950/50">
                <tr>
                  <th className="py-3 px-3">Category</th>
                  <th className="py-3 px-3">Products</th>
                  <th className="py-3 px-3">Revenue</th>
                  <th className="py-3 px-3">Avg Discount</th>
                  <th className="py-3 px-3">Margin %</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60 font-medium">
                {categories.map((cat) => (
                  <tr key={cat.category_id} className="hover:bg-gray-800/40 transition">
                    <td className="py-3 px-3 font-semibold text-white">{cat.category_name}</td>
                    <td className="py-3 px-3 text-gray-300">{cat.product_count}</td>
                    <td className="py-3 px-3 text-sky-400">${cat.total_revenue.toLocaleString()}</td>
                    <td className="py-3 px-3 text-amber-400">{cat.avg_discount_pct}%</td>
                    <td className="py-3 px-3 text-emerald-400">{cat.profit_margin_pct}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Monthly Granular Historical Data Table */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">
              Historical Monthly Performance Ledger
            </h3>
            <p className="text-xs text-gray-400">Complete month-by-month financial ledger</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-gray-400 uppercase text-[10px] tracking-wider border-b border-gray-800 bg-gray-950/50">
              <tr>
                <th className="py-3 px-3">Month</th>
                <th className="py-3 px-3">Orders</th>
                <th className="py-3 px-3">Units Sold</th>
                <th className="py-3 px-3">Revenue</th>
                <th className="py-3 px-3">Gross Profit</th>
                <th className="py-3 px-3">Margin %</th>
                <th className="py-3 px-3">MoM Growth</th>
                <th className="py-3 px-3">AOV</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60 font-medium">
              {filteredTrends.map((row) => (
                <tr key={row.year_month} className="hover:bg-gray-800/40 transition">
                  <td className="py-2.5 px-3 font-semibold text-white">{row.year_month}</td>
                  <td className="py-2.5 px-3 text-gray-300">{row.total_orders.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-gray-300">{row.total_units_sold.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-sky-400">${row.total_revenue.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-emerald-400">${row.total_profit.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-gray-300">{row.profit_margin_pct}%</td>
                  <td className="py-2.5 px-3">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                      row.mom_revenue_growth_pct >= 0 ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                    }`}>
                      {row.mom_revenue_growth_pct > 0 ? `+${row.mom_revenue_growth_pct}%` : `${row.mom_revenue_growth_pct}%`}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-gray-300">${row.average_order_value.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
