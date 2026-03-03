// ========================================
// Pro-Max AFIS - WebSocket Context
// ========================================
// Real-time data synchronization
// ========================================

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAuth } from './AuthContext';

interface WebSocketContextType {
  socket: Socket | null;
  isConnected: boolean;
  reconnect: () => void;
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

export const WebSocketProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const { token, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated || !token) {
      if (socket) {
        socket.disconnect();
        setSocket(null);
        setIsConnected(false);
      }
      return;
    }

    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
    
    const newSocket = io(wsUrl, {
      auth: { token },
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    newSocket.on('connect', () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    });

    newSocket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    newSocket.on('message', (data) => {
      console.log('WebSocket message:', data);
      // Handle different message types
      switch (data.event) {
        case 'transaction_created':
          // Handle new transaction
          break;
        case 'financial_alert':
          // Handle financial alert
          break;
        case 'inventory_alert':
          // Handle inventory alert
          break;
        case 'dashboard_update':
          // Handle dashboard update
          break;
        default:
          console.log('Unknown event:', data.event);
      }
    });

    setSocket(newSocket);

    return () => {
      newSocket.disconnect();
    };
  }, [isAuthenticated, token]);

  const reconnect = () => {
    if (socket) {
      socket.connect();
    }
  };

  return (
    <WebSocketContext.Provider value={{ socket, isConnected, reconnect }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (context === undefined) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};