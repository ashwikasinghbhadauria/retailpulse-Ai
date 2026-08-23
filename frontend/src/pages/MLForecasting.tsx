import React, { useEffect, useState } from 'react';
import {
  Cpu,
  CheckCircle2,
} from 'lucide-react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar
} from 'recharts';

import { api } from '../services/api';
import { DemandForecastResponse, CustomerChurnResponse } from '../types';

export const MLForecasting: React.FC = () => {
  const [forecast, setForecast] = useState<DemandForecastResponse | null>(null);
  const [churn, setChurn] = useState<CustomerChurnResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadML = async () => {
      try {
        setLoading(true);
        const [fcRes, churnRes] = await Promise.all([
          api.getDemandForecast(),
          api.getCustomerChurn(),
        ]);
        setForecast(fcRes);
        setChurn(churnRes);
      } catch (err) {
        console.error('Failed to load ML models & forecasting:', err);
      } finally {
        setLoading(false);
      }
    };
    loadML();
  }, []);

  if (loading || !forecast || !churn) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-sky-500/20 border-t-sky-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-12">
      {/* Header Overview */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-xs font-semibold text-indigo-400 mb-2">
            <Cpu className="w-3.5 h-3.5" />
            <span>Supervised ML & Time-Series Engine</span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            Predictive Analytics & Model Validation
          </h2>
          <p className="text-xs text-gray-400 max-w-2xl mt-1">
            Empirical demand forecasting with multi-step autoregressive features and 90% confidence bands.
            Side-by-side benchmarking of churn classification models on ROC-AUC, Recall, and F1-score.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="p-3 bg-gray-950 rounded-xl border border-gray-800 text-right">
            <p className="text-[10px] text-gray-400 uppercase font-semibold">Q4 Projected Sales</p>
            <p className="text-base font-bold text-sky-400">
              ${(forecast.next_quarter_projected_revenue / 1e6).toFixed(2)}M
            </p>
          </div>
          <div className="p-3 bg-gray-950 rounded-xl border border-gray-800 text-right">
            <p className="text-[10px] text-gray-400 uppercase font-semibold">Forecast Validation MAPE</p>
            <p className="text-base font-bold text-emerald-400">
              {forecast.validation_metrics.champion_mape}%
            </p>
          </div>
        </div>
      </div>

      {/* Demand Forecast Chart */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">
              Enterprise Demand Forecast ({forecast.forecast_horizon_months}-Month Horizon)
            </h3>
            <p className="text-xs text-gray-400">
              Historical actuals joined with future predictions and 90% confidence uncertainty intervals
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs font-medium">
            <span className="flex items-center gap-1.5 text-sky-400">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-500"></span> Actual Revenue
            </span>
            <span className="flex items-center gap-1.5 text-amber-400">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Projected Revenue
            </span>
            <span className="flex items-center gap-1.5 text-indigo-400">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500/40"></span> 90% Confidence Band
            </span>
          </div>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={forecast.forecast_timeline} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorUncertainty" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0.05} />
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
                formatter={(val: any) => [val != null ? `$${Number(val).toLocaleString()}` : '-', '']}
              />
              <Area type="monotone" dataKey="upper_bound_90ci" name="Upper 90% CI" stroke="none" fill="url(#colorUncertainty)" fillOpacity={1} />
              <Line type="monotone" dataKey="actual_revenue" name="Actual Sales" stroke="#0ea5e9" strokeWidth={2.5} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="predicted_revenue" name="Forecast" stroke="#f59e0b" strokeWidth={2.5} strokeDasharray="5 5" dot={{ r: 4 }} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Churn Model Benchmark & Feature Importances */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ML Churn Leaderboard Table */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">
                Customer Churn Model Comparison
              </h3>
              <p className="text-xs text-gray-400">Benchmarked against holdout test partition (25%)</p>
            </div>
            <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Champion: {churn.champion_model}
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-gray-400 uppercase text-[10px] tracking-wider border-b border-gray-800 bg-gray-950/50">
                <tr>
                  <th className="py-3 px-3">Model</th>
                  <th className="py-3 px-3">ROC-AUC</th>
                  <th className="py-3 px-3">Recall</th>
                  <th className="py-3 px-3">Precision</th>
                  <th className="py-3 px-3">F1-Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60 font-medium">
                {churn.model_comparisons.map((m) => (
                  <tr
                    key={m.model_name}
                    className={`transition ${m.model_name === churn.champion_model ? 'bg-sky-500/5' : 'hover:bg-gray-800/40'}`}
                  >
                    <td className="py-3 px-3 font-semibold text-white flex items-center gap-1.5">
                      {m.model_name === churn.champion_model && (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      )}
                      {m.model_name}
                    </td>
                    <td className="py-3 px-3 font-bold text-sky-400">{m.roc_auc.toFixed(4)}</td>
                    <td className="py-3 px-3 text-emerald-400">{m.recall.toFixed(4)}</td>
                    <td className="py-3 px-3 text-gray-300">{m.precision.toFixed(4)}</td>
                    <td className="py-3 px-3 text-white font-semibold">{m.f1_score.toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Feature Importances Bar Chart */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <h3 className="text-base font-bold text-white tracking-tight mb-1">
            Churn Driver Feature Importances
          </h3>
          <p className="text-xs text-gray-400 mb-4">Gini importance weights from champion ensemble</p>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={churn.feature_importances} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" horizontal={false} />
                <XAxis type="number" stroke="#6B7280" fontSize={11} tickLine={false} tickFormatter={(val) => `${(val * 100).toFixed(0)}%`} />
                <YAxis dataKey="feature" type="category" stroke="#6B7280" fontSize={10} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.75rem', fontSize: '12px' }}
                  formatter={(val: number) => [`${(val * 100).toFixed(1)}%`, 'Importance']}
                />
                <Bar dataKey="importance" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
