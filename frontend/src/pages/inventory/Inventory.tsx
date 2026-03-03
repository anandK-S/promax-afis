// ========================================
// Pro-Max AFIS - Inventory Page (Complete)
// ========================================

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Package, Plus, Search, Filter, Download, 
  TrendingUp, TrendingDown, AlertTriangle, 
  BarChart3, Box, Edit2, Trash2, Eye, X,
  ArrowUpRight, ArrowDownRight, Check, Clock,
  AlertCircle, ChevronDown
} from 'lucide-react';
import { Layout } from '../../components/layout/Layout';

// Types
interface Product {
  id: string;
  name: string;
  sku: string;
  category: string;
  costPrice: number;
  sellingPrice: number;
  stock: number;
  minStock: number;
  maxStock: number;
  unit: string;
  gst: number;
  hsnCode: string;
  status: 'active' | 'inactive' | 'out_of_stock';
  lastUpdated: string;
}

interface StockMovement {
  id: string;
  productId: string;
  productName: string;
  type: 'in' | 'out' | 'adjustment';
  quantity: number;
  reason: string;
  date: string;
  reference?: string;
}

interface LowStockAlert {
  id: string;
  productId: string;
  productName: string;
  currentStock: number;
  minStock: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'active' | 'resolved';
}

// Mock Data
const mockProducts: Product[] = [
  { id: '1', name: 'Premium Widget A', sku: 'WGT-A-001', category: 'Widgets', costPrice: 150, sellingPrice: 250, stock: 150, minStock: 50, maxStock: 500, unit: 'pieces', gst: 18, hsnCode: '8471', status: 'active', lastUpdated: '2024-03-15' },
  { id: '2', name: 'Standard Widget B', sku: 'WGT-B-002', category: 'Widgets', costPrice: 100, sellingPrice: 180, stock: 45, minStock: 50, maxStock: 300, unit: 'pieces', gst: 18, hsnCode: '8471', status: 'active', lastUpdated: '2024-03-14' },
  { id: '3', name: 'Industrial Component X', sku: 'CMP-X-003', category: 'Components', costPrice: 500, sellingPrice: 850, stock: 25, minStock: 30, maxStock: 100, unit: 'pieces', gst: 18, hsnCode: '8544', status: 'active', lastUpdated: '2024-03-13' },
  { id: '4', name: 'Electronic Module Y', sku: 'MOD-Y-004', category: 'Electronics', costPrice: 1200, sellingPrice: 2000, stock: 8, minStock: 20, maxStock: 50, unit: 'pieces', gst: 18, hsnCode: '8542', status: 'active', lastUpdated: '2024-03-12' },
  { id: '5', name: 'Connector Set Z', sku: 'CON-Z-005', category: 'Accessories', costPrice: 50, sellingPrice: 120, stock: 0, minStock: 100, maxStock: 500, unit: 'sets', gst: 18, hsnCode: '8536', status: 'out_of_stock', lastUpdated: '2024-03-10' },
  { id: '6', name: 'Power Supply Unit', sku: 'PSU-001', category: 'Electronics', costPrice: 800, sellingPrice: 1500, stock: 35, minStock: 25, maxStock: 75, unit: 'pieces', gst: 18, hsnCode: '8504', status: 'active', lastUpdated: '2024-03-08' },
  { id: '7', name: 'Display Panel LED', sku: 'DPL-002', category: 'Electronics', costPrice: 2500, sellingPrice: 4500, stock: 12, minStock: 15, maxStock: 40, unit: 'pieces', gst: 18, hsnCode: '8531', status: 'active', lastUpdated: '2024-03-05' },
  { id: '8', name: 'Mounting Bracket Set', sku: 'MBS-003', category: 'Accessories', costPrice: 75, sellingPrice: 150, stock: 200, minStock: 100, maxStock: 400, unit: 'sets', gst: 18, hsnCode: '8302', status: 'active', lastUpdated: '2024-03-01' },
];

