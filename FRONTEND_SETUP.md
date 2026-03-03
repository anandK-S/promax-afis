# 🚀 Pro-Max AFIS - Frontend Setup Guide

## 📋 Overview

This guide will help you set up and run the Pro-Max AFIS frontend application. The frontend is built with React, TypeScript, Tailwind CSS, and Framer Motion for animations.

---

## 🎨 Features Implemented

### ✅ Core Infrastructure
- **React 18** with TypeScript for type safety
- **Vite** for fast development and optimized builds
- **Tailwind CSS** for utility-first styling
- **Framer Motion** for smooth animations
- **React Router** for navigation
- **Axios** for API communication
- **Socket.io Client** for real-time WebSocket connections
- **React Hot Toast** for notifications
- **Recharts** for beautiful charts and visualizations

### ✅ Design System
- **Premium Glass Morphism Effects**
- **Gradient Backgrounds & Buttons**
- **Dark/Light Mode Support**
- **Responsive Design** (Mobile & Desktop)
- **Smooth Micro-animations**
- **Enterprise-grade UI Components**
- **Color Palette**: Professional blue, purple, green, and accent colors

### ✅ Pages Created
1. **Landing Page** - Stunning hero section with animated backgrounds
2. **Login Page** - Premium authentication with password visibility toggle
3. **Register Page** - Comprehensive registration with validation
4. **Dashboard** - Command center with charts, stats, and AI insights
5. **Financials** - Placeholder (to be implemented)
6. **Inventory** - Placeholder (to be implemented)
7. **AI Chat** - Placeholder (to be implemented)
8. **Voice Insights** - Placeholder (to be implemented)
9. **Reports** - Placeholder (to be implemented)
10. **Settings** - Placeholder (to be implemented)
11. **404 Not Found** - Custom error page

