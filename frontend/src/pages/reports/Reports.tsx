// ========================================
// Pro-Max AFIS - Reports Page (Complete)
// ========================================

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  FileText, Download, Calendar, Filter, 
  BarChart3, PieChart, TrendingUp, TrendingDown,
  DollarSign, Package, Users, ShoppingCart,
  ArrowUpRight, ArrowDownRight, Printer, Share2,
  RefreshCw, Clock, CheckCircle
} from 'lucide-react';
import { Layout } from '../../components/layout/Layout';

// Types
interface Report {
  id: string;
  name: string;
  type: 'financial' | 'inventory' | 'sales' | 'tax';
  lastGenerated: string;
  status: 'ready' | 'generating' | 'scheduled';
  size: string;
}

// Mock Data
const mockReports: Report[] = [
  { id: '1', name: 'Monthly P&L Statement - March 2024', type: 'financial', lastGenerated: '2024-03-15 10:30', status: 'ready', size: '245 KB' },
  { id: '2', name: 'Inventory Valuation Report', type: 'inventory', lastGenerated: '2024-03-14 16:45', status: 'ready', size: '128 KB' },
  { id: '3', name: 'Sales Performance Report - Q1', type: 'sales', lastGenerated: '2024-03-15 09:00', status: 'ready', size: '312 KB' },
  { id: '4', name: 'GST Summary - March 2024', type: 'tax', lastGenerated: '2024-03-15 08:00', status: 'ready', size: '89 KB' },
  { id: '5', name: 'Cash Flow Statement', type: 'financial', lastGenerated: '2024-03-14 14:20', status: 'ready', size: '156 KB' },
  { id: '6', name: 'Low Stock Analysis', type: 'inventory', lastGenerated: '2024-03-13 11:15', status: 'ready', size: '78 KB' },
];

const reportTypes = [
  { id: 'all', label: 'All Reports', icon: FileText },
  { id: 'financial', label: 'Financial', icon: DollarSign },
  { id: 'inventory', label: 'Inventory', icon: Package },
  { id: 'sales', label: 'Sales', icon: ShoppingCart },
  { id: 'tax', label: 'Tax Reports', icon: BarChart3 },
];

// Monthly Data for Charts
const monthlyRevenue = [
  { month: 'Oct', revenue: 245000, expenses: 95000 },
  { month: 'Nov', revenue: 278000, expenses: 102000 },
  { month: 'Dec', revenue: 312000, expenses: 115000 },
  { month: 'Jan', revenue: 285000, expenses: 98000 },
  { month: 'Feb', revenue: 298000, expenses: 105000 },
  { month: 'Mar', revenue: 310000, expenses: 105000 },
];

const categoryBreakdown = [
  { name: 'Sales Revenue', value: 225000, color: 'bg-emerald-500' },
  { name: 'Service Income', value: 85000, color: 'bg-blue-500' },
  { name: 'Inventory Purchase', value: 45000, color: 'bg-red-500' },
  { name: 'Salaries', value: 25000, color: 'bg-orange-500' },
  { name: 'Rent', value: 15000, color: 'bg-amber-500' },
  { name: 'Marketing', value: 12000, color: 'bg-purple-500' },
];

// Currency Formatter
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(amount);
};

