// ========================================
// Pro-Max AFIS - Dashboard
// ========================================
// Premium command center with wow factor
// ========================================

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Layout } from '../../components/layout/Layout';
import { useAuth } from '../../contexts/AuthContext';
import { apiService } from '../../services/api';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4'];

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [financialSummary, setFinancialSummary] = useState<any>(null);
  const [healthScore, setHealthScore] = useState<any>(null);

  // Mock data for demonstration (will be replaced with real API calls)
  const salesData = [
    { month: 'Jan', sales: 40000, expenses: 28000, profit: 12000 },
    { month: 'Feb', sales: 45000, expenses: 30000, profit: 15000 },
    { month: 'Mar', sales: 52000, expenses: 32000, profit: 20000 },
    { month: 'Apr', sales: 48000, expenses: 29000, profit: 19000 },
    { month: 'May', sales: 58000, expenses: 34000, profit: 24000 },
    { month: 'Jun', sales: 62000, expenses: 36000, profit: 26000 },
  ];

  const categoryData = [
    { name: 'Sales', value: 45, color: '#3b82f6' },
    { name: 'Services', value: 25, color: '#8b5cf6' },
    { name: 'Other Income', value: 10, color: '#10b981' },
    { name: 'Inventory', value: 15, color: '#f59e0b' },
    { name: 'Marketing', value: 5, color: '#ef4444' },
  ];

  const topProducts = [
    { name: 'Product A', sales: 125000, trend: '+12%' },
    { name: 'Product B', sales: 98000, trend: '+8%' },
    { name: 'Product C', sales: 76000, trend: '+15%' },
    { name: 'Product D', sales: 65000, trend: '-3%' },
    { name: 'Product E', sales: 54000, trend: '+5%' },
  ];

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Load financial summary
      const summary = await apiService.financials.getSummary({ period: 'this_month' });
      setFinancialSummary(summary.data);
      
      // Load health score
      const health = await apiService.ml.getHealthScore();
      setHealthScore(health.data);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-3xl p-8 text-white shadow-2xl"
        >
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <h1 className="text-4xl font-bold mb-2">
                Welcome back, {user?.first_name}! 👋
              </h1>
              <p className="text-xl text-white/90">
                Here's what's happening with your business today
              </p>
            </div>
            <div className="flex gap-4">
              <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-6 text-center min-w-[150px]">
                <div className="text-3xl font-bold mb-1">₹2.6L</div>
                <div className="text-sm text-white/80">Total Revenue</div>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-6 text-center min-w-[150px]">
                <div className="text-3xl font-bold mb-1">₹1.9L</div>
                <div className="text-sm text-white/80">Total Expenses</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {[
            { label: 'Total Revenue', value: '₹2,65,000', trend: '+12%', color: 'from-blue-500 to-blue-600', icon: '💰' },
            { label: 'Total Expenses', value: '₹1,89,000', trend: '+8%', color: 'from-red-500 to-red-600', icon: '💸' },
            { label: 'Net Profit', value: '₹76,000', trend: '+18%', color: 'from-green-500 to-green-600', icon: '📈' },
            { label: 'Cash Flow', value: '₹1,45,000', trend: '+5%', color: 'from-purple-500 to-purple-600', icon: '💵' },
          ].map((stat, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.05, y: -5 }}
              className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border-2 border-transparent hover:border-blue-500"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center text-2xl shadow-lg`}>
                  {stat.icon}
                </div>
                <span className={`text-sm font-bold ${stat.trend.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
                  {stat.trend}
                </span>
              </div>
              <div className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
                {stat.value}
              </div>
              <div className="text-sm text-slate-600 dark:text-slate-400">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Revenue Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-slate-900 dark:text-white">Revenue Overview</h2>
              <select className="px-4 py-2 bg-slate-100 dark:bg-slate-700 rounded-lg text-sm text-slate-700 dark:text-slate-300 border-none outline-none">
                <option>Last 6 Months</option>
                <option>Last Year</option>
                <option>All Time</option>
              </select>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={salesData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }}
                  itemStyle={{ color: '#f1f5f9' }}
                />
                <Legend />
                <Area type="monotone" dataKey="sales" name="Sales" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
                <Area type="monotone" dataKey="expenses" name="Expenses" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
                <Area type="monotone" dataKey="profit" name="Profit" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Category Breakdown */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-slate-900 dark:text-white">Category Breakdown</h2>
              <button className="text-blue-600 hover:text-blue-700 font-medium text-sm">
                View All
              </button>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }}
                  itemStyle={{ color: '#f1f5f9' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* Financial Health & Top Products */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Health Score */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-6 text-white shadow-2xl"
          >
            <h2 className="text-xl font-bold mb-4">Financial Health</h2>
            <div className="text-center mb-6">
              <div className="text-7xl font-bold mb-2">87</div>
              <div className="text-white/90">Excellent</div>
            </div>
            <div className="space-y-3">
              {[
                { label: 'Cash Position', score: 92, color: 'bg-green-400' },
                { label: 'Profitability', score: 85, color: 'bg-blue-400' },
                { label: 'Efficiency', score: 88, color: 'bg-purple-400' },
              ].map((item, index) => (
                <div key={index}>
                  <div className="flex justify-between text-sm mb-1">
                    <span>{item.label}</span>
                    <span className="font-semibold">{item.score}%</span>
                  </div>
                  <div className="h-2 bg-white/30 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${item.color} rounded-full transition-all duration-500`}
                      style={{ width: `${item.score}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Top Products */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="lg:col-span-2 bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-slate-900 dark:text-white">Top Performing Products</h2>
              <button className="text-blue-600 hover:text-blue-700 font-medium text-sm">
                View All Products
              </button>
            </div>
            <div className="space-y-4">
              {topProducts.map((product, index) => (
                <motion.div
                  key={index}
                  whileHover={{ scale: 1.02 }}
                  className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-700 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-600 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="font-semibold text-slate-900 dark:text-white">{product.name}</div>
                      <div className="text-sm text-slate-600 dark:text-slate-400">₹{product.sales.toLocaleString()}</div>
                    </div>
                  </div>
                  <div className={`text-sm font-bold ${product.trend.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
                    {product.trend}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Recent Transactions & AI Insights */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Transactions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-slate-900 dark:text-white">Recent Transactions</h2>
              <button className="text-blue-600 hover:text-blue-700 font-medium text-sm">
                View All
              </button>
            </div>
            <div className="space-y-4">
              {[
                { id: 1, description: 'Product Sale - Product A', amount: 12500, type: 'income', date: '2 hours ago' },
                { id: 2, description: 'Inventory Purchase', amount: 8500, type: 'expense', date: '5 hours ago' },
                { id: 3, description: 'Service Payment', amount: 3200, type: 'income', date: 'Yesterday' },
                { id: 4, description: 'Office Rent', amount: 15000, type: 'expense', date: '2 days ago' },
                { id: 5, description: 'Product Sale - Product B', amount: 9800, type: 'income', date: '2 days ago' },
              ].map((transaction) => (
                <motion.div
                  key={transaction.id}
                  whileHover={{ scale: 1.02 }}
                  className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-700 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-600 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center text-lg ${
                      transaction.type === 'income' 
                        ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400' 
                        : 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'
                    }`}>
                      {transaction.type === 'income' ? '↑' : '↓'}
                    </div>
                    <div>
                      <div className="font-semibold text-slate-900 dark:text-white">{transaction.description}</div>
                      <div className="text-sm text-slate-600 dark:text-slate-400">{transaction.date}</div>
                    </div>
                  </div>
                  <div className={`font-bold ${transaction.type === 'income' ? 'text-green-500' : 'text-red-500'}`}>
                    {transaction.type === 'income' ? '+' : '-'}₹{transaction.amount.toLocaleString()}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* AI Insights */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.7 }}
            className="bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl p-6 text-white shadow-2xl"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center text-2xl">
                🤖
              </div>
              <div>
                <h2 className="text-xl font-bold">AI Insights</h2>
                <p className="text-white/80 text-sm">Intelligent recommendations</p>
              </div>
            </div>
            <div className="space-y-4">
              {[
                { 
                  type: 'alert', 
                  icon: '⚠️', 
                  title: 'Low Stock Alert', 
                  message: 'Product C is running low on stock. Consider reordering soon.',
                  color: 'bg-yellow-400/20 border-yellow-400'
                },
                { 
                  type: 'insight', 
                  icon: '💡', 
                  title: 'Revenue Opportunity', 
                  message: 'Sales of Product A increased by 12% this month. Consider increasing inventory.',
                  color: 'bg-blue-400/20 border-blue-400'
                },
                { 
                  type: 'trend', 
                  icon: '📈', 
                  title: 'Positive Trend', 
                  message: 'Your profit margin improved by 5% compared to last month. Keep up the good work!',
                  color: 'bg-green-400/20 border-green-400'
                },
              ].map((insight, index) => (
                <motion.div
                  key={index}
                  whileHover={{ scale: 1.02 }}
                  className={`p-4 ${insight.color} bg-opacity-10 border rounded-xl backdrop-blur-sm hover:bg-opacity-20 transition-all`}
                >
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{insight.icon}</span>
                    <div>
                      <div className="font-semibold mb-1">{insight.title}</div>
                      <div className="text-sm text-white/90">{insight.message}</div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
            <button className="w-full mt-6 py-3 bg-white text-purple-600 font-bold rounded-xl hover:bg-white/90 transition-colors flex items-center justify-center gap-2">
              <span>Chat with AI Assistant</span>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </button>
          </motion.div>
        </div>
      </div>
    </Layout>
  );
};