import React, { useState } from 'react';
import Sidebar from './components/layout/Sidebar';
import Navbar from './components/layout/Navbar';
import DashboardPage from './pages/DashboardPage';
import DatasetPage from './pages/DatasetPage';
import VisualizationPage from './pages/VisualizationPage';
import AutoMLPage from './pages/AutoMLPage';
import CopilotPage from './pages/CopilotPage';
import HistoryPage from './pages/HistoryPage';
import ReportPage from './pages/ReportPage';
import ProfilePage from './pages/ProfilePage';
import AdminPage from './pages/AdminPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderActivePage = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardPage onNavigate={setActiveTab} />;
      case 'dataset':
        return <DatasetPage />;
      case 'visualization':
        return <VisualizationPage />;
      case 'automl':
        return <AutoMLPage />;
      case 'copilot':
        return <CopilotPage />;
      case 'history':
        return <HistoryPage />;
      case 'report':
        return <ReportPage />;
      case 'profile':
        return <ProfilePage />;
      case 'admin':
        return <AdminPage />;
      default:
        return <DashboardPage onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#09090b]">
      {/* Linear-style Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Application Container */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Vercel-style Navbar */}
        <Navbar activeTabTitle={activeTab} />

        {/* Page Content Container */}
        <main className="flex-1 p-6 overflow-y-auto">
          {renderActivePage()}
        </main>
      </div>
    </div>
  );
}
