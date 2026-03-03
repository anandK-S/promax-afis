// ========================================
// Pro-Max AFIS - Financials Page (Complete)
// ========================================

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  DollarSign, TrendingUp, TrendingDown, CreditCard, 
  Plus, Filter, Download, Search, Calendar,
  ArrowUpRight, ArrowDownRight, PieChart, BarChart3,
  Eye, Edit2, Trash2, X, Check, AlertCircle
} from 'lucide-react';
import { Layout } from '../../components/layout/Layout';

// Types
interface Transaction {
  id: string;
  type: 'income' | 'expense';
  amount: number;
  category: string;
  description: string;
  date: string;
  paymentMethod: string;
  status: 'completed' | 'pending' | 'failed';
  gstAmount?: number;
  tdsAmount?: number;
}

interface FinancialSummary {
  totalIncome: number;
  totalExpenses: number;
  netProfit: number;
  profitMargin: number;
  pendingPayments: number;
  gstCollected: number;
  gstPaid: number;
}

// Mock Data
const mockTransactions: Transaction[] = [
  { id: '1', type: 'income', amount: 150000, category: 'Sales Revenue', description: 'Product sales - March', date: '2024-03-15', paymentMethod: 'UPI', status: 'completed', gstAmount: 27000 },
  { id: '2', type: 'expense', amount: 45000, category: 'Inventory Purchase', description: 'Raw materials', date: '2024-03-14', paymentMethod: 'Bank Transfer', status: 'completed', gstAmount: 8100 },
  { id: '3', type: 'income', amount: 85000, category: 'Service Income', description: 'Consulting services', date: '2024-03-13', paymentMethod: 'Cash', status: 'completed', gstAmount: 15300 },
  { id: '4', type: 'expense', amount: 25000, category: 'Salaries', description: 'Staff salaries - March', date: '2024-03-10', paymentMethod: 'Bank Transfer', status: 'completed' },
  { id: '5', type: 'expense', amount: 15000, category: 'Rent', description: 'Office rent - March', date: '2024-03-01', paymentMethod: 'Bank Transfer', status: 'completed' },
  { id: '6', type: 'income', amount: 75000, category: 'Sales Revenue', description: 'Online sales', date: '2024-03-08', paymentMethod: 'UPI', status: 'pending', gstAmount: 13500 },
  { id: '7', type: 'expense', amount: 8000, category: 'Utilities', description: 'Electricity bill', date: '2024-03-05', paymentMethod: 'UPI', status: 'completed' },
  { id: '8', type: 'expense', amount: 12000, category: 'Marketing', description: 'Social media ads', date: '2024-03-03', paymentMethod: 'Credit Card', status: 'completed', gstAmount: 2160 },
];

const mockSummary: FinancialSummary = {
  totalIncome: 310000,
  totalExpenses: 105000,
  netProfit: 205000,
  profitMargin: 66.1,
  pendingPayments: 75000,
  gstCollected: 55800,
  gstPaid: 10260
};

const categories = {
  income: ['Sales Revenue', 'Service Income', 'Interest Income', 'Other Income'],
  expense: ['Inventory Purchase', 'Salaries', 'Rent', 'Utilities', 'Marketing', 'Transport', 'Office Supplies', 'Other Expenses']
};

const paymentMethods = ['UPI', 'Cash', 'Bank Transfer', 'Credit Card', 'Debit Card', 'Cheque'];

// Currency Formatter
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(amount);
};

// Date Formatter
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
};