### ✅ Components Created
- **Sidebar** - Animated navigation with collapsible design
- **Header** - Top navigation with search, notifications, theme toggle
- **Layout** - Main layout wrapper
- **LoadingScreen** - Premium loading animation
- **ErrorBoundary** - Global error handling
- **Cards, Buttons, Inputs** - Reusable UI components

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js 20+** - [Download](https://nodejs.org/)
- **npm 10+** - Comes with Node.js
- **Git** - [Download](https://git-scm.com/)

---

## 🔧 Installation Steps

### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install all the required packages from package.json, including:
- React & React Router
- TypeScript & Vite
- Tailwind CSS
- Framer Motion
- Axios
- Socket.io Client
- Recharts
- And more...

### Step 3: Create Environment File

Create a `.env` file in the frontend directory:

```bash
# API Configuration
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws

# Feature Flags
VITE_ENABLE_VOICE=true
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_MULTI_LANGUAGE=true
```

### Step 4: Start Development Server

```bash
npm run dev
```

The application will be available at: **http://localhost:5173**

---

## 🎯 Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint

# Run type checking
npm run type-check

# Format code
npm run format
```

---

## 📂 Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable components
│   │   ├── common/      # Common components (LoadingScreen, ErrorBoundary)
│   │   └── layout/      # Layout components (Sidebar, Header, Layout)
│   ├── contexts/        # React contexts (Theme, Auth, WebSocket)
│   ├── pages/           # Page components
│   │   ├── auth/        # Authentication pages (Login, Register)
│   │   ├── dashboard/   # Dashboard page
│   │   ├── financials/  # Financials page
│   │   ├── inventory/   # Inventory page
│   │   ├── ai/          # AI pages (Chat, Voice)
│   │   ├── reports/     # Reports page
│   │   └── settings/    # Settings page
│   ├── services/        # API services
│   ├── styles/          # Global styles
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── index.html           # HTML template
├── package.json         # Dependencies
├── tsconfig.json        # TypeScript config
├── tailwind.config.js   # Tailwind config
└── vite.config.ts       # Vite config
```

---

## 🎨 Design System

### Colors

```css
/* Primary Colors */
--color-primary: #1e40af;
--color-primary-light: #3b82f6;
--color-primary-dark: #1e3a8a;

/* Secondary Colors */
--color-secondary: #10b981;

/* Accent Colors */
--color-accent-purple: #8b5cf6;
--color-accent-pink: #ec4899;
--color-accent-orange: #f97316;
--color-accent-cyan: #06b6d4;

/* Status Colors */
--color-success: #10b981;
--color-warning: #f59e0b;
--color-error: #ef4444;
--color-info: #3b82f6;
```

### Typography

```css
--font-primary: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

### Components

#### Buttons
```tsx
// Primary Button
<button className="btn-primary">
  Click Me
</button>

// Secondary Button
<button className="btn-secondary">
  Cancel
</button>
```

#### Cards
```tsx
<div className="card">
  Card content
</div>

<div className="card card-gradient">
  Gradient Card
</div>
```

#### Inputs
```tsx
<input
  type="text"
  className="input-premium"
  placeholder="Enter text"
/>
```

#### Badges
```tsx
<span className="badge badge-success">Success</span>
<span className="badge badge-warning">Warning</span>
<span className="badge badge-error">Error</span>
<span className="badge badge-info">Info</span>
```

---

## 🔄 Context Providers

### Theme Context
```tsx
import { useTheme } from './contexts/ThemeContext';

const { theme, toggleTheme } = useTheme();
```

### Auth Context
```tsx
import { useAuth } from './contexts/AuthContext';

const { user, login, logout, isAuthenticated } = useAuth();
```

### WebSocket Context
```tsx
import { useWebSocket } from './contexts/WebSocketContext';

const { socket, isConnected } = useWebSocket();
```

---

## 🌐 API Integration

### Using the API Service
```tsx
import { apiService } from './services/api';

// Get transactions
const transactions = await apiService.financials.getTransactions();

// Create transaction
await apiService.financials.createTransaction(data);

// Get financial summary
const summary = await apiService.financials.getSummary({ period: 'this_month' });

// Get health score
const health = await apiService.ml.getHealthScore();
```

---

## 📱 Responsive Design

The frontend is fully responsive and works on:
- **Desktop** (1200px+)
- **Laptop** (992px - 1199px)
- **Tablet** (768px - 991px)
- **Mobile** (320px - 767px)

### Breakpoints
```css
/* Mobile First */
/* Mobile: 0-767px */
/* Tablet: 768px-991px */
/* Desktop: 992px+ */
```

---

## 🎭 Animations

Using Framer Motion for smooth animations:

```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>
```

---

## 🐛 Troubleshooting

### Issue: Port 5173 already in use
```bash
# Kill the process
lsof -ti:5173 | xargs kill

# Or use a different port
npm run dev -- --port 5174
```

### Issue: Module not found
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Issue: TypeScript errors
```bash
# Check types
npm run type-check
```

---

## 🚀 Building for Production

```bash
# Build the application
npm run build

# Preview the build
npm run preview
```

The production build will be in the `dist/` directory.

---

## 📝 Next Steps

### To Implement:
1. **Financials Page** - Transaction management, charts, filters
2. **Inventory Page** - Product catalog, stock management, alerts
3. **AI Chat Page** - Chat interface with AI agent
4. **Voice Insights Page** - Voice input and audio output
5. **Reports Page** - Advanced reports and analytics
6. **Settings Page** - User and business settings

### Enhancements:
- Add PWA support for mobile app experience
- Implement offline support
- Add more chart types and visualizations
- Create 3D elements with Three.js
- Add more animations and micro-interactions

---

## 💡 Tips

1. **Use hot reload**: Changes are automatically reflected in the browser
2. **Check console**: Open DevTools to see any errors
3. **Test responsive**: Use Chrome DevTools device emulation
4. **Clean build**: Occasionally run `npm run build` to test production build
5. **Use TypeScript**: Take advantage of type safety
6. **Follow design system**: Use the predefined classes and components

---

## 🎉 Congratulations!

Your Pro-Max AFIS frontend is now set up and running! 

The application features:
- ✅ Premium, enterprise-grade design
- ✅ Smooth animations and transitions
- ✅ Responsive layout for all devices
- ✅ Dark/Light mode support
- ✅ Real-time WebSocket integration
- ✅ Beautiful charts and visualizations
- ✅ Comprehensive routing and navigation

**Open http://localhost:5173 to see your application!**

For questions or issues, refer to the main README.md or contact the development team.