export const Reports: React.FC = () => {
  const [activeType, setActiveType] = useState('all');
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);

  // Filter Reports
  const filteredReports = mockReports.filter(r => 
    activeType === 'all' || r.type === activeType
  );

  // Get Type Badge Color
  const getTypeColor = (type: string) => {
    switch (type) {
      case 'financial': return 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400';
      case 'inventory': return 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400';
      case 'sales': return 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400';
      case 'tax': return 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400';
      default: return 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-400';
    }
  };

  // Calculate totals
  const totalRevenue = monthlyRevenue.reduce((sum, m) => sum + m.revenue, 0);
  const totalExpenses = monthlyRevenue.reduce((sum, m) => sum + m.expenses, 0);
  const avgProfitMargin = Math.round(((totalRevenue - totalExpenses) / totalRevenue) * 100);

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Reports & Analytics
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1">
              Generate, view, and download business reports
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700">
              <Calendar className="w-4 h-4 text-slate-500" />
              <input
                type="date"
                value={dateRange.start}
                onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                className="bg-transparent text-slate-700 dark:text-slate-300 focus:outline-none"
              />
              <span className="text-slate-400">to</span>
              <input
                type="date"
                value={dateRange.end}
                onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                className="bg-transparent text-slate-700 dark:text-slate-300 focus:outline-none"
              />
            </div>
            <button 
              onClick={() => setShowGenerateModal(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25"
            >
              <FileText className="w-4 h-4" />
              Generate Report
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-emerald-600">
                <ArrowUpRight className="w-4 h-4" />
                +18.3%
              </span>
            </div>
            <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">Total Revenue (6M)</h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{formatCurrency(totalRevenue)}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-red-500 to-rose-600 flex items-center justify-center">
                <TrendingDown className="w-6 h-6 text-white" />
              </div>
            </div>
            <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">Total Expenses (6M)</h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{formatCurrency(totalExpenses)}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
            </div>
            <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">Avg Profit Margin</h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{avgProfitMargin}%</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-purple-500 to-pink-600 flex items-center justify-center">
                <FileText className="w-6 h-6 text-white" />
              </div>
            </div>
            <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">Reports Generated</h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{mockReports.length}</p>
          </motion.div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Reports List */}
          <div className="xl:col-span-2 bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700">
            {/* Type Filter */}
            <div className="p-4 border-b border-slate-100 dark:border-slate-700">
              <div className="flex items-center gap-2 overflow-x-auto pb-2">
                {reportTypes.map(type => (
                  <button
                    key={type.id}
                    onClick={() => setActiveType(type.id)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all ${
                      activeType === type.id 
                        ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' 
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'
                    }`}
                  >
                    <type.icon className="w-4 h-4" />
                    {type.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Reports Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 dark:bg-slate-700/50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Report</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Type</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Generated</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Size</th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {filteredReports.map((report, index) => (
                    <motion.tr
                      key={report.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                    >
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-700 flex items-center justify-center">
                            <FileText className="w-5 h-5 text-slate-500 dark:text-slate-400" />
                          </div>
                          <div>
                            <p className="font-medium text-slate-900 dark:text-white">{report.name}</p>
                            <p className="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-1">
                              {report.status === 'ready' ? (
                                <>
                                  <CheckCircle className="w-3 h-3 text-emerald-500" />
                                  Ready
                                </>
                              ) : (
                                <>
                                  <Clock className="w-3 h-3 text-amber-500" />
                                  Processing
                                </>
                              )}
                            </p>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        <span className={`px-3 py-1 rounded-lg text-xs font-medium capitalize ${getTypeColor(report.type)}`}>
                          {report.type}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400">
                        {report.lastGenerated}
                      </td>
                      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400">
                        {report.size}
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex items-center justify-center gap-2">
                          <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-blue-600 transition-colors" title="View">
                            <FileText className="w-4 h-4" />
                          </button>
                          <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-emerald-600 transition-colors" title="Download">
                            <Download className="w-4 h-4" />
                          </button>
                          <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-purple-600 transition-colors" title="Print">
                            <Printer className="w-4 h-4" />
                          </button>
                          <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-blue-600 transition-colors" title="Share">
                            <Share2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Side Panel */}
          <div className="space-y-6">
            {/* Revenue Chart (Visual) */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-slate-900 dark:text-white">Revenue Trend</h3>
                <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500">
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
              
              {/* Simple Bar Chart */}
              <div className="space-y-3">
                {monthlyRevenue.map((item, index) => (
                  <div key={item.month} className="flex items-center gap-3">
                    <span className="w-8 text-xs text-slate-500">{item.month}</span>
                    <div className="flex-1 h-6 bg-slate-100 dark:bg-slate-700 rounded-lg overflow-hidden relative">
                      <div 
                        className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg"
                        style={{ width: `${(item.revenue / 350000) * 100}%` }}
                      />
                    </div>
                    <span className="w-16 text-xs text-slate-600 dark:text-slate-400 text-right">
                      {formatCurrency(item.revenue).replace('₹', '')}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Category Breakdown */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700">
              <div className="flex items-center gap-2 mb-4">
                <PieChart className="w-5 h-5 text-blue-500" />
                <h3 className="font-semibold text-slate-900 dark:text-white">Category Breakdown</h3>
              </div>
              
              <div className="space-y-3">
                {categoryBreakdown.map(cat => (
                  <div key={cat.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${cat.color}`}></div>
                      <span className="text-sm text-slate-600 dark:text-slate-400">{cat.name}</span>
                    </div>
                    <span className="text-sm font-medium text-slate-900 dark:text-white">
                      {formatCurrency(cat.value)}
                    </span>
                  </div>
                ))}
              </div>

              {/* Visual Pie Representation */}
              <div className="mt-4 flex items-center justify-center">
                <div className="relative w-32 h-32">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                    {categoryBreakdown.map((cat, i) => {
                      const total = categoryBreakdown.reduce((s, c) => s + c.value, 0);
                      const prevOffset = categoryBreakdown.slice(0, i).reduce((s, c) => s + (c.value / total) * 100, 0);
                      return (
                        <circle
                          key={cat.name}
                          cx="18"
                          cy="18"
                          r="15.9"
                          fill="transparent"
                          stroke={cat.color.replace('bg-', '').replace('-500', '')}
                          strokeWidth="3"
                          strokeDasharray={`${(cat.value / total) * 100} ${100 - (cat.value / total) * 100}`}
                          strokeDashoffset={-prevOffset}
                          className="transition-all duration-500"
                        />
                      );
                    })}
                  </svg>
                </div>
              </div>
            </div>

            {/* Quick Reports */}
            <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl p-6 text-white">
              <h3 className="font-semibold mb-4">Quick Reports</h3>
              <div className="space-y-2">
                {[
                  'Today\'s Summary',
                  'Weekly Sales',
                  'Monthly P&L',
                  'Inventory Status',
                  'GST Report'
                ].map((report, index) => (
                  <button
                    key={index}
                    className="w-full flex items-center justify-between p-3 rounded-xl bg-white/10 hover:bg-white/20 transition-all text-left"
                  >
                    <span className="text-sm">{report}</span>
                    <Download className="w-4 h-4" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Generate Report Modal */}
        {showGenerateModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowGenerateModal(false)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-full max-w-md"
              onClick={e => e.stopPropagation()}
            >
              <div className="p-6 border-b border-slate-100 dark:border-slate-700">
                <h2 className="text-xl font-bold text-slate-900 dark:text-white">Generate New Report</h2>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Select the type of report to generate</p>
              </div>
              
              <div className="p-6 space-y-3">
                {reportTypes.filter(t => t.id !== 'all').map(type => (
                  <button
                    key={type.id}
                    onClick={() => {
                      console.log(`Generating ${type.label} report...`);
                      setShowGenerateModal(false);
                    }}
                    className="w-full flex items-center gap-4 p-4 rounded-xl border border-slate-200 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all"
                  >
                    <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                      <type.icon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                    </div>
                    <div className="text-left">
                      <p className="font-medium text-slate-900 dark:text-white">{type.label} Report</p>
                      <p className="text-xs text-slate-500 dark:text-slate-400">Generate detailed {type.label.toLowerCase()} report</p>
                    </div>
                  </button>
                ))}
              </div>

              <div className="p-6 border-t border-slate-100 dark:border-slate-700">
                <button
                  onClick={() => setShowGenerateModal(false)}
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all"
                >
                  Cancel
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </div>
    </Layout>
  );
};