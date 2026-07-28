import React from 'react';
import { motion } from 'framer-motion';
import { ShieldAlert, Activity, Users, Lock, Server } from 'lucide-react';

export default function AdminPage() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-zinc-100 flex items-center gap-2">
            System Administration & Security Audit Trail
            <span className="text-[10px] px-2 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/20 font-mono">
              ADMIN ACCESS
            </span>
          </h2>
          <p className="text-xs text-zinc-400">Monitor active user sessions, audit logs, and rate limiting status.</p>
        </div>
      </div>

      {/* System Health Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl glass-panel space-y-1">
          <div className="flex justify-between text-zinc-400 text-xs font-medium">
            <span>API Server Rate Limit</span>
            <Activity className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-xl font-bold text-zinc-100 font-mono">100 req / min</p>
          <p className="text-[11px] text-emerald-400">Sliding Window Middleware Active</p>
        </div>

        <div className="p-4 rounded-xl glass-panel space-y-1">
          <div className="flex justify-between text-zinc-400 text-xs font-medium">
            <span>Active DB Sessions</span>
            <Server className="w-4 h-4 text-violet-400" />
          </div>
          <p className="text-xl font-bold text-zinc-100 font-mono">8 Connections</p>
          <p className="text-[11px] text-zinc-400">PostgreSQL Async Engine</p>
        </div>

        <div className="p-4 rounded-xl glass-panel space-y-1">
          <div className="flex justify-between text-zinc-400 text-xs font-medium">
            <span>Security Status</span>
            <Lock className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-xl font-bold text-emerald-400 font-mono">SECURE</p>
          <p className="text-[11px] text-zinc-400">JWT + RBAC + Bcrypt</p>
        </div>
      </div>

      {/* Audit Logs Table */}
      <div className="p-5 rounded-xl glass-panel space-y-4">
        <h3 className="text-sm font-semibold text-zinc-200">Recent Security Audit Trail</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-zinc-950/80 text-zinc-400 border-b border-zinc-800">
              <tr>
                <th className="p-3">Timestamp</th>
                <th className="p-3">User</th>
                <th className="p-3">Action</th>
                <th className="p-3">Resource</th>
                <th className="p-3">IP Address</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 font-mono">
              {[
                { time: '2026-07-27 10:15:22', user: 'analyst@company.ai', action: 'USER_LOGIN', resource: 'Auth', ip: '192.168.1.102' },
                { time: '2026-07-27 10:16:04', user: 'analyst@company.ai', action: 'UPLOAD_DATASET', resource: 'Dataset', ip: '192.168.1.102' },
                { time: '2026-07-27 10:18:30', user: 'analyst@company.ai', action: 'START_AUTOML', resource: 'AutoML', ip: '192.168.1.102' },
              ].map((log, idx) => (
                <tr key={idx} className="hover:bg-zinc-800/40">
                  <td className="p-3 text-zinc-500">{log.time}</td>
                  <td className="p-3 font-sans text-zinc-200">{log.user}</td>
                  <td className="p-3 font-bold text-cyan-400">{log.action}</td>
                  <td className="p-3 font-sans text-zinc-300">{log.resource}</td>
                  <td className="p-3 text-zinc-400">{log.ip}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  );
}
