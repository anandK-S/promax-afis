// ========================================
// Pro-Max AFIS - Voice Insights Page (Complete)
// ========================================

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Mic, MicOff, Volume2, VolumeX, Play, Pause,
  TrendingUp, TrendingDown, AlertTriangle, CheckCircle,
  DollarSign, Package, BarChart3, PieChart, RefreshCw,
  Settings, History, Languages, Loader2
} from 'lucide-react';
import { Layout } from '../../components/layout/Layout';

// Types
interface InsightCard {
  id: string;
  title: string;
  value: string;
  change: string;
  trend: 'up' | 'down' | 'neutral';
  category: 'financial' | 'inventory' | 'sales' | 'operations';
}

interface VoiceCommand {
  id: string;
  command: string;
  timestamp: Date;
  status: 'success' | 'error';
  response: string;
}

// Mock Data
const mockInsights: InsightCard[] = [
  { id: '1', title: 'Revenue Today', value: '₹45,500', change: '+12%', trend: 'up', category: 'financial' },
  { id: '2', title: 'Orders Pending', value: '23', change: '-5', trend: 'down', category: 'sales' },
  { id: '3', title: 'Low Stock Items', value: '5', change: '+2', trend: 'up', category: 'inventory' },
  { id: '4', title: 'Net Profit Margin', value: '66%', change: '+3%', trend: 'up', category: 'financial' },
  { id: '5', title: 'Customer Visits', value: '156', change: '+18%', trend: 'up', category: 'operations' },
  { id: '6', title: 'Avg Order Value', value: '₹2,450', change: '+8%', trend: 'up', category: 'sales' },
];

const mockHistory: VoiceCommand[] = [
  { id: '1', command: 'Show me today\'s revenue', timestamp: new Date(Date.now() - 300000), status: 'success', response: 'Today\'s revenue is ₹45,500, which is 12% higher than yesterday.' },
  { id: '2', command: 'Check inventory alerts', timestamp: new Date(Date.now() - 900000), status: 'success', response: 'You have 5 low stock items. The most critical is Connector Set Z with 0 units.' },
  { id: '3', command: 'What\'s my profit margin?', timestamp: new Date(Date.now() - 1800000), status: 'success', response: 'Your current profit margin is 66%, up 3% from last month.' },
  { id: '4', command: 'Send payment reminder', timestamp: new Date(Date.now() - 3600000), status: 'success', response: 'Payment reminder sent to ABC Corp Ltd for invoice INV-2024-078 of ₹45,000.' },
];

const supportedLanguages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
  { code: 'gu', name: 'Gujarati', flag: '🇮🇳' },
  { code: 'mr', name: 'Marathi', flag: '🇮🇳' },
  { code: 'ta', name: 'Tamil', flag: '🇮🇳' },
  { code: 'te', name: 'Telugu', flag: '🇮🇳' },
  { code: 'bn', name: 'Bengali', flag: '🇮🇳' },
  { code: 'kn', name: 'Kannada', flag: '🇮🇳' },
  { code: 'ml', name: 'Malayalam', flag: '🇮🇳' },
  { code: 'pa', name: 'Punjabi', flag: '🇮🇳' },
];

const quickCommands = [
  { icon: DollarSign, label: 'Revenue Today', command: 'show revenue today' },
  { icon: Package, label: 'Stock Status', command: 'check stock status' },
  { icon: BarChart3, label: 'Sales Report', command: 'give me sales report' },
  { icon: AlertTriangle, label: 'Alerts', command: 'show all alerts' },
  { icon: TrendingUp, label: 'Forecast', command: 'predict next week sales' },
  { icon: PieChart, label: 'Expenses', command: 'break down expenses' },
];

