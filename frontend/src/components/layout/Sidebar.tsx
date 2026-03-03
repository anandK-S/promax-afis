// ========================================
// Pro-Max AFIS - Sidebar Component
// ========================================
// Premium navigation sidebar with animations
// ========================================

import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { useWebSocket } from '../../contexts/WebSocketContext';

const menuItems = [
  { path: '/dashboard', icon: '📊', label: 'Dashboard', description: 'Overview & insights' },
  { path: '/financials', icon: '💰', label: 'Financials', description: 'Transactions & reports' },
  { path: '/inventory', icon: '📦', label: 'Inventory', description: 'Stock & products' },
  { path: '/ai-chat', icon: '🤖', label: 'AI Assistant', description: 'Chat & insights' },
  { path: '/voice-insights', icon: '🎤', label: 'Voice Insights', description: 'Voice commands' },
  { path: '/reports', icon: '📈', label: 'Reports', description: 'Analytics & forecasts' },
  { path: '/settings', icon: '⚙️', label: 'Settings', description: 'Preferences' },
];

export const Sidebar: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const location = useLocation();
  const { user } = useAuth();
  const { theme } = useTheme();
  const { isConnected } = useWebSocket();

  return (
    <>
      {/* Desktop Sidebar */}
      <motion.aside
        initial={false}
        animate={{ width: isOpen ? '260px' : '80px' }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="hidden md:flex flex-col h-screen bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 shadow-xl z-40"
      >
        {/* Logo */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-700">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center gap-3"
          >
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg">
              <span className="text-white font-bold text-lg">P</span>
            </div>
            <AnimatePresence>
              {isOpen && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="overflow-hidden"
                >
                  <h1 className="text-xl font-bold text-slate-900 dark:text-white">
                    Pro-Max AFIS
                  </h1>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Financial Intelligence
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path;
            
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => `
                  relative group flex items-center gap-3 p-3 rounded-xl transition-all duration-200
                  ${isActive 
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg' 
                    : 'hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300'
                  }
                `}
              >
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  className="text-2xl flex-shrink-0"
                >
                  {item.icon}
                </motion.div>
                
                <AnimatePresence>
                  {isOpen && (
                    <motion.div
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -10 }}
                      className="overflow-hidden flex-1"
                    >
                      <div className="font-semibold text-sm">{item.label}</div>
                      <div className={`text-xs ${isActive ? 'text-white/80' : 'text-slate-500 dark:text-slate-400'}`}>
                        {item.description}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
                
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute inset-0 rounded-xl"
                    initial={false}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* User Profile */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center text-white font-semibold flex-shrink-0">
              {user?.first_name?.[0] || 'U'}
            </div>
            
            <AnimatePresence>
              {isOpen && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="overflow-hidden flex-1 min-w-0"
                >
                  <div className="font-semibold text-sm text-slate-900 dark:text-white truncate">
                    {user?.first_name} {user?.last_name}
                  </div>
                  <div className="text-xs text-slate-500 dark:text-slate-400 truncate">
                    {user?.email}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </motion.aside>

      {/* Mobile Sidebar Overlay */}
      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={onClose}
              className="fixed inset-0 bg-black/50 md:hidden z-30"
            />
            
            <motion.aside
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed left-0 top-0 h-full w-72 bg-white dark:bg-slate-800 shadow-2xl md:hidden z-40 flex flex-col"
            >
              {/* Mobile Logo */}
              <div className="p-6 border-b border-slate-200 dark:border-slate-700">
                <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                  Pro-Max AFIS
                </h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  Financial Intelligence
                </p>
              </div>

              {/* Mobile Navigation */}
              <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
                {menuItems.map((item) => {
                  const isActive = location.pathname === item.path;
                  
                  return (
                    <NavLink
                      key={item.path}
                      to={item.path}
                      onClick={onClose}
                      className={`
                        relative group flex items-center gap-3 p-4 rounded-xl transition-all duration-200
                        ${isActive 
                          ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg' 
                          : 'hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300'
                        }
                      `}
                    >
                      <span className="text-2xl">{item.icon}</span>
                      <div>
                        <div className="font-semibold">{item.label}</div>
                        <div className={`text-xs ${isActive ? 'text-white/80' : 'text-slate-500 dark:text-slate-400'}`}>
                          {item.description}
                        </div>
                      </div>
                    </NavLink>
                  );
                })}
              </nav>

              {/* Mobile User Profile */}
              <div className="p-4 border-t border-slate-200 dark:border-slate-700">
                <div className="flex items-center gap-3 p-3 bg-slate-100 dark:bg-slate-700 rounded-xl">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center text-white font-semibold">
                    {user?.first_name?.[0] || 'U'}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-slate-900 dark:text-white truncate">
                      {user?.first_name} {user?.last_name}
                    </div>
                    <div className="text-xs text-slate-500 dark:text-slate-400 truncate">
                      {user?.email}
                    </div>
                  </div>
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
};