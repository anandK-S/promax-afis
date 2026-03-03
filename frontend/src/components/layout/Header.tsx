// ========================================
// Pro-Max AFIS - Header Component
// ========================================
// Premium top navigation bar
// ========================================

import React from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { useWebSocket } from '../../contexts/WebSocketContext';

interface HeaderProps {
  onMenuClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { isConnected } = useWebSocket();

  return (
    <header className="fixed top-0 right-0 left-0 md:left-auto md:right-0 md:w-[calc(100%-260px)] bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 shadow-md z-30 transition-all duration-300">
      <div className="h-16 flex items-center justify-between px-4 md:px-6">
        {/* Left Section - Mobile Menu &amp; Search */}
        <div className="flex items-center gap-4">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onMenuClick}
            className="md:hidden p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
          >
            <svg className="w-6 h-6 text-slate-700 dark:text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </motion.button>

          {/* Search Bar */}
          <div className="hidden sm:flex items-center gap-2 bg-slate-100 dark:bg-slate-700 rounded-xl px-4 py-2 flex-1 max-w-md">
            <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              placeholder="Search transactions, products, reports..."
              className="bg-transparent border-none outline-none text-sm text-slate-700 dark:text-slate-300 flex-1 placeholder-slate-400"
            />
          </div>
        </div>

        {/* Right Section - Actions */}
        <div className="flex items-center gap-2 md:gap-4">
          {/* Connection Status */}
          <div className="hidden md:flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
            <span className="text-xs text-slate-500 dark:text-slate-400">
              {isConnected ? 'Live' : 'Offline'}
            </span>
          </div>

          {/* Theme Toggle */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleTheme}
            className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
            title="Toggle theme"
          >
            {theme === 'light' ? (
              <svg className="w-5 h-5 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            ) : (
              <svg className="w-5 h-5 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            )}
          </motion.button>

          {/* Notifications */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="relative p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
          >
            <svg className="w-5 h-5 text-slate-700 dark:text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
          </motion.button>

          {/* User Menu */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={logout}
            className="hidden md:flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl shadow-lg hover:shadow-xl transition-all"
          >
            <span className="text-sm font-semibold">Logout</span>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </motion.button>
        </div>
      </div>
    </header>
  );
};