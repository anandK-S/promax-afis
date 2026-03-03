// ========================================
// Pro-Max AFIS - Landing Page
// ========================================
// Premium landing page with wow factor
// ========================================

import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';

export const LandingPage: React.FC = () => {
  const { theme } = useTheme();

  const features = [
    {
      icon: '🤖',
      title: 'AI-Powered Insights',
      description: 'Advanced machine learning algorithms analyze your financial data to provide actionable insights and predictions.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: '📊',
      title: 'Real-Time Dashboard',
      description: 'Live financial monitoring with beautiful visualizations and instant updates across all devices.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: '🎤',
      title: 'Voice Intelligence',
      description: 'Natural voice commands in 10+ Indian languages. Just speak and get instant financial insights.',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: '📈',
      title: 'Smart Forecasting',
      description: 'Ensemble ML models predict sales, cash flow, and inventory needs with 95%+ accuracy.',
      color: 'from-orange-500 to-red-500'
    },
    {
      icon: '🔒',
      title: 'Bank-Grade Security',
      description: 'Enterprise-level security with JWT authentication, Argon2 encryption, and role-based access control.',
      color: 'from-indigo-500 to-purple-500'
    },
    {
      icon: '📦',
      title: 'Smart Inventory',
      description: 'Automatic low-stock alerts, intelligent reordering, and comprehensive inventory management.',
      color: 'from-teal-500 to-cyan-500'
    }
  ];

  const stats = [
    { value: '95%+', label: 'Forecast Accuracy' },
    { value: '10+', label: 'Indian Languages' },
    { value: '50+', label: 'ML Models' },
    { value: '24/7', label: 'AI Monitoring' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-slate-900 dark:via-blue-900 dark:to-purple-900">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              rotate: [0, 90, 0],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear"
            }}
            className="absolute -top-1/2 -right-1/2 w-full h-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1.2, 1, 1.2],
              rotate: [90, 0, 90],
            }}
            transition={{
              duration: 25,
              repeat: Infinity,
              ease: "linear"
            }}
            className="absolute -bottom-1/2 -left-1/2 w-full h-full bg-gradient-to-tr from-green-500/20 to-cyan-500/20 rounded-full blur-3xl"
          />
        </div>

        {/* Content */}
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-800 rounded-full shadow-lg mb-8"
            >
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Powered by Advanced AI & Machine Learning
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-5xl sm:text-6xl md:text-7xl font-bold mb-6"
            >
              <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                Pro-Max AFIS
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-xl sm:text-2xl md:text-3xl text-slate-700 dark:text-slate-300 mb-8"
            >
              Autonomous Financial Intelligence System
              <br />
              <span className="text-lg md:text-xl text-slate-600 dark:text-slate-400">
                Transforming MSMEs with AI-Powered Financial Management
              </span>
            </motion.p>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="text-lg text-slate-600 dark:text-slate-400 max-w-3xl mx-auto mb-12"
            >
              Experience the future of financial management. Our AI-powered system provides
              real-time insights, predictive analytics, voice commands, and intelligent
              automation - all in one powerful platform.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <Link
                to="/register"
                className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-lg rounded-xl shadow-2xl hover:shadow-3xl transition-all duration-300 transform hover:scale-105"
              >
                Get Started Free
              </Link>
              <Link
                to="/login"
                className="w-full sm:w-auto px-8 py-4 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-lg rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-2 border-slate-200 dark:border-slate-700"
              >
                Sign In
              </Link>
            </motion.div>
          </div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.05 }}
                className="bg-white dark:bg-slate-800 rounded-2xl p-6 text-center shadow-xl hover:shadow-2xl transition-all duration-300"
              >
                <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-slate-600 dark:text-slate-400">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
              Powerful Features
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-400">
              Everything you need to manage your finances intelligently
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05, y: -10 }}
                className="group bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-700 rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300 border-2 border-transparent hover:border-blue-500"
              >
                <motion.div
                  whileHover={{ scale: 1.2, rotate: 5 }}
                  className={`w-16 h-16 bg-gradient-to-br ${feature.color} rounded-2xl flex items-center justify-center text-3xl mb-6 shadow-lg group-hover:shadow-xl transition-all`}
                >
                  {feature.icon}
                </motion.div>
                <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl text-white/90 mb-8">
              Join thousands of MSMEs already using Pro-Max AFIS to manage their finances smarter
            </p>
            <Link
              to="/register"
              className="inline-block px-12 py-4 bg-white text-blue-600 font-bold text-lg rounded-xl shadow-2xl hover:shadow-3xl transition-all duration-300 transform hover:scale-105"
            >
              Start Free Trial
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="text-2xl font-bold mb-4">Pro-Max AFIS</div>
          <p className="text-slate-400 mb-6">
            Autonomous Financial Intelligence System for MSMEs
          </p>
          <div className="text-sm text-slate-500">
            © 2024 Pro-Max AFIS. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};