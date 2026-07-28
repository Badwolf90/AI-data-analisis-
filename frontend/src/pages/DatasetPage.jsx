import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Database, FileSpreadsheet, CheckCircle2, Sliders, RefreshCw } from 'lucide-react';

const mockDatasets = [
  { id: 'ds_1', name: 'customer_churn_v2.csv', size: '2.4 MB', rows: 7043, cols: 21, status: 'Preprocessed', date: '2026-07-27' },
  { id: 'ds_2', name: 'wine_quality_full.parquet', size: '1.8 MB', rows: 4898, cols: 12, status: 'Raw', date: '2026-07-26' },
  { id: 'ds_3', name: 'housing_prices.csv', size: '850 KB', rows: 1460, cols: 81, status: 'Preprocessed', date: '2026-07-25' },
];

export default function DatasetPage() {
  const [selectedDataset, setSelectedDataset] = useState(mockDatasets[0]);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Upload Drag & Drop Box */}
      <div className="p-8 rounded-2xl glass-panel border border-dashed border-zinc-700 hover:border-cyan-500 transition-all text-center space-y-3 cursor-pointer group">
        <div className="w-12 h-12 rounded-xl bg-zinc-800 flex items-center justify-center mx-auto text-cyan-400 group-hover:scale-110 transition-transform">
          <Upload className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-zinc-200">Drag and drop your dataset file here</h3>
          <p className="text-xs text-zinc-400 mt-1">Supports CSV, XLSX, and Parquet up to 500MB</p>
        </div>
        <button className="px-4 py-2 rounded-lg bg-zinc-800 text-xs font-medium text-zinc-300 border border-zinc-700 hover:bg-zinc-700">
          Browse Local Files
        </button>
      </div>

      {/* Datasets Table & Explorer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Dataset List Table */}
        <div className="lg:col-span-2 p-5 rounded-xl glass-panel space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-zinc-200">Uploaded Datasets</h3>
            <span className="text-xs text-zinc-400 font-mono">3 Datasets Registered</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-zinc-950/80 text-zinc-400 border-b border-zinc-800">
                <tr>
                  <th className="p-3">File Name</th>
                  <th className="p-3">Size</th>
                  <th className="p-3">Rows x Cols</th>
                  <th className="p-3">Status</th>
                  <th className="p-3">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/60">
                {mockDatasets.map((ds) => (
                  <tr 
                    key={ds.id}
                    onClick={() => setSelectedDataset(ds)}
                    className={`cursor-pointer hover:bg-zinc-800/40 transition-colors ${
                      selectedDataset.id === ds.id ? 'bg-zinc-800/70 border-l-2 border-cyan-400' : ''
                    }`}
                  >
                    <td className="p-3 font-semibold text-zinc-200 flex items-center gap-2">
                      <FileSpreadsheet className="w-4 h-4 text-cyan-400" />
                      {ds.name}
                    </td>
                    <td className="p-3 text-zinc-400 font-mono">{ds.size}</td>
                    <td className="p-3 text-zinc-400 font-mono">{ds.rows} x {ds.cols}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-medium ${
                        ds.status === 'Preprocessed' 
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                          : 'bg-zinc-800 text-zinc-400'
                      }`}>
                        {ds.status}
                      </span>
                    </td>
                    <td className="p-3 text-zinc-500">{ds.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Selected Dataset Inspection & Preprocessing Controls */}
        <div className="p-5 rounded-xl glass-panel space-y-4">
          <div className="flex justify-between items-center border-b border-zinc-800 pb-3">
            <h3 className="text-sm font-semibold text-zinc-200">Dataset Inspection</h3>
            <Sliders className="w-4 h-4 text-cyan-400" />
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between">
              <span className="text-zinc-400">Selected:</span>
              <span className="font-semibold text-zinc-200 font-mono">{selectedDataset.name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-zinc-400">Missing Values Imputation:</span>
              <span className="text-emerald-400 font-mono">Median / Mode</span>
            </div>
            <div className="flex justify-between">
              <span className="text-zinc-400">Categorical Encoding:</span>
              <span className="text-cyan-400 font-mono">LabelEncoder</span>
            </div>
            <div className="flex justify-between">
              <span className="text-zinc-400">Scaling Method:</span>
              <span className="text-violet-400 font-mono">StandardScaler</span>
            </div>
          </div>

          <button className="w-full py-2.5 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/30 text-xs font-semibold transition-all flex items-center justify-center gap-2">
            <RefreshCw className="w-3.5 h-3.5" />
            Run Automatic Preprocessing
          </button>
        </div>
      </div>
    </motion.div>
  );
}
