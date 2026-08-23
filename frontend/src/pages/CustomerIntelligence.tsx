import React, { useEffect, useState } from 'react';
import {
  Users,
  AlertTriangle,
  Mail
} from 'lucide-react';
import {
  ResponsiveContainer,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts';

import { api } from '../services/api';
import { SegmentationResponse, CustomerChurnResponse } from '../types';

const SEGMENT_COLORS = ['#0ea5e9', '#6366f1', '#10b981', '#f59e0b', '#ec4899'];
const RISK_COLORS = ['#10b981', '#f59e0b', '#ef4444'];

export const CustomerIntelligence: React.FC = () => {
  const [segmentation, setSegmentation] = useState<SegmentationResponse | null>(null);
  const [churn, setChurn] = useState<CustomerChurnResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [segRes, churnRes] = await Promise.all([
          api.getCustomerSegments(),
          api.getCustomerChurn(),
        ]);
        setSegmentation(segRes);
        setChurn(churnRes);
      } catch (err) {
        console.error('Failed to load customer intelligence:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading || !segmentation || !churn) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-sky-500/20 border-t-sky-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-12">
      {/* Overview Banner */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-xs font-semibold text-sky-400 mb-2">
            <Users className="w-3.5 h-3.5" />
            <span>K-Means RFM + ML Churn Model</span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            Customer Segmentation & Retention Intelligence
          </h2>
          <p className="text-xs text-gray-400 max-w-2xl mt-1">
            Standardized RFM feature space clustered into {segmentation.optimal_k} behavioral tiers (Silhouette: {segmentation.best_silhouette_score}).
            Combined with supervised ML churn risk scoring to identify at-risk high-value accounts.
          </p>
        </div>

        <div className="flex items-center gap-4 shrink-0">
          <div className="text-right">
            <p className="text-[11px] text-gray-400 uppercase font-semibold">Evaluated Customers</p>
            <p className="text-base font-bold text-white">{segmentation.total_segmented_customers.toLocaleString()}</p>
          </div>
          <div className="h-8 w-px bg-gray-800"></div>
          <div className="text-right">
            <p className="text-[11px] text-gray-400 uppercase font-semibold">Champion Churn Model</p>
            <p className="text-sm font-bold text-emerald-400">{churn.champion_model} (AUC: {churn.champion_roc_auc})</p>
          </div>
        </div>
      </div>

      {/* Customer Segment Profiles Grid */}
      <div>
        <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">
          RFM Behavioral Segments
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          {segmentation.segments.map((seg, idx) => (
            <div
              key={seg.cluster_id}
              className="bg-gray-900 border border-gray-800 rounded-2xl p-5 hover:border-gray-700 transition space-y-4"
            >
              <div className="flex items-start justify-between">
                <div>
                  <span
                    className="w-2.5 h-2.5 rounded-full inline-block mr-2"
                    style={{ backgroundColor: SEGMENT_COLORS[idx % SEGMENT_COLORS.length] }}
                  ></span>
                  <span className="text-xs font-bold text-white">{seg.segment_name}</span>
                  <p className="text-xs text-gray-400 mt-1">
                    {seg.customer_count.toLocaleString()} customers ({seg.customer_share_pct}%)
                  </p>
                </div>
              </div>

              <div className="pt-3 border-t border-gray-800/80 space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-400">Total Spend:</span>
                  <span className="font-semibold text-sky-400">${seg.total_revenue.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Revenue Share:</span>
                  <span className="font-semibold text-white">{seg.revenue_share_pct}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Avg Recency:</span>
                  <span className="font-semibold text-gray-200">{seg.avg_recency_days} days</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Avg Frequency:</span>
                  <span className="font-semibold text-gray-200">{seg.avg_frequency} orders</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Average Order Value:</span>
                  <span className="font-semibold text-emerald-400">${seg.avg_order_value.toFixed(2)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Segmentation Distribution Charts & Churn Risk Banding */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Segment Share vs Revenue Share */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <h3 className="text-base font-bold text-white tracking-tight mb-1">
            Segment Customer Count vs Revenue Contribution
          </h3>
          <p className="text-xs text-gray-400 mb-4">Proportion of customer base vs monetary value captured</p>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={segmentation.segments} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="segment_name" stroke="#6B7280" fontSize={10} tickLine={false} />
                <YAxis stroke="#6B7280" fontSize={11} tickLine={false} tickFormatter={(val) => `${val}%`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.75rem', fontSize: '12px' }}
                  formatter={(val: any) => [`${val}%`, '']}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="customer_share_pct" name="Customer Share %" fill="#6366f1" radius={[4, 4, 0, 0]} />
                <Bar dataKey="revenue_share_pct" name="Revenue Share %" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Churn Risk Band Breakdown */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white tracking-tight mb-1">
              Customer Population Churn Risk Bands
            </h3>
            <p className="text-xs text-gray-400 mb-6">
              Distribution of predicted churn probabilities across customer base
            </p>

            <div className="space-y-4">
              {churn.risk_band_distribution.map((band, idx) => (
                <div key={band.risk_band} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-gray-200">{band.risk_band}</span>
                    <span className="text-gray-400">
                      {band.customer_count.toLocaleString()} customers ({band.share_pct}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-800 rounded-full h-2.5 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${band.share_pct}%`,
                        backgroundColor: RISK_COLORS[idx % RISK_COLORS.length]
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-6 p-4 rounded-xl bg-gray-950/70 border border-gray-800 text-xs space-y-1 text-gray-300">
            <div className="flex items-center gap-1.5 text-amber-400 font-bold">
              <AlertTriangle className="w-4 h-4" />
              <span>Retention Opportunity</span>
            </div>
            <p className="text-[11px] text-gray-400">
              {churn.top_at_risk_vip_customers.length} high-value VIP accounts currently exceed 70% churn risk probability.
            </p>
          </div>
        </div>
      </div>

      {/* Top At-Risk VIP Customers Table */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">
              High-Value Accounts at Churn Risk
            </h3>
            <p className="text-xs text-gray-400">
              VIP accounts requiring immediate proactive retention outreach
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-gray-400 uppercase text-[10px] tracking-wider border-b border-gray-800 bg-gray-950/50">
              <tr>
                <th className="py-3 px-3">Customer ID</th>
                <th className="py-3 px-3">Customer Name</th>
                <th className="py-3 px-3">Region</th>
                <th className="py-3 px-3">Segment</th>
                <th className="py-3 px-3">Historical Spend</th>
                <th className="py-3 px-3">Orders</th>
                <th className="py-3 px-3">Days Inactive</th>
                <th className="py-3 px-3">Churn Probability</th>
                <th className="py-3 px-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60 font-medium">
              {churn.top_at_risk_vip_customers.map((c) => (
                <tr key={c.customer_id} className="hover:bg-gray-800/40 transition">
                  <td className="py-3 px-3 text-gray-400 font-mono">{c.customer_id}</td>
                  <td className="py-3 px-3 font-semibold text-white">{c.customer_name}</td>
                  <td className="py-3 px-3 text-gray-300">{c.region}</td>
                  <td className="py-3 px-3 text-gray-300">{c.segment}</td>
                  <td className="py-3 px-3 font-bold text-sky-400">${c.total_spend.toLocaleString()}</td>
                  <td className="py-3 px-3 text-gray-300">{c.total_orders}</td>
                  <td className="py-3 px-3 text-rose-400 font-semibold">{c.recency_days}d</td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">
                      {(c.churn_probability * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <button className="px-2.5 py-1 rounded-lg bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 text-[11px] font-semibold border border-sky-500/30 transition flex items-center gap-1">
                      <Mail className="w-3 h-3" />
                      Re-engage
                    </button>
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
