import React, { useEffect, useState } from 'react';
import {
  Package,
  AlertOctagon
} from 'lucide-react';

import { api } from '../services/api';
import { ProductMetric } from '../types';

export const ProductIntelligence: React.FC = () => {
  const [topProducts, setTopProducts] = useState<ProductMetric[]>([]);
  const [underperforming, setUnderperforming] = useState<ProductMetric[]>([]);
  const [sortBy, setSortBy] = useState<string>('revenue');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        setLoading(true);
        const [topRes, underRes] = await Promise.all([
          api.getTopProducts(12, sortBy),
          api.getUnderperformingProducts(8),
        ]);
        setTopProducts(topRes);
        setUnderperforming(underRes);
      } catch (err) {
        console.error('Failed to load product analytics:', err);
      } finally {
        setLoading(false);
      }
    };
    loadProducts();
  }, [sortBy]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-sky-500/20 border-t-sky-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-12">
      {/* Header Banner */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-xs font-semibold text-sky-400 mb-2">
            <Package className="w-3.5 h-3.5" />
            <span>Merchandising & Profitability Matrix</span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            Product Performance & Assortment Analytics
          </h2>
          <p className="text-xs text-gray-400 max-w-2xl mt-1">
            Analyze SKU-level profitability, unit margins, and discount drag across all 125 catalog items.
          </p>
        </div>

        {/* Sort Controls */}
        <div className="flex items-center gap-2 bg-gray-950 p-1 rounded-xl border border-gray-800 text-xs">
          <button
            onClick={() => setSortBy('revenue')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition ${
              sortBy === 'revenue' ? 'bg-sky-500 text-white' : 'text-gray-400 hover:text-white'
            }`}
          >
            By Revenue
          </button>
          <button
            onClick={() => setSortBy('profit')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition ${
              sortBy === 'profit' ? 'bg-sky-500 text-white' : 'text-gray-400 hover:text-white'
            }`}
          >
            By Profit
          </button>
          <button
            onClick={() => setSortBy('units')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition ${
              sortBy === 'units' ? 'bg-sky-500 text-white' : 'text-gray-400 hover:text-white'
            }`}
          >
            By Units
          </button>
        </div>
      </div>

      {/* Top 12 Product Cards Grid */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider">
            Top Performing SKUs ({sortBy.toUpperCase()})
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {topProducts.map((p, idx) => (
            <div
              key={p.product_id}
              className="bg-gray-900 border border-gray-800 rounded-2xl p-5 hover:border-gray-700 transition space-y-3"
            >
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                    {p.category_name}
                  </span>
                  <h4 className="text-sm font-bold text-white line-clamp-1">{p.product_name}</h4>
                  <p className="text-xs text-gray-400 font-mono">{p.product_id}</p>
                </div>
                <span className="text-sm font-bold text-gray-400">#{idx + 1}</span>
              </div>

              <div className="pt-3 border-t border-gray-800/80 grid grid-cols-2 gap-2 text-xs">
                <div>
                  <p className="text-gray-400">Total Revenue</p>
                  <p className="font-bold text-sky-400">${p.total_revenue.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-gray-400">Gross Profit</p>
                  <p className="font-bold text-emerald-400">${p.total_profit.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-gray-400">Profit Margin</p>
                  <p className="font-semibold text-white">{p.gross_margin_pct}%</p>
                </div>
                <div>
                  <p className="text-gray-400">Units Sold</p>
                  <p className="font-semibold text-gray-300">{p.total_units_sold.toLocaleString()} pcs</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Underperforming Products & Margin Erosion Table */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <div className="flex items-center gap-2 mb-2 text-amber-400">
          <AlertOctagon className="w-5 h-5" />
          <h3 className="text-base font-bold text-white tracking-tight">
            Underperforming SKUs & Margin Erosion Watchlist
          </h3>
        </div>
        <p className="text-xs text-gray-400 mb-4">
          Items with below-average gross profit margins or high promotional discount rates requiring price rationalization
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-gray-400 uppercase text-[10px] tracking-wider border-b border-gray-800 bg-gray-950/50">
              <tr>
                <th className="py-3 px-3">Product ID</th>
                <th className="py-3 px-3">Product Name</th>
                <th className="py-3 px-3">Category</th>
                <th className="py-3 px-3">Unit Price</th>
                <th className="py-3 px-3">Revenue</th>
                <th className="py-3 px-3">Gross Margin</th>
                <th className="py-3 px-3">Avg Discount</th>
                <th className="py-3 px-3">Risk Assessment</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60 font-medium">
              {underperforming.map((p) => (
                <tr key={p.product_id} className="hover:bg-gray-800/40 transition">
                  <td className="py-3 px-3 text-gray-400 font-mono">{p.product_id}</td>
                  <td className="py-3 px-3 font-semibold text-white">{p.product_name}</td>
                  <td className="py-3 px-3 text-gray-300">{p.category_name}</td>
                  <td className="py-3 px-3 text-gray-300">${p.price.toFixed(2)}</td>
                  <td className="py-3 px-3 text-sky-400">${p.total_revenue.toLocaleString()}</td>
                  <td className="py-3 px-3 text-amber-400 font-bold">{p.gross_margin_pct}%</td>
                  <td className="py-3 px-3 text-rose-400">{p.avg_discount_pct}%</td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      {p.risk_flag || 'Low Margin'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
