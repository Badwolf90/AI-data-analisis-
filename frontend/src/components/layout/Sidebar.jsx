import React from 'react';
import { 
  LayoutDashboard, Database, BarChart2, Cpu, Bot, 
  History, FileText, User, ShieldAlert, Sparkles, ChevronRight
} from 'lucide-react';

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'dataset', label: 'Dataset Manager', icon: Database, badge: 'CSV/Parquet' },
  { id: 'visualization', label: 'Visualization', icon: BarChart2 },
  { id: 'automl', label: 'AutoML Engine', icon: Cpu, badge: 'Optuna' },
  { id: 'copilot', label: 'AI Copilot', icon: Bot, highlight: true },
  { id: 'history', label: 'Experiment History', icon: History },
  { id: 'report', label: 'Report Generator', icon: FileText },
  { id: 'profile', label: 'Profile & API', icon: User },
  { id: 'admin', label: 'Admin & Audit', icon: ShieldAlert, role: 'Admin' },
];

export default function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="w-64 glass-panel border-r border-zinc-800/80 flex flex-col justify-between h-screen sticky top-0 z-30">
      <div>
        {/* Brand Header */}
        <div className="p-5 flex items-center gap-3 border-b border-zinc-800/60">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Sparkles className="w-5 h-5 text-white animate-pulse" />
          </div>
          <div>
            <h1 className="font-bold text-sm text-zinc-100 tracking-tight flex items-center gap-1.5">
              AI Platform <span className="text-[10px] bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-1.5 py-0.5 rounded font-mono">v1.0</span>
            </h1>
            <p className="text-xs text-zinc-400">Enterprise AI Analytics</p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="p-3 space-y-1">
          <div className="px-3 py-2 text-[10px] font-semibold uppercase tracking-wider text-zinc-400">
            Main Platform
          </div>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all group ${
                  isActive
                    ? 'bg-zinc-800/90 text-cyan-400 border border-zinc-700/60 shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 transition-colors ${
                    isActive ? 'text-cyan-400' : 'text-zinc-500 group-hover:text-zinc-300'
                  }`} />
                  <span>{item.label}</span>
                </div>

                <div className="flex items-center gap-1.5">
                  {item.badge && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono">
                      {item.badge}
                    </span>
                  )}
                  {item.highlight && (
                    <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                  )}
                  {isActive && <ChevronRight className="w-3.5 h-3.5 text-cyan-400" />}
                </div>
              </button>
            );
          })}
        </nav>
      </div>

      {/* User Footer Card */}
      <div className="p-3 border-t border-zinc-800/60">
        <div className="p-3 rounded-lg bg-zinc-950/60 border border-zinc-800/80 flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center font-bold text-xs text-white">
            DS
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-zinc-200 truncate">Senior Data Scientist</p>
            <p className="text-[11px] text-zinc-400 truncate">analyst@company.ai</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