export const Financials: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'all' | 'income' | 'expense'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [showFilters, setShowFilters] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    type: 'income' as 'income' | 'expense',
    amount: '',
    category: '',
    description: '',
    date: new Date().toISOString().split('T')[0],
    paymentMethod: 'UPI',
    gstApplicable: false
  });

  // Filter Transactions
  const filteredTransactions = mockTransactions.filter(t => {
    const matchesType = activeTab === 'all' || t.type === activeTab;
    const matchesSearch = t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          t.category.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesSearch;
  });

  // Stats Cards Data
  const statsCards = [
    { 
      title: 'Total Income', 
      value: mockSummary.totalIncome, 
      change: '+12.5%', 
      positive: true, 
      icon: TrendingUp, 
      color: 'from-emerald-500 to-green-600' 
    },
    { 
      title: 'Total Expenses', 
      value: mockSummary.totalExpenses, 
      change: '+5.2%', 
      positive: false, 
      icon: TrendingDown, 
      color: 'from-red-500 to-rose-600' 
    },
    { 
      title: 'Net Profit', 
      value: mockSummary.netProfit, 
      change: '+18.3%', 
      positive: true, 
      icon: DollarSign, 
      color: 'from-blue-500 to-indigo-600' 
    },
    { 
      title: 'Pending Payments', 
      value: mockSummary.pendingPayments, 
      change: '3 invoices', 
      positive: false, 
      icon: CreditCard, 
      color: 'from-amber-500 to-orange-600' 
    }
  ];

  // Handle Form Submit
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In real app, this would call the API
    console.log('Form submitted:', formData);
    setShowAddModal(false);
    setFormData({
      type: 'income',
      amount: '',
      category: '',
      description: '',
      date: new Date().toISOString().split('T')[0],
      paymentMethod: 'UPI',
      gstApplicable: false
    });
  };

  // Category Breakdown Data
  const categoryBreakdown = [
    { name: 'Sales Revenue', value: 225000, percentage: 72.6, color: 'bg-emerald-500' },
    { name: 'Service Income', value: 85000, percentage: 27.4, color: 'bg-blue-500' }
  ];

  const expenseBreakdown = [
    { name: 'Inventory', value: 45000, percentage: 42.9, color: 'bg-red-500' },
    { name: 'Salaries', value: 25000, percentage: 23.8, color: 'bg-orange-500' },
    { name: 'Rent', value: 15000, percentage: 14.3, color: 'bg-amber-500' },
    { name: 'Marketing', value: 12000, percentage: 11.4, color: 'bg-purple-500' },
    { name: 'Others', value: 8000, percentage: 7.6, color: 'bg-slate-500' }
  ];

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Financial Management
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1">
              Track income, expenses, and manage your business finances
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all">
              <Download className="w-4 h-4" />
              Export
            </button>
            <button 
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25"
            >
              <Plus className="w-4 h-4" />
              Add Transaction
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          {statsCards.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${stat.color} flex items-center justify-center`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <span className={`flex items-center gap-1 text-sm font-medium ${stat.positive ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
                  {stat.positive ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                  {stat.change}
                </span>
              </div>
              <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">
                {stat.title}
              </h3>
              <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">
                {formatCurrency(stat.value)}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Transactions List */}
          <div className="xl:col-span-2 bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700">
            {/* Tabs & Search */}
            <div className="p-4 border-b border-slate-100 dark:border-slate-700">
              <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                <div className="flex items-center gap-2 bg-slate-100 dark:bg-slate-700 rounded-xl p-1">
                  {['all', 'income', 'expense'].map(tab => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab as any)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        activeTab === tab 
                          ? 'bg-white dark:bg-slate-600 text-blue-600 dark:text-blue-400 shadow-sm' 
                          : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                      }`}
                    >
                      {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                  ))}
                </div>
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search transactions..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <button 
                  onClick={() => setShowFilters(!showFilters)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all ${
                    showFilters 
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-blue-600' 
                      : 'border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400'
                  }`}
                >
                  <Filter className="w-4 h-4" />
                  Filters
                </button>
              </div>
            </div>

            {/* Transactions Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 dark:bg-slate-700/50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                      Transaction
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                      Category
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                      Amount
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {filteredTransactions.map((transaction, index) => (
                    <motion.tr
                      key={transaction.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                    >
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                            transaction.type === 'income' 
                              ? 'bg-emerald-100 dark:bg-emerald-900/30' 
                              : 'bg-red-100 dark:bg-red-900/30'
                          }`}>
                            {transaction.type === 'income' 
                              ? <ArrowUpRight className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                              : <ArrowDownRight className="w-5 h-5 text-red-600 dark:text-red-400" />
                            }
                          </div>
                          <div>
                            <p className="font-medium text-slate-900 dark:text-white">
                              {transaction.description}
                            </p>
                            <p className="text-xs text-slate-500 dark:text-slate-400">
                              {transaction.paymentMethod}
                            </p>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        <span className="px-3 py-1 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
                          {transaction.category}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400">
                        {formatDate(transaction.date)}
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className={`font-semibold ${
                          transaction.type === 'income' 
                            ? 'text-emerald-600 dark:text-emerald-400' 
                            : 'text-red-600 dark:text-red-400'
                        }`}>
                          {transaction.type === 'income' ? '+' : '-'}{formatCurrency(transaction.amount)}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-center">
                        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-medium ${
                          transaction.status === 'completed' 
                            ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' 
                            : transaction.status === 'pending'
                            ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400'
                            : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                        }`}>
                          {transaction.status === 'completed' && <Check className="w-3 h-3" />}
                          {transaction.status === 'pending' && <AlertCircle className="w-3 h-3" />}
                          {transaction.status}
                        </span>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex items-center justify-center gap-2">
                          <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-blue-600 transition-colors">
                            <Edit2 className="w-4 h-4" />
                          </button>
                          <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-red-600 transition-colors">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="p-4 border-t border-slate-100 dark:border-slate-700 flex items-center justify-between">
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Showing {filteredTransactions.length} of {mockTransactions.length} transactions
              </p>
              <div className="flex items-center gap-2">
                <button className="px-3 py-1 rounded-lg border border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors">
                  Previous
                </button>
                <button className="px-3 py-1 rounded-lg bg-blue-600 text-white">
                  1
                </button>
                <button className="px-3 py-1 rounded-lg border border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors">
                  2
                </button>
                <button className="px-3 py-1 rounded-lg border border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors">
                  Next
                </button>
              </div>
            </div>
          </div>

          {/* Side Panel - Category Breakdown */}
          <div className="space-y-6">
            {/* Income Breakdown */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700">
              <div className="flex items-center gap-2 mb-4">
                <PieChart className="w-5 h-5 text-emerald-500" />
                <h3 className="font-semibold text-slate-900 dark:text-white">Income Breakdown</h3>
              </div>
              <div className="space-y-3">
                {categoryBreakdown.map(cat => (
                  <div key={cat.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${cat.color}`}></div>
                      <span className="text-sm text-slate-600 dark:text-slate-400">{cat.name}</span>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-slate-900 dark:text-white">
                        {formatCurrency(cat.value)}
                      </p>
                      <p className="text-xs text-slate-500">{cat.percentage}%</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Expense Breakdown */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 className="w-5 h-5 text-red-500" />
                <h3 className="font-semibold text-slate-900 dark:text-white">Expense Breakdown</h3>
              </div>
              <div className="space-y-3">
                {expenseBreakdown.map(cat => (
                  <div key={cat.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${cat.color}`}></div>
                      <span className="text-sm text-slate-600 dark:text-slate-400">{cat.name}</span>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-slate-900 dark:text-white">
                        {formatCurrency(cat.value)}
                      </p>
                      <p className="text-xs text-slate-500">{cat.percentage}%</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* GST Summary */}
            <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl p-6 text-white">
              <h3 className="font-semibold mb-4">GST Summary (March)</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-blue-200">GST Collected</span>
                  <span className="font-semibold">{formatCurrency(mockSummary.gstCollected)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-blue-200">GST Paid</span>
                  <span className="font-semibold">{formatCurrency(mockSummary.gstPaid)}</span>
                </div>
                <div className="border-t border-blue-500 pt-3 flex justify-between">
                  <span className="text-blue-200">Net GST Payable</span>
                  <span className="font-bold text-lg">{formatCurrency(mockSummary.gstCollected - mockSummary.gstPaid)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Add Transaction Modal */}
        <AnimatePresence>
          {showAddModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
              onClick={() => setShowAddModal(false)}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-full max-w-lg"
                onClick={e => e.stopPropagation()}
              >
                <div className="p-6 border-b border-slate-100 dark:border-slate-700 flex items-center justify-between">
                  <h2 className="text-xl font-bold text-slate-900 dark:text-white">Add Transaction</h2>
                  <button 
                    onClick={() => setShowAddModal(false)}
                    className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                  {/* Type Toggle */}
                  <div className="flex items-center gap-2 p-1 bg-slate-100 dark:bg-slate-700 rounded-xl">
                    <button
                      type="button"
                      onClick={() => setFormData({ ...formData, type: 'income' })}
                      className={`flex-1 py-2 rounded-lg font-medium transition-all ${
                        formData.type === 'income' 
                          ? 'bg-emerald-500 text-white shadow-lg' 
                          : 'text-slate-600 dark:text-slate-400'
                      }`}
                    >
                      Income
                    </button>
                    <button
                      type="button"
                      onClick={() => setFormData({ ...formData, type: 'expense' })}
                      className={`flex-1 py-2 rounded-lg font-medium transition-all ${
                        formData.type === 'expense' 
                          ? 'bg-red-500 text-white shadow-lg' 
                          : 'text-slate-600 dark:text-slate-400'
                      }`}
                    >
                      Expense
                    </button>
                  </div>

                  {/* Amount */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Amount (₹)
                    </label>
                    <input
                      type="number"
                      value={formData.amount}
                      onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                      placeholder="Enter amount"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  {/* Category */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Category
                    </label>
                    <select
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    >
                      <option value="">Select category</option>
                      {categories[formData.type].map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  </div>

                  {/* Description */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Description
                    </label>
                    <input
                      type="text"
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      placeholder="Enter description"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  {/* Date & Payment Method */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                        Date
                      </label>
                      <input
                        type="date"
                        value={formData.date}
                        onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                        Payment Method
                      </label>
                      <select
                        value={formData.paymentMethod}
                        onChange={(e) => setFormData({ ...formData, paymentMethod: e.target.value })}
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        {paymentMethods.map(method => (
                          <option key={method} value={method}>{method}</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* GST Toggle */}
                  <div className="flex items-center gap-3 p-4 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
                    <input
                      type="checkbox"
                      id="gstApplicable"
                      checked={formData.gstApplicable}
                      onChange={(e) => setFormData({ ...formData, gstApplicable: e.target.checked })}
                      className="w-5 h-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="gstApplicable" className="text-sm text-slate-700 dark:text-slate-300">
                      GST Applicable (18%)
                    </label>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowAddModal(false)}
                      className="flex-1 px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="flex-1 px-4 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25"
                    >
                      Add Transaction
                    </button>
                  </div>
                </form>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Layout>
  );
};