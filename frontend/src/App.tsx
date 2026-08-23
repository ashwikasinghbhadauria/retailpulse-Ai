import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { ExecutiveOverview } from './pages/ExecutiveOverview';
import { SalesAnalytics } from './pages/SalesAnalytics';
import { CustomerIntelligence } from './pages/CustomerIntelligence';
import { ProductIntelligence } from './pages/ProductIntelligence';
import { MLForecasting } from './pages/MLForecasting';
import { AIBusinessAnalyst } from './pages/AIBusinessAnalyst';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('executive');

  const renderActivePage = () => {
    switch (activeTab) {
      case 'executive':
        return <ExecutiveOverview />;
      case 'sales':
        return <SalesAnalytics />;
      case 'customers':
        return <CustomerIntelligence />;
      case 'products':
        return <ProductIntelligence />;
      case 'forecasting':
        return <MLForecasting />;
      case 'ai-analyst':
        return <AIBusinessAnalyst />;
      default:
        return <ExecutiveOverview />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0B0F19] text-gray-100">
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar activeTab={activeTab} />
        <main className="flex-1 p-8 max-w-7xl w-full mx-auto">
          {renderActivePage()}
        </main>
      </div>
    </div>
  );
};

export default App;
