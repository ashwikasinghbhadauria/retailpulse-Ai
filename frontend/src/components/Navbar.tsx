import React from 'react';
import { Database, Terminal } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab }) => {
  const getTabTitle = (tab: string) => {
    switch (tab) {
      case 'executive': return 'Executive Overview & Business KPIs';
      case 'sales': return 'Sales Trends & Geospatial Performance';
      case 'customers': return 'Customer Intelligence & RFM Clustering';
      case 'products': return 'Product Profitability & Assortment Matrix';
      case 'forecasting': return 'Machine Learning Models & Demand Forecasting';
      case 'ai-analyst': return 'Generative AI Business Analyst (Tool-Calling)';
      default: return 'Retail Intelligence Dashboard';
    }
  };

  return (
    <header className="h-16 bg-gray-900/80 backdrop-blur-md border-b border-gray-800 px-8 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-4">
        <div>
          <h2 className="text-base font-semibold text-white tracking-tight">
            {getTabTitle(activeTab)}
          </h2>
          <p className="text-xs text-gray-400">
            Real-time data warehouse & predictive ML engines
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Environment Badge */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700/60 text-xs text-gray-300">
          <Database className="w-3.5 h-3.5 text-sky-400" />
          <span>PostgreSQL / SQLite 3NF</span>
        </div>

        {/* API Docs Button */}
        <a
          href="http://127.0.0.1:8000/docs"
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-xs font-medium text-gray-200 border border-gray-700 transition"
        >
          <Terminal className="w-3.5 h-3.5 text-emerald-400" />
          <span>FastAPI Docs</span>
        </a>

        {/* Live Indicator */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-xs font-medium text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Online</span>
        </div>
      </div>
    </header>
  );
};
