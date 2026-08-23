import React from 'react';
import {
  LayoutDashboard,
  TrendingUp,
  Users,
  Package,
  Cpu,
  Bot,
  Layers,
  Sparkles,
  ShieldCheck
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'executive', label: 'Executive Overview', icon: LayoutDashboard, badge: null },
    { id: 'sales', label: 'Sales Analytics', icon: TrendingUp, badge: null },
    { id: 'customers', label: 'Customer Intelligence', icon: Users, badge: 'RFM' },
    { id: 'products', label: 'Product Intelligence', icon: Package, badge: null },
    { id: 'forecasting', label: 'ML & Forecasting', icon: Cpu, badge: 'ML' },
    { id: 'ai-analyst', label: 'AI Business Analyst', icon: Bot, badge: 'AI' },
  ];

  return (
    <aside className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col justify-between shrink-0 h-screen sticky top-0">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center px-6 border-b border-gray-800 gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <Layers className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-tight text-white flex items-center gap-1.5">
              RetailPulse <span className="text-xs px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-400 font-semibold border border-sky-500/30">AI</span>
            </h1>
            <p className="text-[11px] text-gray-400 font-medium">Enterprise Intelligence</p>
          </div>
        </div>

        {/* Navigation Menu */}
        <div className="px-3 py-6">
          <p className="px-3 text-[11px] font-semibold uppercase tracking-wider text-gray-400 mb-3">
            Analytics & Models
          </p>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-sky-500/15 text-sky-400 border border-sky-500/30 shadow-sm'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-gray-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span
                      className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${
                        isActive
                          ? 'bg-sky-500 text-white'
                          : 'bg-gray-800 text-gray-400 border border-gray-700'
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Footer System Status */}
      <div className="p-4 border-t border-gray-800">
        <div className="bg-gray-950/60 rounded-xl p-3 border border-gray-800/80">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-gray-300 flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              Engine Status
            </span>
            <span className="inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Live (v1.0)
            </span>
          </div>
          <div className="text-[11px] text-gray-400 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-sky-400" />
            12k Customers &bull; 57k Orders
          </div>
        </div>
      </div>
    </aside>
  );
};
