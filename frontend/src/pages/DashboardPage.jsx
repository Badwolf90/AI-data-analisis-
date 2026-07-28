import React from 'react';
import { motion } from 'framer-motion';
import { Database, Cpu } from 'lucide-react';
import AnalyticsDashboard from '../components/dashboard/AnalyticsDashboard';

export default function DashboardPage({ onNavigate }) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      {/* Header Banner */}
      <div className="p-6 rounded-2xl glass-panel border border-zinc-800 bg-gradient-to-r from-zinc-900 via-zinc-900/90 to-zinc-950 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-zinc-100 flex items-center gap-2">
            Welcome back, <span className="gradient-text">Senior Data Scientist</span> 👋
          </h2>
          <p className="text-xs text-zinc-400 mt-1">
            Enterprise Analytics Telemetry & Interactive Plotly Dashboard Engine Online.
          </p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={() => onNavigate('dataset')}
            className="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-xs font-medium text-zinc-200 border border-zinc-700 transition-all flex items-center gap-2"
          >
            <Database className="w-3.5 h-3.5 text-cyan-400" />
            Upload Dataset
          </button>
          <button 
            onClick={() => onNavigate('automl')}
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-xs font-semibold text-white shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-2"
          >
            <Cpu className="w-3.5 h-3.5" />
            Run AutoML Pipeline
          </button>
        </div>
      </div>

      {/* Embedded 9-Widget & 7-Plotly Chart Analytics Dashboard */}
      <AnalyticsDashboard />
    </motion.div>
  );
}