const mockMovements: StockMovement[] = [
  { id: '1', productId: '1', productName: 'Premium Widget A', type: 'in', quantity: 50, reason: 'Purchase from supplier', date: '2024-03-15', reference: 'PO-2024-001' },
  { id: '2', productId: '2', productName: 'Standard Widget B', type: 'out', quantity: 25, reason: 'Sales order', date: '2024-03-14', reference: 'SO-2024-045' },
  { id: '3', productId: '3', productName: 'Industrial Component X', type: 'adjustment', quantity: -3, reason: 'Damaged goods', date: '2024-03-13' },
  { id: '4', productId: '4', productName: 'Electronic Module Y', type: 'out', quantity: 5, reason: 'Sales order', date: '2024-03-12', reference: 'SO-2024-044' },
  { id: '5', productId: '6', productName: 'Power Supply Unit', type: 'in', quantity: 15, reason: 'Purchase from supplier', date: '2024-03-08', reference: 'PO-2024-002' },
];

const mockAlerts: LowStockAlert[] = [
  { id: '1', productId: '2', productName: 'Standard Widget B', currentStock: 45, minStock: 50, severity: 'low', status: 'active' },
  { id: '2', productId: '3', productName: 'Industrial Component X', currentStock: 25, minStock: 30, severity: 'medium', status: 'active' },
  { id: '3', productId: '4', productName: 'Electronic Module Y', currentStock: 8, minStock: 20, severity: 'high', status: 'active' },
  { id: '4', productId: '5', productName: 'Connector Set Z', currentStock: 0, minStock: 100, severity: 'critical', status: 'active' },
  { id: '5', productId: '7', productName: 'Display Panel LED', currentStock: 12, minStock: 15, severity: 'low', status: 'active' },
];

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

