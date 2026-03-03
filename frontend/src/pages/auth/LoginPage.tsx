// ========================================
// Pro-Max AFIS - Login Page
// ========================================
// Premium authentication page
// ========================================

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { toast } from 'react-hot-toast';
import { LoadingScreen } from '../../components/common/LoadingScreen';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      toast.error('Please fill in all fields');
      return;
    }

    setIsSubmitting(true);
    
    try {
      await login(email, password);
      toast.success('Welcome back! Redirecting to dashboard...');
      setTimeout(() => navigate('/dashboard'), 1000);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-slate-900 dark:via-blue-900 dark:to-purple-900 p-4">
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
          className="absolute -top-1/2 -right-1/2 w-full h-full bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-full blur-3xl"
        />
      </div>

      {/* Login Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative w-full max-w-md"
      >
        <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-2xl p-8 md:p-12 border border-slate-200 dark:border-slate-700">
          {/* Logo */}
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-xl"
            >
              <span className="text-white text-4xl font-bold">P</span>
            </motion.div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
              Welcome Back
            </h1>
            <p className="text-slate-600 dark:text-slate-400">
              Sign in to your Pro-Max AFIS account
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Field */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                Email Address
              </label>
              <div className="relative">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400"
                  required
                />
                <svg
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
                  />
                </svg>
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400 pr-12"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                >
                  {showPassword ? (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"
                />
                <span className="text-sm text-slate-600 dark:text-slate-400">Remember me</span>
              </label>
              <Link
                to="/forgot-password"
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                Forgot password?
              </Link>
            </div>

            {/* Submit Button */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isSubmitting ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </motion.button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center gap-4">
            <div className="flex-1 h-px bg-slate-200 dark:bg-slate-700" />
            <span className="text-sm text-slate-500 dark:text-slate-400">or</span>
            <div className="flex-1 h-px bg-slate-200 dark:bg-slate-700" />
          </div>

          {/* Sign Up Link */}
          <div className="text-center">
            <p className="text-slate-600 dark:text-slate-400">
              Don't have an account?{' '}
              <Link
                to="/register"
                className="text-blue-600 hover:text-blue-700 font-semibold"
              >
                Sign up for free
              </Link>
            </p>
          </div>
        </div>

        {/* Back to Home */}
        <div className="mt-6 text-center">
          <Link
            to="/"
            className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors inline-flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Home
          </Link>
        </div>
      </motion.div>
    </div>
  );
};