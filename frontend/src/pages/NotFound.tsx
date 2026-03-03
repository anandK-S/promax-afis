// ========================================
// Pro-Max AFIS - 404 Not Found Page
// ========================================

import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-slate-900 dark:via-blue-900 dark:to-purple-900 p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <motion.div
          animate={{ 
            scale: [1, 1.1, 1],
            rotate: [0, 5, -5, 0],
          }}
          transition={{ 
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="text-9xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4"
        >
          404
        </motion.div>
        
        <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-4">
          Page Not Found
        </h1>
        
        <p className="text-xl text-slate-600 dark:text-slate-400 mb-8">
          Oops! The page you're looking for doesn't exist.
        </p>
        
        <Link
          to="/"
          className="inline-block px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
        >
          Go Back Home
        </Link>
      </motion.div>
    </div>
  );
};