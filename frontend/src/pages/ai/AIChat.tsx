// ========================================
// Pro-Max AFIS - AI Chat Page (Complete)
// ========================================

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, Mic, MicOff, Bot, User, Sparkles,
  MoreVertical, Trash2, Settings, X, Loader2,
  Lightbulb, TrendingUp, AlertCircle, CheckCircle
} from 'lucide-react';
import { Layout } from '../../components/layout/Layout';

// Types
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  actions?: Action[];
}

interface Action {
  label: string;
  type: 'navigate' | 'execute' | 'view';
  path?: string;
}

// Predefined Quick Actions
const quickActions = [
  { label: 'Show financial summary', prompt: 'What is my financial summary for this month?' },
  { label: 'Check inventory status', prompt: 'Which products are running low on stock?' },
  { label: 'Sales forecast', prompt: 'What is the sales forecast for next week?' },
  { label: 'Cash balance', prompt: 'What is my current cash balance?' },
  { label: 'Pending payments', prompt: 'How many pending payments do I have?' },
  { label: 'Expense breakdown', prompt: 'Break down my expenses by category' }
];

// Mock AI Responses
const mockResponses: Record<string, { response: string; actions?: Action[] }> = {
  'financial': {
    response: `Based on your data for March 2024:

📊 **Financial Summary**
- **Total Income**: ₹3,10,000 (+12.5% from last month)
- **Total Expenses**: ₹1,05,000 (+5.2% from last month)
- **Net Profit**: ₹2,05,000 (+18.3% from last month)
- **Profit Margin**: 66.1%

🏆 **Top Performing Categories**
1. Sales Revenue: ₹2,25,000 (72.6%)
2. Service Income: ₹85,000 (27.4%)

⚠️ **Alerts**
- 3 pending invoices worth ₹75,000
- GST net payable: ₹45,540 for March`,
    actions: [
      { label: 'View Full Report', type: 'navigate', path: '/financials' },
      { label: 'Download P&L', type: 'execute' }
    ]
  },
  'inventory': {
    response: `📦 **Inventory Status Report**

**Current Stock Level**: 475 units
**Total Stock Value**: ₹2,25,000

🚨 **Low Stock Alerts (5 items)**
1. **Connector Set Z** - 0 units (CRITICAL)
   - Min stock: 100 units
   - Action: Immediate reorder required

2. **Electronic Module Y** - 8 units (HIGH)
   - Min stock: 20 units
   - Action: Order within 3 days

3. **Industrial Component X** - 25 units (MEDIUM)
   - Min stock: 30 units
   - Action: Plan reorder

💡 **Recommendations**
- Consider increasing minimum stock for Electronic Module Y due to consistent demand
- Place bulk order for Connector Set Z to get better pricing`,
    actions: [
      { label: 'Manage Inventory', type: 'navigate', path: '/inventory' },
      { label: 'View All Alerts', type: 'execute' }
    ]
  },
  'forecast': {
    response: `📈 **Sales Forecast (Next 7 Days)**

**Predicted Sales**: ₹1,85,000
**Confidence Level**: 92%
**Growth Trend**: +15% vs last week

**Daily Breakdown:**
- Mon (Mar 18): ₹28,500
- Tue (Mar 19): ₹32,000
- Wed (Mar 20): ₹26,500
- Thu (Mar 21): ₹29,000
- Fri (Mar 22): ₹31,000
- Sat (Mar 23): ₹22,000
- Sun (Mar 24): ₹16,000

🎯 **Key Insights**
- Peak sales expected on Tuesday
- Weekend sales typically 30% lower
- Consider running promotions on Saturday to boost numbers`,
    actions: [
      { label: 'View Detailed Forecast', type: 'navigate', path: '/reports' },
      { label: 'Simulate Scenarios', type: 'execute' }
    ]
  },
  'cash': {
    response: `💰 **Cash Position Analysis**

**Current Cash Balance**: ₹8,75,000

**Cash Flow Breakdown:**
- Cash In (This Month): ₹2,45,000
- Cash Out (This Month): ₹1,65,000
- Net Cash Flow: +₹80,000

**Liquidity Position**: EXCELLENT ✅
- Current ratio: 2.8
- Quick ratio: 2.1
- Cash runway: 8.5 months (at current burn rate)

**Upcoming Payments (Next 30 Days):**
- Vendor payments: ₹1,25,000
- Salary: ₹85,000
- GST payment: ₹45,540
- **Total**: ₹2,55,540

📊 You have sufficient cash to cover all upcoming payments comfortably.`,
    actions: [
      { label: 'View Cash Flow', type: 'navigate', path: '/financials' },
      { label: 'Cash Flow Report', type: 'execute' }
    ]
  },
  'pending': {
    response: `⏳ **Pending Payments Overview**

**Total Pending**: ₹75,000 across 3 invoices

**Invoice Details:**
1. **INV-2024-078** - ₹45,000
   - Due: March 20, 2024 (in 5 days)
   - Client: ABC Corp Ltd
   - Status: Follow-up needed

2. **INV-2024-082** - ₹20,000
   - Due: March 25, 2024 (in 10 days)
   - Client: XYZ Industries
   - Status: Payment expected

3. **INV-2024-085** - ₹10,000
   - Due: March 18, 2024 (overdue)
   - Client: StartUp Solutions
   - Status: Urgent follow-up required

⚠️ **Action Required**
- 1 invoice is overdue
- Send payment reminders to overdue clients
- Consider payment reminders for invoices due this week`,
    actions: [
      { label: 'View Invoices', type: 'navigate', path: '/financials' },
      { label: 'Send Reminders', type: 'execute' }
    ]
  },
  'expenses': {
    response: `📊 **Expense Breakdown (March 2024)**

**Total Expenses**: ₹1,05,000

**By Category:**
1. **Inventory Purchase**: ₹45,000 (42.9%)
2. **Salaries**: ₹25,000 (23.8%)
3. **Rent**: ₹15,000 (14.3%)
4. **Marketing**: ₹12,000 (11.4%)
5. **Utilities & Others**: ₹8,000 (7.6%)

**Trend Analysis:**
- Marketing expenses increased by 25% vs last month
- Inventory costs stable
- Salaries unchanged

💡 **Insights**
- Marketing ROI shows positive correlation with sales growth (+15%)
- Consider optimizing marketing spend for better ROI
- Inventory costs well within budget at 42.9% of revenue`,
    actions: [
      { label: 'Detailed Report', type: 'navigate', path: '/reports' },
      { label: 'Optimize Budget', type: 'execute' }
    ]
  },
  'default': {
    response: `I understand you're asking about that. Let me help you with your financial and business data.

Based on your business data, I can provide insights on:
- Financial performance and reports
- Inventory status and alerts
- Sales forecasting and trends
- Cash flow analysis
- Expense breakdown and optimization
- Payment tracking and follow-ups

Please let me know what specific information you need, or try one of the quick actions above.`
  }
};