export const Inventory: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'products' | 'movements' | 'alerts'>('products');
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  // Product Form State
  const [productForm, setProductForm] = useState({
    name: '',
    sku: '',
    category: '',
    costPrice: '',
    sellingPrice: '',
    stock: '',
    minStock: '',
    maxStock: '',
    unit: 'pieces',
    gst: '18',
    hsnCode: ''
  });

  // Movement Form State
  const [showMovementModal, setShowMovementModal] = useState(false);
  const [movementForm, setMovementForm] = useState({
    productId: '',
    type: 'in' as 'in' | 'out' | 'adjustment',
    quantity: '',
    reason: '',
    reference: ''
  });

  // Filter Products
  const filteredProducts = mockProducts.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          p.sku.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = filterCategory === 'all' || p.category === filterCategory;
    const matchesStatus = filterStatus === 'all' || p.status === filterStatus;
    return matchesSearch && matchesCategory && matchesStatus;
  });

  // Stats
  const totalProducts = mockProducts.length;
  const totalStock = mockProducts.reduce((sum, p) => sum + p.stock, 0);
  const totalValue = mockProducts.reduce((sum, p) => sum + (p.stock * p.costPrice), 0);
  const activeAlerts = mockAlerts.filter(a => a.status === 'active').length;

  const categories = ['all', ...new Set(mockProducts.map(p => p.category))];

  // Get severity color
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400';
      case 'high': return 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400';
      case 'medium': return 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400';
      case 'low': return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400';
      default: return 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-400';
    }
  };

  // Handle Product Submit
  const handleProductSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Product added:', productForm);
    setShowAddModal(false);
    setProductForm({
      name: '', sku: '', category: '', costPrice: '', sellingPrice: '',
      stock: '', minStock: '', maxStock: '', unit: 'pieces', gst: '18', hsnCode: ''
    });
  };

  // Handle Movement Submit
  const handleMovementSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Movement recorded:', movementForm);
    setShowMovementModal(false);
    setMovementForm({ productId: '', type: 'in', quantity: '', reason: '', reference: '' });
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Inventory Management
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1">
              Track products, stock levels, and manage inventory movements
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all">
              <Download className="w-4 h-4" />
              Export
            </button>
            <button 
              onClick={() => setShowMovementModal(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl border border-blue-200 dark:border-blue-800 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all"
            >
              <ArrowUpRight className="w-4 h-4" />
              Record Movement
            </button>
            <button 
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25"
            >
              <Plus className="w-4 h-4" />
              Add Product
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
                <Package className="w-6 h-6 text-white" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-emerald-600">
                <TrendingUp className="w-4 h-4" />
                +12 this month
              </span>
            </div>
            <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">Total Products</h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{totalProducts}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 flex items-center justify-center">
                <Box className="w-6 h-6 text-white" />
              </div>
            </div>
            <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">Total Stock Units</h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{totalStock.toLocaleString()}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-purple-500 to-pink-600 flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
            </div>
            <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">Stock Value</h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{formatCurrency(totalValue)}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-white" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-red-600">
                <AlertCircle className="w-4 h-4" />
                {activeAlerts} active
              </span>
            </div>
            <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium">Low Stock Alerts</h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{activeAlerts}</p>
          </motion.div>
        </div>

        {/* Main Content */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700">
          {/* Tabs */}
          <div className="p-4 border-b border-slate-100 dark:border-slate-700">
            <div className="flex flex-col sm:flex-row sm:items-center gap-4">
              <div className="flex items-center gap-2 bg-slate-100 dark:bg-slate-700 rounded-xl p-1">
                {[
                  { id: 'products', label: 'Products', icon: Package },
                  { id: 'movements', label: 'Movements', icon: TrendingUp },
                  { id: 'alerts', label: 'Alerts', icon: AlertTriangle }
                ].map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      activeTab === tab.id 
                        ? 'bg-white dark:bg-slate-600 text-blue-600 dark:text-blue-400 shadow-sm' 
                        : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    <tab.icon className="w-4 h-4" />
                    {tab.label}
                    {tab.id === 'alerts' && activeAlerts > 0 && (
                      <span className="w-5 h-5 rounded-full bg-red-500 text-white text-xs flex items-center justify-center">
                        {activeAlerts}
                      </span>
                    )}
                  </button>
                ))}
              </div>
              
              {activeTab === 'products' && (
                <>
                  <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      placeholder="Search products..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div className="flex items-center gap-2">
                    <select
                      value={filterCategory}
                      onChange={(e) => setFilterCategory(e.target.value)}
                      className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      {categories.map(cat => (
                        <option key={cat} value={cat}>{cat === 'all' ? 'All Categories' : cat}</option>
                      ))}
                    </select>
                    <select
                      value={filterStatus}
                      onChange={(e) => setFilterStatus(e.target.value)}
                      className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="all">All Status</option>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                      <option value="out_of_stock">Out of Stock</option>
                    </select>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Products Table */}
          {activeTab === 'products' && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 dark:bg-slate-700/50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Product</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">SKU</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Category</th>
                    <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Cost Price</th>
                    <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Selling Price</th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Stock</th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Status</th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {filteredProducts.map((product, index) => (
                    <motion.tr
                      key={product.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                    >
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                            product.status === 'out_of_stock' 
                              ? 'bg-red-100 dark:bg-red-900/30' 
                              : product.stock <= product.minStock
                              ? 'bg-amber-100 dark:bg-amber-900/30'
                              : 'bg-blue-100 dark:bg-blue-900/30'
                          }`}>
                            <Package className={`w-5 h-5 ${
                              product.status === 'out_of_stock' 
                                ? 'text-red-600 dark:text-red-400' 
                                : product.stock <= product.minStock
                                ? 'text-amber-600 dark:text-amber-400'
                                : 'text-blue-600 dark:text-blue-400'
                            }`} />
                          </div>
                          <div>
                            <p className="font-medium text-slate-900 dark:text-white">{product.name}</p>
                            <p className="text-xs text-slate-500 dark:text-slate-400">HSN: {product.hsnCode}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        <span className="px-2 py-1 rounded-lg text-xs font-mono bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
                          {product.sku}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400">
                        {product.category}
                      </td>
                      <td className="px-4 py-4 text-right text-sm text-slate-600 dark:text-slate-400">
                        {formatCurrency(product.costPrice)}
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className="font-medium text-slate-900 dark:text-white">
                          {formatCurrency(product.sellingPrice)}
                        </span>
                        <p className="text-xs text-emerald-600">
                          {Math.round((product.sellingPrice - product.costPrice) / product.costPrice * 100)}% margin
                        </p>
                      </td>
                      <td className="px-4 py-4">
                        <div className="text-center">
                          <span className={`text-lg font-semibold ${
                            product.stock === 0 ? 'text-red-600' : product.stock <= product.minStock ? 'text-amber-600' : 'text-slate-900 dark:text-white'
                          }`}>
                            {product.stock}
                          </span>
                          <p className="text-xs text-slate-500">Min: {product.minStock}</p>
                        </div>
                      </td>
                      <td className="px-4 py-4 text-center">
                        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-medium ${
                          product.status === 'active' 
                            ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' 
                            : product.status === 'inactive'
                            ? 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-400'
                            : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                        }`}>
                          {product.status === 'out_of_stock' && <AlertCircle className="w-3 h-3" />}
                          {product.status.replace('_', ' ')}
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
          )}

          {/* Movements Tab */}
          {activeTab === 'movements' && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 dark:bg-slate-700/50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Movement</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Product</th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Quantity</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Reason</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Reference</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {mockMovements.map((movement, index) => (
                    <motion.tr
                      key={movement.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                    >
                      <td className="px-4 py-4">
                        <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium ${
                          movement.type === 'in' 
                            ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' 
                            : movement.type === 'out'
                            ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                            : 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400'
                        }`}>
                          {movement.type === 'in' ? <ArrowDownRight className="w-3 h-3" /> : <ArrowUpRight className="w-3 h-3" />}
                          {movement.type === 'in' ? 'Stock In' : movement.type === 'out' ? 'Stock Out' : 'Adjustment'}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-sm text-slate-900 dark:text-white font-medium">
                        {movement.productName}
                      </td>
                      <td className="px-4 py-4 text-center">
                        <span className={`text-lg font-semibold ${
                          movement.quantity > 0 ? 'text-emerald-600' : 'text-red-600'
                        }`}>
                          {movement.quantity > 0 ? '+' : ''}{movement.quantity}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400">
                        {movement.reason}
                      </td>
                      <td className="px-4 py-4">
                        {movement.reference ? (
                          <span className="px-2 py-1 rounded-lg text-xs font-mono bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400">
                            {movement.reference}
                          </span>
                        ) : (
                          <span className="text-slate-400">-</span>
                        )}
                      </td>
                      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400">
                        {formatDate(movement.date)}
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Alerts Tab */}
          {activeTab === 'alerts' && (
            <div className="p-4">
              <div className="space-y-3">
                {mockAlerts.map((alert, index) => (
                  <motion.div
                    key={alert.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className={`flex items-center justify-between p-4 rounded-xl border ${
                      alert.severity === 'critical' 
                        ? 'border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20' 
                        : alert.severity === 'high'
                        ? 'border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/20'
                        : alert.severity === 'medium'
                        ? 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20'
                        : 'border-yellow-200 dark:border-yellow-800 bg-yellow-50 dark:bg-yellow-900/20'
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                        alert.severity === 'critical' ? 'bg-red-500' : alert.severity === 'high' ? 'bg-orange-500' : alert.severity === 'medium' ? 'bg-amber-500' : 'bg-yellow-500'
                      }`}>
                        <AlertTriangle className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <p className="font-medium text-slate-900 dark:text-white">{alert.productName}</p>
                        <p className="text-sm text-slate-600 dark:text-slate-400">
                          Current: <span className="font-semibold">{alert.currentStock}</span> units | 
                          Minimum: <span className="font-semibold">{alert.minStock}</span> units
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold uppercase ${getSeverityColor(alert.severity)}`}>
                        {alert.severity}
                      </span>
                      <button className="px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 transition-colors">
                        Reorder
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Add Product Modal */}
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
                className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
                onClick={e => e.stopPropagation()}
              >
                <div className="p-6 border-b border-slate-100 dark:border-slate-700 flex items-center justify-between sticky top-0 bg-white dark:bg-slate-800">
                  <h2 className="text-xl font-bold text-slate-900 dark:text-white">Add New Product</h2>
                  <button 
                    onClick={() => setShowAddModal(false)}
                    className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <form onSubmit={handleProductSubmit} className="p-6 space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-2">
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Product Name</label>
                      <input
                        type="text"
                        value={productForm.name}
                        onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
                        placeholder="Enter product name"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">SKU</label>
                      <input
                        type="text"
                        value={productForm.sku}
                        onChange={(e) => setProductForm({ ...productForm, sku: e.target.value })}
                        placeholder="WGT-XXX-001"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Category</label>
                      <input
                        type="text"
                        value={productForm.category}
                        onChange={(e) => setProductForm({ ...productForm, category: e.target.value })}
                        placeholder="e.g., Electronics, Widgets"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Cost Price (₹)</label>
                      <input
                        type="number"
                        value={productForm.costPrice}
                        onChange={(e) => setProductForm({ ...productForm, costPrice: e.target.value })}
                        placeholder="0"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Selling Price (₹)</label>
                      <input
                        type="number"
                        value={productForm.sellingPrice}
                        onChange={(e) => setProductForm({ ...productForm, sellingPrice: e.target.value })}
                        placeholder="0"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Current Stock</label>
                      <input
                        type="number"
                        value={productForm.stock}
                        onChange={(e) => setProductForm({ ...productForm, stock: e.target.value })}
                        placeholder="0"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Minimum Stock</label>
                      <input
                        type="number"
                        value={productForm.minStock}
                        onChange={(e) => setProductForm({ ...productForm, minStock: e.target.value })}
                        placeholder="0"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Maximum Stock</label>
                      <input
                        type="number"
                        value={productForm.maxStock}
                        onChange={(e) => setProductForm({ ...productForm, maxStock: e.target.value })}
                        placeholder="0"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Unit</label>
                      <select
                        value={productForm.unit}
                        onChange={(e) => setProductForm({ ...productForm, unit: e.target.value })}
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="pieces">Pieces</option>
                        <option value="sets">Sets</option>
                        <option value="kg">Kilograms</option>
                        <option value="liters">Liters</option>
                        <option value="meters">Meters</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">GST Rate (%)</label>
                      <select
                        value={productForm.gst}
                        onChange={(e) => setProductForm({ ...productForm, gst: e.target.value })}
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="0">0%</option>
                        <option value="5">5%</option>
                        <option value="12">12%</option>
                        <option value="18">18%</option>
                        <option value="28">28%</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">HSN Code</label>
                      <input
                        type="text"
                        value={productForm.hsnCode}
                        onChange={(e) => setProductForm({ ...productForm, hsnCode: e.target.value })}
                        placeholder="8471"
                        className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>

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
                      Add Product
                    </button>
                  </div>
                </form>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Record Movement Modal */}
        <AnimatePresence>
          {showMovementModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
              onClick={() => setShowMovementModal(false)}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-full max-w-md"
                onClick={e => e.stopPropagation()}
              >
                <div className="p-6 border-b border-slate-100 dark:border-slate-700 flex items-center justify-between">
                  <h2 className="text-xl font-bold text-slate-900 dark:text-white">Record Stock Movement</h2>
                  <button 
                    onClick={() => setShowMovementModal(false)}
                    className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <form onSubmit={handleMovementSubmit} className="p-6 space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Product</label>
                    <select
                      value={movementForm.productId}
                      onChange={(e) => setMovementForm({ ...movementForm, productId: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    >
                      <option value="">Select product</option>
                      {mockProducts.map(p => (
                        <option key={p.id} value={p.id}>{p.name} ({p.sku})</option>
                      ))}
                    </select>
                  </div>

                  <div className="flex items-center gap-2 p-1 bg-slate-100 dark:bg-slate-700 rounded-xl">
                    {[
                      { id: 'in', label: 'Stock In', icon: ArrowDownRight },
                      { id: 'out', label: 'Stock Out', icon: ArrowUpRight },
                      { id: 'adjustment', label: 'Adjustment', icon: Edit2 }
                    ].map(type => (
                      <button
                        key={type.id}
                        type="button"
                        onClick={() => setMovementForm({ ...movementForm, type: type.id as any })}
                        className={`flex-1 flex items-center justify-center gap-1 py-2 rounded-lg text-sm font-medium transition-all ${
                          movementForm.type === type.id 
                            ? type.id === 'in' 
                              ? 'bg-emerald-500 text-white shadow-lg' 
                              : type.id === 'out'
                              ? 'bg-red-500 text-white shadow-lg'
                              : 'bg-amber-500 text-white shadow-lg'
                            : 'text-slate-600 dark:text-slate-400'
                        }`}
                      >
                        <type.icon className="w-4 h-4" />
                        {type.label}
                      </button>
                    ))}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Quantity</label>
                    <input
                      type="number"
                      value={movementForm.quantity}
                      onChange={(e) => setMovementForm({ ...movementForm, quantity: e.target.value })}
                      placeholder="Enter quantity"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Reason</label>
                    <input
                      type="text"
                      value={movementForm.reason}
                      onChange={(e) => setMovementForm({ ...movementForm, reason: e.target.value })}
                      placeholder="e.g., Purchase, Sale, Damaged"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Reference (Optional)</label>
                    <input
                      type="text"
                      value={movementForm.reference}
                      onChange={(e) => setMovementForm({ ...movementForm, reference: e.target.value })}
                      placeholder="e.g., PO-2024-001"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div className="flex gap-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowMovementModal(false)}
                      className="flex-1 px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="flex-1 px-4 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25"
                    >
                      Record Movement
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