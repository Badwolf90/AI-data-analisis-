import React from 'react';
import { motion } from 'framer-motion';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { BarChart2, PieChart, Layers } from 'lucide-react';

const scatterData = [
  { x: 25, y: 45000, category: 'Churn' },
  { x: 30, y: 55000, category: 'Retained' },
  { x: 45, y: 80000, category: 'Retained' },
  { x: 22, y: 32000, category: 'Churn' },
  { x: 50, y: 95000, category: 'Retained' },
  { x: 35, y: 62000, category: 'Churn' },
];

const featureImportanceData = [
  { feature: 'Contract_Length', importance: 0.38 },
  { feature: 'Monthly_Charges', importance: 0.26 },
  { feature: 'Tenure_Months', importance: 0.18 },
  { feature: 'Total_Charges', importance: 0.11 },
  { feature: 'Tech_Support', importance: 0.07 },
];

export default function VisualizationPage() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-zinc-100">Interactive EDA & Model Visualizations</h2>
          <p className="text-xs text-zinc-400">Explore feature correlations, scatter distributions, and SHAP importances.</p>
        </div>
        <div className="flex gap-2">
          <span className="text-xs font-mono px-3 py-1 rounded bg-zinc-800 text-zinc-300 border border-zinc-700">
            Dataset: customer_churn_v2.csv
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Scatter Plot */}
        <div className="p-5 rounded-xl glass-panel space-y-4">
          <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Age vs Income Distribution Scatter Plot
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                <XAxis dataKey="x" name="Age" stroke="#52525b" fontSize={11} />
                <YAxis dataKey="y" name="Income" stroke="#52525b" fontSize={11} />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a' }} />
                <Scatter name="Customers" data={scatterData} fill="#06b6d4" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Global SHAP Feature Importance Bar Chart */}
        <div className="p-5 rounded-xl glass-panel space-y-4">
          <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-violet-400" />
            Global SHAP Feature Importance Ranking
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={featureImportanceData} layout="vertical">
                <XAxis type="number" stroke="#52525b" fontSize={11} />
                <YAxis dataKey="feature" type="category" stroke="#52525b" fontSize={11} width={110} />
                <Tooltip contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a' }} />
                <Bar dataKey="importance" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
