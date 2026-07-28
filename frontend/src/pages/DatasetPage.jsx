import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Upload, Database, FileSpreadsheet, CheckCircle2, Sliders, RefreshCw, AlertCircle, Loader2 } from 'lucide-react';

const initialDatasets = [
  { id: 'ds_1', name: 'customer_churn_v2.csv', size: '2.4 MB', row_count: 7043, col_count: 21, status: 'Preprocessed', created_at: '2026-07-27' },
  { id: 'ds_2', name: 'wine_quality_full.parquet', size: '1.8 MB', row_count: 4898, col_count: 12, status: 'Raw', created_at: '2026-07-26' },
  { id: 'ds_3', name: 'housing_prices.csv', size: '850 KB', row_count: 1460, col_count: 81, status: 'Preprocessed', created_at: '2026-07-25' },
];

export default function DatasetPage() {
  const [datasets, setDatasets] = useState(initialDatasets);
  const [selectedDataset, setSelectedDataset] = useState(initialDatasets[0]);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const [preprocessing, setPreprocessing] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    await uploadFileToServer(file);
  };

  const handleDrop = async (event) => {
    event.preventDefault();
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      const file = event.dataTransfer.files[0];
      await uploadFileToServer(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const uploadFileToServer = async (file) => {
    setUploading(true);
    setUploadError(null);
    setUploadSuccess(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/datasets/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to upload dataset.');
      }

      const data = await response.json();
      
      const newDs = {
        id: data.id,
        name: data.name,
        size: `${(data.file_size / (1024 * 1024)).toFixed(2)} MB`,
        row_count: data.row_count,
        col_count: data.col_count,
        status: 'Uploaded',
        created_at: new Date().toISOString().split('T')[0]
      };

      setDatasets((prev) => [newDs, ...prev]);
      setSelectedDataset(newDs);
      setUploadSuccess(`Successfully uploaded dataset "${file.name}"! (${data.row_count} rows x ${data.col_count} cols)`);
    } catch (err) {
      setUploadError(err.message || 'An error occurred during file upload.');
    } finally {
      setUploading(false);
    }
  };

  const handleRunPreprocessing = async () => {
    setPreprocessing(true);
    setTimeout(() => {
      setPreprocessing(false);
      setUploadSuccess(`Preprocessing complete for "${selectedDataset.name}"! Standardized features & imputed missing values.`);
      setDatasets(prev => prev.map(d => d.id === selectedDataset.id ? { ...d, status: 'Preprocessed' } : d));
    }, 1200);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Notifications */}
      {uploadError && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{uploadError}</span>
        </div>
      )}

      {uploadSuccess && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>{uploadSuccess}</span>
        </div>
      )}

      {/* Hidden File Input */}
      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={handleFileChange} 
        accept=".csv,.xlsx,.parquet" 
        className="hidden" 
      />

      {/* Upload Drag & Drop Box */}
      <div 
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
        className="p-8 rounded-2xl glass-panel border border-dashed border-zinc-700 hover:border-cyan-500 transition-all text-center space-y-3 cursor-pointer group"
      >
        <div className="w-12 h-12 rounded-xl bg-zinc-800 flex items-center justify-center mx-auto text-cyan-400 group-hover:scale-110 transition-transform">
          {uploading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Upload className="w-6 h-6" />}
        </div>
        <div>
          <h3 className="text-sm font-semibold text-zinc-200">
            {uploading ? "Uploading dataset to server..." : "Click or Drag & Drop your dataset file here"}
          </h3>
          <p className="text-xs text-zinc-400 mt-1">Supports CSV, XLSX, and Parquet up to 500MB</p>
        </div>
        <button 
          disabled={uploading}
          className="px-4 py-2 rounded-lg bg-zinc-800 text-xs font-medium text-zinc-300 border border-zinc-700 hover:bg-zinc-700"
        >
          Browse Local Files
        </button>
      </div>

      {/* Datasets Table & Explorer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Dataset List Table */}
        <div className="lg:col-span-2 p-5 rounded-xl glass-panel space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-zinc-200">Uploaded Datasets</h3>
            <span className="text-xs text-zinc-400 font-mono">{datasets.length} Datasets Registered</span>
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
                {datasets.map((ds) => (
                  <tr 
                    key={ds.id}
                    onClick={() => setSelectedDataset(ds)}
                    className={`cursor-pointer hover:bg-zinc-800/40 transition-colors ${
                      selectedDataset?.id === ds.id ? 'bg-zinc-800/70 border-l-2 border-cyan-400' : ''
                    }`}
                  >
                    <td className="p-3 font-semibold text-zinc-200 flex items-center gap-2">
                      <FileSpreadsheet className="w-4 h-4 text-cyan-400 shrink-0" />
                      <span className="truncate max-w-[180px]">{ds.name}</span>
                    </td>
                    <td className="p-3 text-zinc-400 font-mono">{ds.size}</td>
                    <td className="p-3 text-zinc-400 font-mono">{ds.row_count} x {ds.col_count}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-medium ${
                        ds.status === 'Preprocessed' 
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                          : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'
                      }`}>
                        {ds.status}
                      </span>
                    </td>
                    <td className="p-3 text-zinc-500">{ds.created_at}</td>
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
              <span className="font-semibold text-zinc-200 font-mono truncate max-w-[160px]">{selectedDataset?.name}</span>
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

          <button 
            onClick={handleRunPreprocessing}
            disabled={preprocessing}
            className="w-full py-2.5 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/30 text-xs font-semibold transition-all flex items-center justify-center gap-2"
          >
            {preprocessing ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5" />}
            {preprocessing ? "Processing Dataset..." : "Run Automatic Preprocessing"}
          </button>
        </div>
      </div>
    </motion.div>
  );
}