// Get AI Response based on query
const getAIResponse = (query: string): { response: string; actions?: Action[] } => {
  const lowerQuery = query.toLowerCase();
  
  if (lowerQuery.includes('financial') || lowerQuery.includes('summary') || lowerQuery.includes('profit') || lowerQuery.includes('income')) {
    return mockResponses.financial;
  } else if (lowerQuery.includes('inventory') || lowerQuery.includes('stock') || lowerQuery.includes('product')) {
    return mockResponses.inventory;
  } else if (lowerQuery.includes('forecast') || lowerQuery.includes('prediction') || lowerQuery.includes('future')) {
    return mockResponses.forecast;
  } else if (lowerQuery.includes('cash') || lowerQuery.includes('balance') || lowerQuery.includes('money')) {
    return mockResponses.cash;
  } else if (lowerQuery.includes('pending') || lowerQuery.includes('invoice') || lowerQuery.includes('payment')) {
    return mockResponses.pending;
  } else if (lowerQuery.includes('expense') || lowerQuery.includes('spend') || lowerQuery.includes('cost')) {
    return mockResponses.expenses;
  }
  
  return mockResponses.default;
};

export const AIChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `Hello! 👋 I'm your AI Financial Assistant. I can help you with:

📊 Financial insights and reports
📦 Inventory management and alerts
📈 Sales forecasting and trends
💰 Cash flow analysis
⏳ Payment tracking

What would you like to know today?`,
      timestamp: new Date(),
      actions: quickActions.map(a => ({ label: a.label, type: 'execute' as const }))
    }
  ]);
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showActions, setShowActions] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle Send Message
  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate AI processing
    setTimeout(() => {
      const aiResponse = getAIResponse(userMessage.content);
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: aiResponse.response,
        timestamp: new Date(),
        actions: aiResponse.actions
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };

  // Handle Voice Recording
  const handleVoiceRecord = () => {
    if (isRecording) {
      setIsRecording(false);
      // Simulate voice transcription
      setInput('What is my sales forecast for next week?');
    } else {
      setIsRecording(true);
      // Simulate recording
      setTimeout(() => {
        setIsRecording(false);
        setInput('What is my current inventory status?');
      }, 2000);
    }
  };

  // Handle Quick Action
  const handleQuickAction = (prompt: string) => {
    setInput(prompt);
    inputRef.current?.focus();
  };

  // Handle Action Button Click
  const handleAction = (action: Action, messageId: string) => {
    if (action.type === 'navigate' && action.path) {
      // Navigate to the path (in real app)
      console.log('Navigate to:', action.path);
    } else if (action.type === 'execute') {
      // Execute action
      console.log('Execute action:', action.label);
    }
    setShowActions(null);
  };

  // Format timestamp
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Layout>
      <div className="h-[calc(100vh-140px)] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900 dark:text-white">AI Financial Assistant</h1>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span className="text-sm text-slate-500 dark:text-slate-400">Online</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 transition-colors">
              <Trash2 className="w-5 h-5" />
            </button>
            <button className="p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 transition-colors">
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex gap-3 max-w-3xl ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                {/* Avatar */}
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                  message.role === 'user' 
                    ? 'bg-gradient-to-r from-emerald-500 to-green-600' 
                    : 'bg-gradient-to-r from-blue-500 to-indigo-600'
                }`}>
                  {message.role === 'user' ? (
                    <User className="w-5 h-5 text-white" />
                  ) : (
                    <Bot className="w-5 h-5 text-white" />
                  )}
                </div>

                {/* Message Content */}
                <div className={`flex flex-col ${message.role === 'user' ? 'items-end' : 'items-start'} flex-1`}>
                  <div className={`rounded-2xl px-4 py-3 max-w-2xl ${
                    message.role === 'user' 
                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-tr-md' 
                      : 'bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-white rounded-tl-md'
                  }`}>
                    <div className="whitespace-pre-wrap text-sm leading-relaxed">
                      {message.content}
                    </div>
                  </div>
                  
                  {/* Actions */}
                  {message.actions && message.actions.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {message.actions.map((action, actionIndex) => (
                        <motion.button
                          key={actionIndex}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: index * 0.1 + actionIndex * 0.05 }}
                          onClick={() => handleAction(action, message.id)}
                          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                            message.role === 'user'
                              ? 'bg-white text-blue-600 hover:bg-slate-50 shadow-sm'
                              : 'bg-white dark:bg-slate-600 text-blue-600 dark:text-blue-400 hover:bg-slate-50 dark:hover:bg-slate-500 shadow-sm'
                          }`}
                        >
                          {action.type === 'navigate' ? (
                            <CheckCircle className="w-4 h-4" />
                          ) : action.type === 'execute' ? (
                            <Sparkles className="w-4 h-4" />
                          ) : (
                            <Lightbulb className="w-4 h-4" />
                          )}
                          {action.label}
                        </motion.button>
                      ))}
                    </div>
                  )}

                  {/* Timestamp */}
                  <span className="text-xs text-slate-400 mt-1">
                    {formatTime(message.timestamp)}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}

          {/* Loading Indicator */}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="bg-slate-100 dark:bg-slate-700 rounded-2xl rounded-tl-md px-4 py-3">
                  <Loader2 className="w-5 h-5 text-slate-400 animate-spin" />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Actions */}
        <div className="p-4 border-t border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
          <div className="flex flex-wrap gap-2 mb-3">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={() => handleQuickAction(action.prompt)}
                className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors"
              >
                {action.label}
              </button>
            ))}
          </div>

          {/* Input Area */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleVoiceRecord}
              className={`p-3 rounded-xl transition-all ${
                isRecording 
                  ? 'bg-red-500 text-white animate-pulse' 
                  : 'bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600'
              }`}
            >
              {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>
            
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask me anything about your finances..."
                className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-12"
              />
              {input && (
                <button
                  onClick={() => setInput('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-600 text-slate-400"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="p-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
};