import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { User, Key, Shield, Copy, Check, Sparkles } from 'lucide-react';

export default function ProfilePage() {
  const [copied, setCopied] = useState(false);
  const apiKey = "ai_live_8f90a21b459c0042d87e1a39f6";

  const handleCopy = () => {
    navigator.clipboard.writeText(apiKey);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6 max-w-4xl"
    >
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-zinc-100">User Profile & API Credentials</h2>
          <p className="text-xs text-zinc-400">Manage account preferences and developer access tokens.</p>
        </div>
      </div>

      {/* User Card */}
      <div className="p-6 rounded-2xl glass-panel border border-zinc-800 flex items-center gap-5">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-violet-500 via-purple-600 to-cyan-500 flex items-center justify-center font-bold text-xl text-white shadow-lg">
          DS
        </div>
        <div className="space-y-1">
          <h3 className="text-base font-bold text-zinc-100 flex items-center gap-2">
            Senior Data Scientist
            <span className="text-[10px] px-2 py-0.5 rounded bg-violet-500/10 text-violet-400 border border-violet-500/20 font-mono">
              ANALYST ROLE
            </span>
          </h3>
          <p className="text-xs text-zinc-400">analyst@company.ai</p>
          <p className="text-[11px] text-zinc-500 font-mono">User ID: 3c335b8b-02e1-4458-9375-08af69e62a0c</p>
        </div>
      </div>

      {/* API Key Generator */}
      <div className="p-6 rounded-2xl glass-panel border border-zinc-800 space-y-4">
        <div className="flex items-center gap-2">
          <Key className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-semibold text-zinc-200">Personal Developer API Token</h3>
        </div>
        <p className="text-xs text-zinc-400">Use this API token to integrate AutoML and Inference endpoints directly into your Python scripts or CI/CD pipelines.</p>

        <div className="flex items-center gap-2">
          <input 
            type="text" 
            readOnly 
            value={apiKey} 
            className="flex-1 glass-input px-4 py-2 text-xs font-mono text-cyan-400"
          />
          <button 
            onClick={handleCopy}
            className="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-xs font-medium text-zinc-200 border border-zinc-700 transition-all flex items-center gap-2"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? 'Copied!' : 'Copy API Key'}
          </button>
        </div>
      </div>
    </motion.div>
  );
}
