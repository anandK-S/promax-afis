// ========================================
// Pro-Max AFIS - Register Page
// ========================================
// Premium registration page
// ========================================

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { toast } from 'react-hot-toast';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register, isLoading } = useAuth();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    password: '',
    confirm_password: '',
    business_name: '',
    business_type: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!formData.first_name || !formData.last_name || !formData.email || !formData.password || !formData.business_name) {
      toast.error('Please fill in all required fields');
      return;
    }

    if (formData.password.length < 12) {
      toast.error('Password must be at least 12 characters long');
      return;
    }

    if (formData.password !== formData.confirm_password) {
      toast.error('Passwords do not match');
      return;
    }

    setIsSubmitting(true);

    try {
      await register(formData);
      toast.success('Account created successfully! Redirecting to dashboard...');
      setTimeout(() => navigate('/dashboard'), 1500);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-slate-900 dark:via-blue-900 dark:to-purple-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
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

      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
            className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-xl"
          >
            <span className="text-white text-4xl font-bold">P</span>
          </motion.div>
          <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-2">
            Create Your Account
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-400">
            Start your journey with Pro-Max AFIS
          </p>
        </div>

        {/* Registration Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white dark:bg-slate-800 rounded-3xl shadow-2xl p-8 md:p-12 border border-slate-200 dark:border-slate-700"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Personal Information */}
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
                Personal Information
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    First Name *
                  </label>
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    placeholder="John"
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Last Name *
                  </label>
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    placeholder="Doe"
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="john@example.com"
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="+91 98765 43210"
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400"
                  />
                </div>
              </div>
            </div>

            {/* Password */}
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
                Password
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Password * (min 12 characters)
                  </label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Enter a strong password"
                      className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400 pr-12"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                    >
                      {showPassword ? '👁️' : '👁️‍🗨️'}
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Confirm Password *
                  </label>
                  <input
                    type="password"
                    name="confirm_password"
                    value={formData.confirm_password}
                    onChange={handleChange}
                    placeholder="Confirm your password"
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Business Information */}
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
                Business Information
              </h3>
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Business Name *
                  </label>
                  <input
                    type="text"
                    name="business_name"
                    value={formData.business_name}
                    onChange={handleChange}
                    placeholder="Your Business Name"
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white placeholder-slate-400"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Business Type
                  </label>
                  <select
                    name="business_type"
                    value={formData.business_type}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-slate-900 dark:text-white"
                  >
                    <option value="">Select business type</option>
                    <option value="retail">Retail</option>
                    <option value="wholesale">Wholesale</option>
                    <option value="manufacturing">Manufacturing</option>
                    <option value="service">Service Provider</option>
                    <option value="restaurant">Restaurant/Food</option>
                    <option value="ecommerce">E-commerce</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Terms & Conditions */}
            <div>
              <label className="flex items-start gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  className="w-5 h-5 text-blue-600 rounded border-slate-300 focus:ring-blue-500 mt-0.5"
                  required
                />
                <span className="text-sm text-slate-600 dark:text-slate-400">
                  I agree to the{' '}
                  <Link to="/terms" className="text-blue-600 hover:text-blue-700 font-medium">
                    Terms of Service
                  </Link>
                  {' '}and{' '}
                  <Link to="/privacy" className="text-blue-600 hover:text-blue-700 font-medium">
                    Privacy Policy
                  </Link>
                </span>
              </label>
            </div>

            {/* Submit Button */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={isSubmitting}
              className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-lg rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isSubmitting ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Creating Account...
                </>
              ) : (
                'Create Account'
              )}
            </motion.button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center gap-4">
            <div className="flex-1 h-px bg-slate-200 dark:bg-slate-700" />
            <span className="text-sm text-slate-500 dark:text-slate-400">or</span>
            <div className="flex-1 h-px bg-slate-200 dark:border-slate-700" />
          </div>

          {/* Sign In Link */}
          <div className="text-center">
            <p className="text-slate-600 dark:text-slate-400">
              Already have an account?{' '}
              <Link
                to="/login"
                className="text-blue-600 hover:text-blue-700 font-semibold"
              >
                Sign in
              </Link>
            </p>
          </div>
        </motion.div>

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
      </div>
    </div>
  );
};