export const VoiceInsights: React.FC = () => {
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [showLanguageModal, setShowLanguageModal] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [history, setHistory] = useState<VoiceCommand[]>(mockHistory);

  // Simulate Voice Recording
  const startListening = () => {
    setIsListening(true);
    setTranscript('');
    setResponse('');
    
    // Simulate listening and transcription
    setTimeout(() => {
      setTranscript('What is my sales forecast for next week?');
      setIsListening(false);
      setIsProcessing(true);
      
      // Simulate AI processing
      setTimeout(() => {
        setResponse(`Based on your historical data, here's the sales forecast for next week:

📈 Predicted Sales: ₹1,85,000
📊 Confidence: 92%
📅 Peak Day: Tuesday (₹32,000)

Key Insights:
• Sales expected to grow 15% from last week
• Best performing category: Electronics
• Consider running promotions on Saturday

Would you like me to send this forecast to your email?`);
        setIsProcessing(false);
        
        // Add to history
        const newCommand: VoiceCommand = {
          id: Date.now().toString(),
          command: 'What is my sales forecast for next week?',
          timestamp: new Date(),
          status: 'success',
          response: 'Sales forecast generated for next week. Predicted: ₹1,85,000 with 92% confidence.'
        };
        setHistory(prev => [newCommand, ...prev]);
        
        // Speak response if enabled
        if (voiceEnabled) {
          speakResponse('Sales forecast generated. Predicted revenue is 1 lakh 85 thousand rupees with 92% confidence.');
        }
      }, 1500);
    }, 3000);
  };

  const stopListening = () => {
    setIsListening(false);
  };

  // Simulate Text-to-Speech
  const speakResponse = (text: string) => {
    setIsSpeaking(true);
    // In real app, use Web Speech API or gTTS
    setTimeout(() => {
      setIsSpeaking(false);
    }, 5000);
  };

  const stopSpeaking = () => {
    setIsSpeaking(false);
  };

  // Handle Quick Command
  const handleQuickCommand = (command: string) => {
    setTranscript(command);
    setIsProcessing(true);
    
    setTimeout(() => {
      const responses: Record<string, string> = {
        'show revenue today': `Today's Revenue: ₹45,500\n\nThis is 12% higher than yesterday's revenue of ₹40,600. Your best selling product today is Premium Widget A with 18 units sold.`,
        'check stock status': `Stock Status Summary:\n\n📦 Total Products: 8\n✅ In Stock: 6\n⚠️ Low Stock: 5\n❌ Out of Stock: 1\n\nTotal Stock Value: ₹2,25,000`,
        'give me sales report': `Sales Report - March 2024:\n\n💰 Total Sales: ₹3,10,000\n📈 Growth: +18.3%\n🎯 Target: 95% achieved\n\nTop Categories:\n1. Sales Revenue: ₹2,25,000\n2. Service Income: ₹85,000`,
        'show all alerts': `You have 5 active alerts:\n\n🚨 CRITICAL: Connector Set Z out of stock\n⚠️ HIGH: Electronic Module Y running low\n⚠️ MEDIUM: Industrial Component X below minimum\n📌 LOW: Standard Widget B, Display Panel LED`,
        'predict next week sales': `Sales Forecast - Next 7 Days:\n\n📈 Predicted: ₹1,85,000\n📊 Confidence: 92%\n\nPeak Day: Tuesday (₹32,000)\nWeekend expected: Lower traffic`,
        'break down expenses': `Expense Breakdown - March 2024:\n\n💼 Total: ₹1,05,000\n\n1. Inventory: ₹45,000 (42.9%)\n2. Salaries: ₹25,000 (23.8%)\n3. Rent: ₹15,000 (14.3%)\n4. Marketing: ₹12,000 (11.4%)\n5. Others: ₹8,000 (7.6%)`
      };
      
      setResponse(responses[command] || 'I understand. Let me process that for you.');
      setIsProcessing(false);
      
      const newCommand: VoiceCommand = {
        id: Date.now().toString(),
        command: command,
        timestamp: new Date(),
        status: 'success',
        response: 'Command processed successfully.'
      };
      setHistory(prev => [newCommand, ...prev]);
    }, 1500);
  };

  // Get category icon
  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'financial': return DollarSign;
      case 'inventory': return Package;
      case 'sales': return TrendingUp;
      default: return BarChart3;
    }
  };

  // Format time ago
  const formatTimeAgo = (date: Date) => {
    const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Voice Insights
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1">
              Speak naturally and get instant financial insights
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setShowLanguageModal(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all"
            >
              <Languages className="w-4 h-4" />
              {supportedLanguages.find(l => l.code === selectedLanguage)?.name}
            </button>
            <button 
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Voice Input Section */}
        <div className="bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 rounded-3xl p-8 text-white relative overflow-hidden">
          {/* Background decorations */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-40 -right-40 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
            <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
          </div>

          <div className="relative z-10 flex flex-col items-center">
            {/* Microphone Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={isListening ? stopListening : startListening}
              disabled={isProcessing}
              className={`w-32 h-32 rounded-full flex items-center justify-center transition-all ${
                isListening 
                  ? 'bg-red-500 shadow-[0_0_60px_rgba(239,68,68,0.5)]' 
                  : 'bg-white/20 backdrop-blur-lg hover:bg-white/30 shadow-[0_0_60px_rgba(255,255,255,0.2)]'
              }`}
            >
              {isProcessing ? (
                <Loader2 className="w-12 h-12 animate-spin" />
              ) : isListening ? (
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ repeat: Infinity, duration: 1 }}
                >
                  <MicOff className="w-12 h-12" />
                </motion.div>
              ) : (
                <Mic className="w-12 h-12" />
              )}
            </motion.button>

            {/* Status Text */}
            <div className="mt-6 text-center">
              {isProcessing ? (
                <p className="text-xl font-medium">Processing your request...</p>
              ) : isListening ? (
                <div>
                  <p className="text-xl font-medium">Listening...</p>
                  <p className="text-white/70 mt-1">Speak naturally in {supportedLanguages.find(l => l.code === selectedLanguage)?.name}</p>
                </div>
              ) : (
                <div>
                  <p className="text-xl font-medium">Tap to speak</p>
                  <p className="text-white/70 mt-1">Ask about your finances, inventory, or forecasts</p>
                </div>
              )}
            </div>

            {/* Transcript */}
            {transcript && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 bg-white/20 backdrop-blur-lg rounded-2xl px-6 py-4 max-w-lg"
              >
                <p className="text-sm text-white/70 mb-1">You said:</p>
                <p className="text-lg font-medium">"{transcript}"</p>
              </motion.div>
            )}

            {/* Response */}
            {response && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 bg-white/10 backdrop-blur-lg rounded-2xl px-6 py-4 max-w-lg"
              >
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm text-white/70">Response:</p>
                  {voiceEnabled && (
                    <button
                      onClick={isSpeaking ? stopSpeaking : () => speakResponse(response)}
                      className="p-1.5 rounded-lg hover:bg-white/10 transition-colors"
                    >
                      {isSpeaking ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                    </button>
                  )}
                </div>
                <p className="text-sm whitespace-pre-wrap">{response}</p>
              </motion.div>
            )}
          </div>
        </div>

        {/* Quick Commands */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">Quick Commands</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {quickCommands.map((cmd, index) => (
              <motion.button
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                onClick={() => handleQuickCommand(cmd.command)}
                disabled={isProcessing || isListening}
                className="flex flex-col items-center gap-2 p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50 hover:bg-slate-100 dark:hover:bg-slate-700 transition-all disabled:opacity-50"
              >
                <cmd.icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                <span className="text-xs font-medium text-slate-600 dark:text-slate-300 text-center">{cmd.label}</span>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Live Insights & History */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Live Insights */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Live Insights</h3>
              <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 transition-colors">
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {mockInsights.map((insight, index) => {
                const Icon = getCategoryIcon(insight.category);
                return (
                  <motion.div
                    key={insight.id}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.05 }}
                    className="p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <Icon className={`w-5 h-5 ${
                        insight.category === 'financial' ? 'text-emerald-500' :
                        insight.category === 'inventory' ? 'text-amber-500' :
                        insight.category === 'sales' ? 'text-blue-500' : 'text-purple-500'
                      }`} />
                      <span className={`flex items-center text-xs font-medium ${
                        insight.trend === 'up' ? 'text-emerald-600 dark:text-emerald-400' : 
                        insight.trend === 'down' ? 'text-red-600 dark:text-red-400' : 
                        'text-slate-500'
                      }`}>
                        {insight.trend === 'up' ? <TrendingUp className="w-3 h-3 mr-0.5" /> : 
                         insight.trend === 'down' ? <TrendingDown className="w-3 h-3 mr-0.5" /> : null}
                        {insight.change}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">{insight.title}</p>
                    <p className="text-lg font-bold text-slate-900 dark:text-white">{insight.value}</p>
                  </motion.div>
                );
              })}
            </div>
          </div>

          {/* Command History */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Command History</h3>
              <History className="w-5 h-5 text-slate-400" />
            </div>
            <div className="space-y-3 max-h-80 overflow-y-auto">
              {history.map((cmd, index) => (
                <motion.div
                  key={cmd.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="flex items-start gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-700/50"
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                    cmd.status === 'success' ? 'bg-emerald-100 dark:bg-emerald-900/30' : 'bg-red-100 dark:bg-red-900/30'
                  }`}>
                    {cmd.status === 'success' ? (
                      <CheckCircle className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-red-600 dark:text-red-400" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-900 dark:text-white truncate">
                      "{cmd.command}"
                    </p>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 line-clamp-2">
                      {cmd.response}
                    </p>
                    <p className="text-xs text-slate-400 dark:text-slate-500 mt-1">
                      {formatTimeAgo(cmd.timestamp)}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        {/* Language Selection Modal */}
        <AnimatePresence>
          {showLanguageModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
              onClick={() => setShowLanguageModal(false)}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-full max-w-md"
                onClick={e => e.stopPropagation()}
              >
                <div className="p-6 border-b border-slate-100 dark:border-slate-700">
                  <h2 className="text-xl font-bold text-slate-900 dark:text-white">Select Language</h2>
                  <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Choose your preferred language for voice commands</p>
                </div>
                <div className="p-4 grid grid-cols-2 gap-2 max-h-80 overflow-y-auto">
                  {supportedLanguages.map(lang => (
                    <button
                      key={lang.code}
                      onClick={() => {
                        setSelectedLanguage(lang.code);
                        setShowLanguageModal(false);
                      }}
                      className={`flex items-center gap-3 p-3 rounded-xl transition-all ${
                        selectedLanguage === lang.code 
                          ? 'bg-blue-100 dark:bg-blue-900/30 border-2 border-blue-500' 
                          : 'bg-slate-50 dark:bg-slate-700/50 hover:bg-slate-100 dark:hover:bg-slate-700'
                      }`}
                    >
                      <span className="text-2xl">{lang.flag}</span>
                      <span className="font-medium text-slate-900 dark:text-white">{lang.name}</span>
                    </button>
                  ))}
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Layout>
  );
};