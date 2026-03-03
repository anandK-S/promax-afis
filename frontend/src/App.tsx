// ========================================
// Pro-Max AFIS - Main Application Component
// ========================================
// Enterprise-grade React application
// ========================================

import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { AuthProvider } from './contexts/AuthContext';
import { WebSocketProvider } from './contexts/WebSocketContext';
import { LoadingScreen } from './components/common/LoadingScreen';
import { ErrorBoundary } from './components/common/ErrorBoundary';

// Lazy load pages for better performance
const LandingPage = lazy(() => import('./pages/LandingPage'));
const LoginPage = lazy(() => import('./pages/auth/LoginPage'));
const RegisterPage = lazy(() => import('./pages/auth/RegisterPage'));
const Dashboard = lazy(() => import('./pages/dashboard/Dashboard'));
const Financials = lazy(() => import('./pages/financials/Financials'));
const Inventory = lazy(() => import('./pages/inventory/Inventory'));
const AIChat = lazy(() => import('./pages/ai/AIChat'));
const VoiceInsights = lazy(() => import('./pages/ai/VoiceInsights'));
const Reports = lazy(() => import('./pages/reports/Reports'));
const Settings = lazy(() => import('./pages/settings/Settings'));
const NotFound = lazy(() => import('./pages/NotFound'));

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const isAuthenticated = localStorage.getItem('token') !== null;
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

// App Component
function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <WebSocketProvider>
            <Router>
              <Suspense fallback={<LoadingScreen />}>
                <Routes>
                  {/* Public Routes */}
                  <Route path="/" element={<LandingPage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  
                  {/* Protected Routes */}
                  <Route
                    path="/dashboard"
                    element={
                      <ProtectedRoute>
                        <Dashboard />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/financials"
                    element={
                      <ProtectedRoute>
                        <Financials />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/inventory"
                    element={
                      <ProtectedRoute>
                        <Inventory />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/ai-chat"
                    element={
                      <ProtectedRoute>
                        <AIChat />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/voice-insights"
                    element={
                      <ProtectedRoute>
                        <VoiceInsights />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/reports"
                    element={
                      <ProtectedRoute>
                        <Reports />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/settings"
                    element={
                      <ProtectedRoute>
                        <Settings />
                      </ProtectedRoute>
                    }
                  />
                  
                  {/* 404 Not Found */}
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Suspense>
            </Router>
          </WebSocketProvider>
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;