import React from 'react';
import { motion } from 'framer-motion';
import { History, Cpu, FileText, CheckCircle2 } from 'lucide-react';

export default function HistoryPage() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-zinc-100">Experiment History & Version Log</h2>
          <p className="text-xs text-zinc-400">Track past AutoML runs, registered model artifacts, and evaluation metrics.</p>
        </div>
      </div>

      <div className="p-5 rounded-xl glass-panel space-y-4">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-zinc-950/80 text-zinc-400 border-b border-zinc-800">
              <tr>
                <th className="p-3">Experiment ID</th>
                <th className="p-3">Dataset</th>
                <th className="p-3">Best Algorithm</th>
                <th className="p-3">Primary Score</th>
                <th className="p-3">Status</th>
                <th className="p-3">Created At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 font-mono">
              {[
                { id: 'exp_9041a', dataset: 'customer_churn_v2.csv', algo: 'GradientBoosting', score: '96.4%', status: 'COMPLETED', time: '2026-07-27 10:15' },
                { id: 'exp_8820b', dataset: 'wine_quality_full.parquet', algo: 'RandomForest', score: '94.8%', status: 'COMPLETED', time: '2026-07-26 14:30' },
                { id: 'exp_7712c', dataset: 'housing_prices.csv', algo: 'XGBoost', score: '93.2%', status: 'COMPLETED', time: '2026-07-25 09:45' },
              ].map((item) => (
                <tr key={item.id} className="hover:bg-zinc-800/40">
                  <td className="p-3 font-semibold text-cyan-400">{item.id}</td>
                  <td className="p-3 font-sans text-zinc-200">{item.dataset}</td>
                  <td className="p-3 font-sans font-bold text-zinc-100">{item.algo}</td>
                  <td className="p-3 text-emerald-400 font-bold">{item.score}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-sans">
                      {item.status}
                    </span>
                  </td>
                  <td className="p-3 text-zinc-500">{item.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  );
}
