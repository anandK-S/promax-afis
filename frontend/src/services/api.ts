// ========================================
// Pro-Max AFIS - API Service
// ========================================
// HTTP client for backend API communication
// ========================================

import axios, { AxiosInstance, AxiosError } from 'axios';
import { toast } from 'react-hot-toast';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await apiClient.post('/auth/refresh', { refresh_token });
          const { access_token } = response.data;
          
          localStorage.setItem('token', access_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }

    // Handle other errors
    let errorMessage = 'An error occurred';
    
    if (error.response) {
      const errorData = error.response.data as any;
      errorMessage = errorData.detail || errorData.message || errorMessage;
    } else if (error.request) {
      errorMessage = 'Network error. Please check your connection.';
    }

    toast.error(errorMessage);
    return Promise.reject(error);
  }
);

// API Service
export const apiService = {
  // Authentication
  auth: {
    login: (email: string, password: string) =>
      apiClient.post('/auth/login', { email, password }),
    
    register: (userData: any) =>
      apiClient.post('/auth/register', userData),
    
    logout: () =>
      apiClient.post('/auth/logout'),
    
    getMe: () =>
      apiClient.get('/auth/me'),
    
    refreshToken: (refreshToken: string) =>
      apiClient.post('/auth/refresh', { refresh_token: refreshToken }),
  },

  // Financials
  financials: {
    getTransactions: (params?: any) =>
      apiClient.get('/financials/transactions', { params }),
    
    createTransaction: (data: any) =>
      apiClient.post('/financials/transactions', data),
    
    updateTransaction: (id: number, data: any) =>
      apiClient.put(`/financials/transactions/${id}`, data),
    
    deleteTransaction: (id: number) =>
      apiClient.delete(`/financials/transactions/${id}`),
    
    getSummary: (params: any) =>
      apiClient.get('/financials/summary', { params }),
    
    getProfitLoss: (params: any) =>
      apiClient.get('/financials/profit-loss', { params }),
    
    getCashFlow: (params: any) =>
      apiClient.get('/financials/cash-flow', { params }),
    
    getCategories: () =>
      apiClient.get('/financials/categories'),
  },

  // Inventory
  inventory: {
    getProducts: (params?: any) =>
      apiClient.get('/inventory/products', { params }),
    
    createProduct: (data: any) =>
      apiClient.post('/inventory/products', data),
    
    updateProduct: (id: number, data: any) =>
      apiClient.put(`/inventory/products/${id}`, data),
    
    deleteProduct: (id: number) =>
      apiClient.delete(`/inventory/products/${id}`),
    
    getMovements: (params?: any) =>
      apiClient.get('/inventory/movements', { params }),
    
    createMovement: (data: any) =>
      apiClient.post('/inventory/movements', data),
    
    getAlerts: (params?: any) =>
      apiClient.get('/inventory/alerts/low-stock', { params }),
    
    resolveAlert: (id: number) =>
      apiClient.put(`/inventory/alerts/${id}/resolve`),
    
    getSummary: () =>
      apiClient.get('/inventory/summary'),
  },

  // Machine Learning
  ml: {
    forecastSales: (params: any) =>
      apiClient.post('/ml/forecast/sales', params),
    
    getHealthScore: () =>
      apiClient.get('/ml/financial-health'),
    
    chat: (data: any) =>
      apiClient.post('/ml/agent/chat', data),
    
    voiceInsight: (data: any) =>
      apiClient.post('/ml/voice/insight', data),
    
    categorize: (data: any) =>
      apiClient.post('/ml/categorize', data),
    
    getAnomalies: (params?: any) =>
      apiClient.get('/ml/anomalies', { params }),
    
    simulate: (data: any) =>
      apiClient.post('/ml/simulate', data),
  },

  // WebSocket (for reference)
  websocket: {
    connect: (token: string) => {
      const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
      return new WebSocket(`${wsUrl}?token=${token}`);
    },
  },
};

export { apiClient };
export default apiClient;