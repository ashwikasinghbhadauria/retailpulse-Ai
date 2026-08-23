import React from 'react';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  change?: number;
  changeLabel?: string;
  icon: LucideIcon;
  color?: 'sky' | 'emerald' | 'amber' | 'indigo' | 'purple' | 'rose';
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  subtitle,
  change,
  changeLabel = 'vs prev month',
  icon: Icon,
  color = 'sky'
}) => {
  const colorStyles = {
    sky: 'from-sky-500/10 to-transparent border-sky-500/20 text-sky-400 bg-sky-500/10',
    emerald: 'from-emerald-500/10 to-transparent border-emerald-500/20 text-emerald-400 bg-emerald-500/10',
    amber: 'from-amber-500/10 to-transparent border-amber-500/20 text-amber-400 bg-amber-500/10',
    indigo: 'from-indigo-500/10 to-transparent border-indigo-500/20 text-indigo-400 bg-indigo-500/10',
    purple: 'from-purple-500/10 to-transparent border-purple-500/20 text-purple-400 bg-purple-500/10',
    rose: 'from-rose-500/10 to-transparent border-rose-500/20 text-rose-400 bg-rose-500/10',
  };

  const isPositive = change !== undefined ? change >= 0 : null;

  return (
    <div className="relative overflow-hidden bg-gray-900 border border-gray-800 rounded-2xl p-5 hover:border-gray-700 transition-all group shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
            {title}
          </p>
          <h3 className="text-2xl font-bold text-white tracking-tight mt-1.5">
            {value}
          </h3>
          {subtitle && (
            <p className="text-xs text-gray-400 mt-0.5">{subtitle}</p>
          )}
        </div>

        <div className={`w-10 h-10 rounded-xl flex items-center justify-center border ${colorStyles[color]}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      {change !== undefined && (
        <div className="mt-4 pt-3 border-t border-gray-800/80 flex items-center gap-2">
          <span
            className={`inline-flex items-center text-xs font-semibold px-1.5 py-0.5 rounded ${
              isPositive
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
            }`}
          >
            {isPositive ? (
              <TrendingUp className="w-3 h-3 mr-1 inline" />
            ) : (
              <TrendingDown className="w-3 h-3 mr-1 inline" />
            )}
            {change > 0 ? `+${change}%` : `${change}%`}
          </span>
          <span className="text-[11px] text-gray-400 font-medium">
            {changeLabel}
          </span>
        </div>
      )}
    </div>
  );
};
