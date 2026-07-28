import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Cpu, Play, CheckCircle2, Award, Zap, SlidersHorizontal } from 'lucide-react';

const algorithmsList = [
  'RandomForest', 'ExtraTrees', 'GradientBoosting', 'AdaBoost', 'DecisionTree',
  'LogisticRegression_Ridge', 'SVM', 'KNN', 'XGBoost', 'LightGBM', 'CatBoost'
];

export default function AutoMLPage() {
  const [isRunning, setIsRunning] = useState(false);
  const [targetCol, setTargetCol] = useState('Churn');
  const [timeBudget, setTimeBudget] = useState(300);

  const handleStartAutoML = () => {
    setIsRunning(true);
    setTimeout(() => setIsRunning(false), 3000);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-zinc-100 flex items-center gap-2">
            AutoML Engine & Hyperparameter Optimization
          </h2>
          <p className="text-xs text-zinc-400">Automated candidate pool evaluation across 11 supervised algorithms.</p>
        </div>

        <button 
          onClick={handleStartAutoML}
          disabled={isRunning}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-xs font-bold text-white shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-2 disabled:opacity-50"
        >
          {isRunning ? <Zap className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-white" />}
          {isRunning ? 'Running Optuna Tuning...' : 'Start Full AutoML Pipeline'}
        </button>
      </div>

      {/* Configuration & Candidates */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* AutoML Config Form */}
        <div className="p-5 rounded-xl glass-panel space-y-4">
          <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2">
            <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
            AutoML Configuration
          </h3>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-zinc-400 mb-1">Target Column</label>
              <input 
                type="text" 
                value={targetCol} 
                onChange={(e) => setTargetCol(e.target.value)}
                className="w-full glass-input p-2" 
              />
            </div>
            <div>
              <label className="block text-zinc-400 mb-1">Task Type</label>
              <select className="w-full glass-input p-2 text-zinc-200">
                <option value="CLASSIFICATION">Classification (Stratified 5-Fold)</option>
                <option value="REGRESSION">Regression (K-Fold CV)</option>
              </select>
            </div>
            <div>
              <label className="block text-zinc-400 mb-1">Time Budget (Seconds)</label>
              <input 
                type="number" 
                value={timeBudget} 
                onChange={(e) => setTimeBudget(e.target.value)}
                className="w-full glass-input p-2" 
              />
            </div>
          </div>
        </div>

        {/* 11 Candidate Algorithms Checklist */}
        <div className="lg:col-span-2 p-5 rounded-xl glass-panel space-y-4">
          <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-violet-400" />
            11 Candidate Algorithms Selected for Training
          </h3>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {algorithmsList.map((algo, idx) => (
              <div key={idx} className="p-3 rounded-lg bg-zinc-950/60 border border-zinc-800 flex items-center justify-between">
                <span className="text-xs font-semibold text-zinc-200">{algo}</span>
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* AutoML Leaderboard */}
      <div className="p-5 rounded-xl glass-panel space-y-4">
        <h3 className="text-sm font-semibold text-zinc-200">Leaderboard Rankings</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-zinc-950/80 text-zinc-400 border-b border-zinc-800">
              <tr>
                <th className="p-3">Rank</th>
                <th className="p-3">Algorithm</th>
                <th className="p-3">CV Score</th>
                <th className="p-3">Accuracy</th>
                <th className="p-3">F1-Score</th>
                <th className="p-3">ROC-AUC</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 font-mono">
              {[
                { rank: 1, algo: 'GradientBoosting', cv: '0.962', acc: '96.5%', f1: '96.4%', roc: '0.982', isBest: true },
                { rank: 2, algo: 'RandomForest', cv: '0.945', acc: '94.8%', f1: '94.8%', roc: '0.965', isBest: false },
                { rank: 3, algo: 'XGBoost', cv: '0.931', acc: '93.2%', f1: '93.1%', roc: '0.954', isBest: false },
                { rank: 4, algo: 'LightGBM', cv: '0.925', acc: '92.7%', f1: '92.6%', roc: '0.948', isBest: false },
                { rank: 5, algo: 'CatBoost', cv: '0.920', acc: '92.1%', f1: '92.0%', roc: '0.942', isBest: false },
              ].map((item) => (
                <tr key={item.rank} className={item.isBest ? 'bg-cyan-500/10 border-l-2 border-cyan-400' : ''}>
                  <td className="p-3 font-bold text-zinc-200">#{item.rank}</td>
                  <td className="p-3 font-sans font-semibold text-zinc-100">{item.algo}</td>
                  <td className="p-3 text-cyan-400">{item.cv}</td>
                  <td className="p-3 text-zinc-300">{item.acc}</td>
                  <td className="p-3 text-emerald-400 font-bold">{item.f1}</td>
                  <td className="p-3 text-violet-400">{item.roc}</td>
                  <td className="p-3">
                    {item.isBest ? (
                      <span className="px-2 py-0.5 rounded text-[10px] bg-cyan-500/20 text-cyan-400 font-sans font-bold border border-cyan-500/30">
                        BEST MODEL
                      </span>
                    ) : (
                      <span className="text-zinc-500 font-sans">Trained</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  );
}
