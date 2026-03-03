// ========================================
// Pro-Max AFIS - Authentication Context
// ========================================
// User authentication state management
// ========================================

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiClient } from '../services/api';

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  avatar_url?: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  business_id?: number;
  created_at: string;
  updated_at: string;
  last_login?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const savedToken = localStorage.getItem('token');
      if (savedToken) {
        try {
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`;
          const response = await apiClient.get('/auth/me');
          setUser(response.data.user);
          setToken(savedToken);
        } catch (error) {
          localStorage.removeItem('token');
          setToken(null);
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      const { access_token, refresh_token, user: userData } = response.data;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      setToken(access_token);
      setUser(userData);
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData: any) => {
    try {
      const response = await apiClient.post('/auth/register', userData);
      // Auto-login after registration
      await login(userData.email, userData.password);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    delete apiClient.defaults.headers.common['Authorization'];
    setToken(null);
    setUser(null);
  };

  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      const response = await apiClient.post('/auth/refresh', { refresh_token });
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      setToken(access_token);
    } catch (error) {
      logout();
      throw error;
    }
  };

  const updateUser = (userData: Partial<User>) => {
    if (user) {
      setUser({ ...user, ...userData });
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token,
        isLoading,
        login,
        register,
        logout,
        refreshToken,
        updateUser
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};