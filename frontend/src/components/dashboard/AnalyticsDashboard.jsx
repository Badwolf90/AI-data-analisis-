import React from 'react';
import { motion } from 'framer-motion';
import { 
  Users, Database, Cpu, Zap, Award, HardDrive, 
  Activity, Server, Gauge, Sparkles 
} from 'lucide-react';
import PlotlyChart from './PlotlyChart';

const darkLayoutDefaults = {
  paper_bgcolor: 'rgba(9, 9, 11, 0)',
  plot_bgcolor: 'rgba(9, 9, 11, 0)',
  font: { color: '#a1a1aa', family: 'Inter, sans-serif', size: 11 },
  margin: { l: 40, r: 20, t: 30, b: 40 },
  autosize: true,
};

export default function AnalyticsDashboard() {
  // Widget Data Configuration
  const kpiWidgets = [
    { title: 'Total Users', value: '1,420', change: '+14% this month', icon: Users, color: 'text-cyan-400' },
    { title: 'Datasets Managed', value: '342', change: '+28 new CSV/Parquet', icon: Database, color: 'text-violet-400' },
    { title: 'Active Trainings', value: '18 Runs', change: 'Optuna Tuning Active', icon: Cpu, color: 'text-emerald-400' },
    { title: 'Total Predictions', value: '1,482,900', change: '+120k requests/day', icon: Zap, color: 'text-blue-400' },
    { title: 'Best Accuracy', value: '96.4%', change: 'GradientBoosting #1', icon: Award, color: 'text-cyan-400' },
    { title: 'Storage Used', value: '42.8 GB', change: '42.8% of 100 GB', icon: HardDrive, color: 'text-amber-400' },
    { title: 'CPU Usage', value: '34%', change: '8 Cores Active', icon: Activity, color: 'text-cyan-400' },
    { title: 'RAM Usage', value: '48%', change: '15.3 GB / 32 GB', icon: Server, color: 'text-purple-400' },
    { title: 'GPU VRAM', value: '62%', change: 'NVIDIA RTX 4090', icon: Gauge, color: 'text-emerald-400' },
  ];

  // 1. Line Chart Data (Accuracy & Loss over time)
  const lineChartData = [
    {
      x: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'],
      y: [88.5, 90.2, 92.4, 94.1, 95.6, 96.2, 96.4],
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Accuracy (%)',
      line: { color: '#06b6d4', width: 3 },
      marker: { size: 6, color: '#06b6d4' }
    },
    {
      x: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'],
      y: [0.35, 0.28, 0.21, 0.15, 0.11, 0.08, 0.06],
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Validation Loss',
      yaxis: 'y2',
      line: { color: '#8b5cf6', width: 2, dash: 'dot' }
    }
  ];

  const lineChartLayout = {
    ...darkLayoutDefaults,
    title: { text: 'AutoML Training Accuracy & Loss Progression', font: { color: '#f4f4f5', size: 13 } },
    yaxis: { title: 'Accuracy (%)', gridcolor: '#27272a' },
    yaxis2: { title: 'Loss', overlaying: 'y', side: 'right', gridcolor: 'rgba(0,0,0,0)' }
  };

  // 2. Pie Chart Data (Dataset Formats)
  const pieChartData = [{
    values: [45, 30, 15, 10],
    labels: ['CSV', 'Parquet', 'Excel', 'JSON'],
    type: 'pie',
    hole: 0.5,
    marker: { colors: ['#06b6d4', '#8b5cf6', '#10b981', '#f59e0b'] }
  }];

  const pieChartLayout = {
    ...darkLayoutDefaults,
    title: { text: 'Dataset Formats Distribution', font: { color: '#f4f4f5', size: 13 } }
  };

  // 3. Heatmap Data (Feature Correlation Matrix)
  const heatmapData = [{
    z: [
      [1.0, 0.85, 0.32, -0.12, 0.64],
      [0.85, 1.0, 0.41, -0.05, 0.72],
      [0.32, 0.41, 1.0, 0.18, 0.29],
      [-0.12, -0.05, 0.18, 1.0, -0.22],
      [0.64, 0.72, 0.29, -0.22, 1.0]
    ],
    x: ['Age', 'Income', 'Tenure', 'Support_Calls', 'Churn_Prob'],
    y: ['Age', 'Income', 'Tenure', 'Support_Calls', 'Churn_Prob'],
    type: 'heatmap',
    colorscale: 'Viridis'
  }];

  const heatmapLayout = {
    ...darkLayoutDefaults,
    title: { text: 'Feature Correlation Matrix Heatmap', font: { color: '#f4f4f5', size: 13 } }
  };

  // 4. Radar Chart Data (Multi-Metric Evaluation)
  const radarChartData = [{
    type: 'scatterpolar',
    r: [96.5, 94.8, 95.2, 96.4, 98.2, 92.0],
    theta: ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC', 'Speed'],
    fill: 'toself',
    name: 'GradientBoosting',
    fillcolor: 'rgba(6, 182, 212, 0.3)',
    line: { color: '#06b6d4' }
  }];

  const radarChartLayout = {
    ...darkLayoutDefaults,
    title: { text: 'Model Multi-Metric Radar Evaluation', font: { color: '#f4f4f5', size: 13 } },
    polar: {
      radialaxis: { visible: true, range: [80, 100], color: '#52525b', gridcolor: '#27272a' },
      angularaxis: { color: '#a1a1aa', gridcolor: '#27272a' },
      bgcolor: 'rgba(9, 9, 11, 0)'
    }
  };

  // 5. Scatter Plot Data (Age vs Income)
  const scatterPlotData = [
    {
      x: [22, 25, 28, 32, 35, 40, 45, 50, 55, 60],
      y: [32000, 41000, 49000, 58000, 64000, 78000, 89000, 95000, 102000, 115000],
      mode: 'markers',
      type: 'scatter',
      name: 'Retained Customers',
      marker: { size: 10, color: '#10b981' }
    },
    {
      x: [21, 24, 27, 30, 33, 38, 42, 48],
      y: [28000, 34000, 39000, 45000, 51000, 62000, 71000, 81000],
      mode: 'markers',
      type: 'scatter',
      name: 'Churned Customers',
      marker: { size: 10, color: '#ef4444' }
    }
  ];

  const scatterPlotLayout = {
    ...darkLayoutDefaults,
    title: { text: 'Age vs Income Customer Distribution Scatter', font: { color: '#f4f4f5', size: 13 } },
    xaxis: { title: 'Age (Years)', gridcolor: '#27272a' },
    yaxis: { title: 'Annual Income ($)', gridcolor: '#27272a' }
  };

  // 6. Boxplot Data (Inference Latency by Model)
  const boxplotData = [
    { y: [12, 14, 15, 15, 16, 17, 18, 22], type: 'box', name: 'RandomForest', marker: { color: '#06b6d4' } },
    { y: [8, 9, 10, 11, 11, 12, 14, 16], type: 'box', name: 'XGBoost', marker: { color: '#8b5cf6' } },
    { y: [5, 6, 7, 7, 8, 9, 10, 12], type: 'box', name: 'LightGBM', marker: { color: '#10b981' } },
    { y: [18, 20, 22, 24, 25, 27, 30, 35], type: 'box', name: 'CatBoost', marker: { color: '#f59e0b' } },
  ];

  const boxplotLayout = {
    ...darkLayoutDefaults,
    title: { text: 'Inference Latency Distribution Boxplot (ms)', font: { color: '#f4f4f5', size: 13 } },
    yaxis: { title: 'Latency (ms)', gridcolor: '#27272a' }
  };

  // 7. Bar Chart Data (Leaderboard Algorithms Comparison)
  const barChartData = [{
    x: ['GradientBoosting', 'RandomForest', 'ExtraTrees', 'XGBoost', 'LightGBM', 'CatBoost', 'AdaBoost', 'DecisionTree', 'SVM', 'KNN', 'Ridge'],
    y: [96.4, 94.8, 94.2, 93.1, 92.7, 92.0, 89.5, 87.2, 86.8, 85.0, 82.4],
    type: 'bar',
    marker: {
      color: ['#06b6d4', '#06b6d4', '#8b5cf6', '#8b5cf6', '#8b5cf6', '#10b981', '#10b981', '#3b82f6', '#3b82f6', '#52525b', '#52525b']
    }
  }];

  const barChartLayout = {
    ...darkLayoutDefaults,
    title: { text: '11 Candidate Algorithms F1-Score Performance Leaderboard', font: { color: '#f4f4f5', size: 13 } },
    xaxis: { tickangle: -30 },
    yaxis: { title: 'F1-Score (%)', range: [75, 100], gridcolor: '#27272a' }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Dashboard Section Header */}
      <div className="flex justify-between items-center border-b border-zinc-800 pb-4">
        <div>
          <h2 className="text-lg font-bold text-zinc-100 flex items-center gap-2">
            System & Machine Learning Analytics Dashboard
            <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
              PLOTLY ENGINE ACTIVE
            </span>
          </h2>
          <p className="text-xs text-zinc-400">Real-time telemetry, 9 resource widgets, and 7 interactive Plotly charts.</p>
        </div>
      </div>

      {/* 9 KPI Resource Widgets Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-9 gap-3">
        {kpiWidgets.map((widget, idx) => {
          const Icon = widget.icon;
          return (
            <div key={idx} className="p-3.5 rounded-xl glass-panel border border-zinc-800 space-y-1.5 hover:border-zinc-700 transition-colors">
              <div className="flex justify-between items-center text-zinc-400">
                <span className="text-[10px] font-medium truncate">{widget.title}</span>
                <Icon className={`w-3.5 h-3.5 ${widget.color}`} />
              </div>
              <div className="text-base font-bold text-zinc-100 font-mono">{widget.value}</div>
              <p className="text-[9px] text-zinc-500 truncate">{widget.change}</p>
            </div>
          );
        })}
      </div>

      {/* 7 Interactive Plotly Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 1. Line Chart */}
        <div className="p-4 rounded-xl glass-panel border border-zinc-800 h-80">
          <PlotlyChart data={lineChartData} layout={lineChartLayout} />
        </div>

        {/* 2. Radar Chart */}
        <div className="p-4 rounded-xl glass-panel border border-zinc-800 h-80">
          <PlotlyChart data={radarChartData} layout={radarChartLayout} />
        </div>

        {/* 3. Heatmap Matrix */}
        <div className="p-4 rounded-xl glass-panel border border-zinc-800 h-80">
          <PlotlyChart data={heatmapData} layout={heatmapLayout} />
        </div>

        {/* 4. Pie Chart */}
        <div className="p-4 rounded-xl glass-panel border border-zinc-800 h-80">
          <PlotlyChart data={pieChartData} layout={pieChartLayout} />
        </div>

        {/* 5. Scatter Plot */}
        <div className="p-4 rounded-xl glass-panel border border-zinc-800 h-80">
          <PlotlyChart data={scatterPlotData} layout={scatterPlotLayout} />
        </div>

        {/* 6. Boxplot */}
        <div className="p-4 rounded-xl glass-panel border border-zinc-800 h-80">
          <PlotlyChart data={boxplotData} layout={boxplotLayout} />
        </div>
      </div>

      {/* 7. Full-Width Bar Chart Leaderboard */}
      <div className="p-4 rounded-xl glass-panel border border-zinc-800 h-96">
        <PlotlyChart data={barChartData} layout={barChartLayout} />
      </div>
    </motion.div>
  );
}
