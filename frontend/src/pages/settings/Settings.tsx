// ========================================
// Pro-Max AFIS - Settings Page (Complete)
// ========================================

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  User, Building, CreditCard, Bell, Shield,
  Palette, Globe, Database, Download, Trash2,
  Save, Eye, EyeOff, Key, Mail, Phone,
  Upload, CheckCircle, AlertCircle, Info
} from 'lucide-react';
import { Layout } from '../../components/layout/Layout';

export const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [showPassword, setShowPassword] = useState(false);
  const [saving, setSaving] = useState(false);

  // Profile Form State
  const [profile, setProfile] = useState({
    firstName: 'Rajesh',
    lastName: 'Sharma',
    email: 'rajesh.sharma@example.com',
    phone: '+91 98765 43210',
    role: 'Admin',
    avatar: ''
  });

  // Business Form State
  const [business, setBusiness] = useState({
    name: 'TechVision Industries Pvt Ltd',
    gst: '29AABCU9603R1ZM',
    pan: 'AABCU9603R',
    tan: 'MUMA01234E',
    industry: 'Technology & Electronics',
    currency: 'INR',
    financialYear: 'April-March',
    timezone: 'Asia/Kolkata'
  });

  // Payment Settings
  const [payments, setPayments] = useState({
    upiId: 'techvision@okaxis',
    bankName: 'State Bank of India',
    accountNumber: '1234567890123456',
    ifsc: 'SBIN0001234',
    accountType: 'Current Account'
  });

  // Notification Settings
  const [notifications, setNotifications] = useState({
    emailLowStock: true,
    emailPaymentReminders: true,
    emailDailySummary: false,
    pushAlerts: true,
    pushUpdates: true,
    pushMarketing: false,
    smsAlerts: false
  });

  // Security Settings
  const [security, setSecurity] = useState({
    twoFactorEnabled: false,
    sessionTimeout: '30',
    ipWhitelist: '',
    passwordExpiry: '90'
  });

  // Preferences
  const [preferences, setPreferences] = useState({
    language: 'en',
    dateFormat: 'DD/MM/YYYY',
    numberFormat: 'en-IN',
    theme: 'system'
  });

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'business', label: 'Business', icon: Building },
    { id: 'payments', label: 'Payments', icon: CreditCard },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'security', label: 'Security', icon: Shield },
    { id: 'preferences', label: 'Preferences', icon: Palette },
    { id: 'data', label: 'Data Management', icon: Database }
  ];

  const handleSave = async () => {
    setSaving(true);
    // Simulate save
    await new Promise(resolve => setTimeout(resolve, 1000));
    setSaving(false);
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            Settings
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            Manage your account and business settings
          </p>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 overflow-hidden">
          {/* Tabs */}
          <div className="border-b border-slate-100 dark:border-slate-700">
            <div className="flex items-center gap-1 p-2 overflow-x-auto">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium whitespace-nowrap transition-all ${
                    activeTab === tab.id 
                      ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' 
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            {/* Profile Tab */}
            {activeTab === 'profile' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-2xl space-y-6"
              >
                {/* Avatar Section */}
                <div className="flex items-center gap-6">
                  <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-3xl font-bold">
                    {profile.firstName[0]}{profile.lastName[0]}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                      {profile.firstName} {profile.lastName}
                    </h3>
                    <p className="text-slate-500">{profile.role}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <button className="px-3 py-1.5 rounded-lg text-sm bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600 transition-all">
                        <Upload className="w-4 h-4 inline mr-1" />
                        Upload Photo
                      </button>
                      <button className="px-3 py-1.5 rounded-lg text-sm bg-red-100 dark:bg-red-900/30 text-red-600 hover:bg-red-200 dark:hover:bg-red-900/40 transition-all">
                        <Trash2 className="w-4 h-4 inline mr-1" />
                        Remove
                      </button>
                    </div>
                  </div>
                </div>

                {/* Personal Information */}
                <div className="space-y-4">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider">
                    Personal Information
                  </h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">First Name</label>
                      <input
                        type="text"
                        value={profile.firstName}
                        onChange={(e) => setProfile({ ...profile, firstName: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Last Name</label>
                      <input
                        type="text"
                        value={profile.lastName}
                        onChange={(e) => setProfile({ ...profile, lastName: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="col-span-2">
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email Address</label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                        <input
                          type="email"
                          value={profile.email}
                          onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                          className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Phone Number</label>
                      <div className="relative">
                        <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                        <input
                          type="tel"
                          value={profile.phone}
                          onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                          className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Role</label>
                      <select
                        value={profile.role}
                        onChange={(e) => setProfile({ ...profile, role: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="Admin">Admin</option>
                        <option value="Manager">Manager</option>
                        <option value="Accountant">Accountant</option>
                        <option value="Viewer">Viewer</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Change Password */}
                <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-700">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider">
                    Change Password
                  </h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-2">
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Current Password</label>
                      <div className="relative">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <button
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                        >
                          {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">New Password</label>
                      <input
                        type="password"
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Confirm Password</label>
                      <input
                        type="password"
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </motion.div>
            )}

            {/* Business Tab */}
            {activeTab === 'business' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-2xl space-y-6"
              >
                <div className="space-y-4">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider">
                    Business Information
                  </h4>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Business Name</label>
                    <input
                      type="text"
                      value={business.name}
                      onChange={(e) => setBusiness({ ...business, name: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Industry</label>
                    <input
                      type="text"
                      value={business.industry}
                      onChange={(e) => setBusiness({ ...business, industry: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-700">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider">
                    Tax Information
                  </h4>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="col-span-1">
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">GST Number</label>
                      <input
                        type="text"
                        value={business.gst}
                        onChange={(e) => setBusiness({ ...business, gst: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="col-span-1">
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">PAN Number</label>
                      <input
                        type="text"
                        value={business.pan}
                        onChange={(e) => setBusiness({ ...business, pan: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="col-span-1">
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">TAN Number</label>
                      <input
                        type="text"
                        value={business.tan}
                        onChange={(e) => setBusiness({ ...business, tan: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-700">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider">
                    Financial Settings
                  </h4>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Currency</label>
                      <select
                        value={business.currency}
                        onChange={(e) => setBusiness({ ...business, currency: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="INR">INR (₹)</option>
                        <option value="USD">USD ($)</option>
                        <option value="EUR">EUR (€)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Financial Year</label>
                      <select
                        value={business.financialYear}
                        onChange={(e) => setBusiness({ ...business, financialYear: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="April-March">April-March</option>
                        <option value="January-December">January-December</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Timezone</label>
                      <select
                        value={business.timezone}
                        onChange={(e) => setBusiness({ ...business, timezone: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                        <option value="Asia/Dubai">Asia/Dubai (GST)</option>
                        <option value="America/New_York">America/New_York (EST)</option>
                      </select>
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </motion.div>
            )}

            {/* Payments Tab */}
            {activeTab === 'payments' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-2xl space-y-6"
              >
                <div className="bg-gradient-to-r from-emerald-500 to-green-600 rounded-2xl p-6 text-white">
                  <div className="flex items-center gap-3 mb-2">
                    <CreditCard className="w-6 h-6" />
                    <h4 className="font-semibold">UPI Payment Link</h4>
                  </div>
                  <p className="text-emerald-100 mb-3">Share this UPI link with your customers for instant payments</p>
                  <div className="bg-white/20 rounded-xl px-4 py-2 font-mono">
                    {payments.upiId}
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider">
                    Bank Account Details
                  </h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-2">
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Bank Name</label>
                      <input
                        type="text"
                        value={payments.bankName}
                        onChange={(e) => setPayments({ ...payments, bankName: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="col-span-2">
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Account Number</label>
                      <input
                        type="text"
                        value={payments.accountNumber}
                        onChange={(e) => setPayments({ ...payments, accountNumber: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">IFSC Code</label>
                      <input
                        type="text"
                        value={payments.ifsc}
                        onChange={(e) => setPayments({ ...payments, ifsc: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Account Type</label>
                      <select
                        value={payments.accountType}
                        onChange={(e) => setPayments({ ...payments, accountType: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="Current Account">Current Account</option>
                        <option value="Savings Account">Savings Account</option>
                      </select>
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </motion.div>
            )}

            {/* Notifications Tab */}
            {activeTab === 'notifications' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-2xl space-y-6"
              >
                <div className="space-y-4">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                    <Mail className="w-4 h-4" />
                    Email Notifications
                  </h4>
                  <div className="space-y-3">
                    {[
                      { key: 'emailLowStock', label: 'Low stock alerts', desc: 'Get notified when products are running low' },
                      { key: 'emailPaymentReminders', label: 'Payment reminders', desc: 'Reminders for pending invoices' },
                      { key: 'emailDailySummary', label: 'Daily summary', desc: 'Receive daily business summary report' }
                    ].map(item => (
                      <div key={item.key} className="flex items-center justify-between p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50">
                        <div>
                          <p className="font-medium text-slate-900 dark:text-white">{item.label}</p>
                          <p className="text-sm text-slate-500">{item.desc}</p>
                        </div>
                        <button
                          onClick={() => setNotifications({ ...notifications, [item.key]: !notifications[item.key as keyof typeof notifications] })}
                          className={`w-12 h-6 rounded-full transition-all ${
                            notifications[item.key as keyof typeof notifications]
                              ? 'bg-blue-600'
                              : 'bg-slate-300 dark:bg-slate-600'
                          }`}
                        >
                          <div className={`w-5 h-5 rounded-full bg-white transition-all ${
                            notifications[item.key as keyof typeof notifications] ? 'translate-x-6' : 'translate-x-0.5'
                          }`} />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-700">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                    <Bell className="w-4 h-4" />
                    Push Notifications
                  </h4>
                  <div className="space-y-3">
                    {[
                      { key: 'pushAlerts', label: 'Critical alerts', desc: 'Immediate alerts for urgent matters' },
                      { key: 'pushUpdates', label: 'System updates', desc: 'Notifications about new features' },
                      { key: 'pushMarketing', label: 'Marketing emails', desc: 'Product updates and offers' }
                    ].map(item => (
                      <div key={item.key} className="flex items-center justify-between p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50">
                        <div>
                          <p className="font-medium text-slate-900 dark:text-white">{item.label}</p>
                          <p className="text-sm text-slate-500">{item.desc}</p>
                        </div>
                        <button
                          onClick={() => setNotifications({ ...notifications, [item.key]: !notifications[item.key as keyof typeof notifications] })}
                          className={`w-12 h-6 rounded-full transition-all ${
                            notifications[item.key as keyof typeof notifications]
                              ? 'bg-blue-600'
                              : 'bg-slate-300 dark:bg-slate-600'
                          }`}
                        >
                          <div className={`w-5 h-5 rounded-full bg-white transition-all ${
                            notifications[item.key as keyof typeof notifications] ? 'translate-x-6' : 'translate-x-0.5'
                          }`} />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </motion.div>
            )}

            {/* Security Tab */}
            {activeTab === 'security' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-2xl space-y-6"
              >
                <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-2xl p-4 flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-medium text-amber-900 dark:text-amber-400">Security Tips</p>
                    <p className="text-sm text-amber-700 dark:text-amber-300 mt-1">Use strong passwords and enable two-factor authentication for better security.</p>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                    <Key className="w-4 h-4" />
                    Two-Factor Authentication
                  </h4>
                  <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-slate-900 dark:text-white">2FA Status</p>
                        <p className="text-sm text-slate-500">Add an extra layer of security to your account</p>
                      </div>
                      <button
                        onClick={() => setSecurity({ ...security, twoFactorEnabled: !security.twoFactorEnabled })}
                        className={`w-12 h-6 rounded-full transition-all ${
                          security.twoFactorEnabled
                            ? 'bg-blue-600'
                            : 'bg-slate-300 dark:bg-slate-600'
                        }`}
                      >
                        <div className={`w-5 h-5 rounded-full bg-white transition-all ${
                          security.twoFactorEnabled ? 'translate-x-6' : 'translate-x-0.5'
                        }`} />
                      </button>
                    </div>
                  </div>
                </div>

                <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-700">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider">
                    Session Settings
                  </h4>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Auto Logout (minutes)</label>
                    <select
                      value={security.sessionTimeout}
                      onChange={(e) => setSecurity({ ...security, sessionTimeout: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="15">15 minutes</option>
                      <option value="30">30 minutes</option>
                      <option value="60">1 hour</option>
                      <option value="120">2 hours</option>
                    </select>
                  </div>
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </motion.div>
            )}

            {/* Preferences Tab */}
            {activeTab === 'preferences' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-2xl space-y-6"
              >
                <div className="space-y-4">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                    <Globe className="w-4 h-4" />
                    Language & Region
                  </h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Language</label>
                      <select
                        value={preferences.language}
                        onChange={(e) => setPreferences({ ...preferences, language: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="en">English</option>
                        <option value="hi">Hindi (हिंदी)</option>
                        <option value="gu">Gujarati (ગુજરાતી)</option>
                        <option value="mr">Marathi (मराठी)</option>
                        <option value="ta">Tamil (தமிழ்)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Timezone</label>
                      <select
                        value={business.timezone}
                        onChange={(e) => setBusiness({ ...business, timezone: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="Asia/Kolkata">Asia/Kolkata</option>
                        <option value="Asia/Dubai">Asia/Dubai</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-700">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                    <Palette className="w-4 h-4" />
                    Display
                  </h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Date Format</label>
                      <select
                        value={preferences.dateFormat}
                        onChange={(e) => setPreferences({ ...preferences, dateFormat: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                        <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                        <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Number Format</label>
                      <select
                        value={preferences.numberFormat}
                        onChange={(e) => setPreferences({ ...preferences, numberFormat: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="en-IN">Indian (1,23,456.78)</option>
                        <option value="en-US">US (123,456.78)</option>
                        <option value="de-DE">European (123.456,78)</option>
                      </select>
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </motion.div>
            )}

            {/* Data Management Tab */}
            {activeTab === 'data' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-2xl space-y-6"
              >
                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-2xl p-4 flex items-start gap-3">
                  <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-medium text-blue-900 dark:text-blue-400">Data Management</p>
                    <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">Export your data or manage your account data here.</p>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                    <Download className="w-4 h-4" />
                    Export Data
                  </h4>
                  <div className="grid grid-cols-2 gap-4">
                    <button className="p-4 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 hover:bg-slate-50 dark:hover:bg-slate-600 transition-all text-left">
                      <p className="font-medium text-slate-900 dark:text-white">Financial Data</p>
                      <p className="text-sm text-slate-500">Export transactions & reports</p>
                    </button>
                    <button className="p-4 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 hover:bg-slate-50 dark:hover:bg-slate-600 transition-all text-left">
                      <p className="font-medium text-slate-900 dark:text-white">Inventory Data</p>
                      <p className="text-sm text-slate-500">Export products & movements</p>
                    </button>
                    <button className="p-4 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 hover:bg-slate-50 dark:hover:bg-slate-600 transition-all text-left">
                      <p className="font-medium text-slate-900 dark:text-white">Customer Data</p>
                      <p className="text-sm text-slate-500">Export customer list</p>
                    </button>
                    <button className="p-4 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 hover:bg-slate-50 dark:hover:bg-slate-600 transition-all text-left">
                      <p className="font-medium text-slate-900 dark:text-white">Complete Backup</p>
                      <p className="text-sm text-slate-500">Export all data (JSON)</p>
                    </button>
                  </div>
                </div>

                <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-700">
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2 text-red-600">
                    <Trash2 className="w-4 h-4" />
                    Danger Zone
                  </h4>
                  <div className="p-4 rounded-xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20">
                    <p className="font-medium text-red-900 dark:text-red-400 mb-1">Delete Account</p>
                    <p className="text-sm text-red-700 dark:text-red-300 mb-3">Permanently delete your account and all associated data. This action cannot be undone.</p>
                    <button className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 transition-colors">
                      Delete Account
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};