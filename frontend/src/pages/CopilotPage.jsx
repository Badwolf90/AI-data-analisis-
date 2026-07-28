import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Bot, Send, User, Sparkles, HelpCircle } from 'lucide-react';

export default function CopilotPage() {
  const [messages, setMessages] = useState([
    {
      sender: 'copilot',
      text: 'Halo! Saya AI Data Science Copilot Anda. 🤖 Ada yang ingin Anda tanyakan tentang hasil AutoML, metrik evaluasi (F1, Accuracy, Recall), atau penjelasan SHAP/LIME pada dataset Anda?'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSend = () => {
    if (!inputMessage.trim()) return;

    const userMsg = { sender: 'user', text: inputMessage };
    setMessages((prev) => [...prev, userMsg]);

    setTimeout(() => {
      let botReply = "Halo! Mari saya jelaskan hasil metrik evaluasi model Anda. Nilai F1-Score sebesar 96.4% menandakan keseimbangan yang sangat tinggi antara Presisi dan Sensitivitas. Model ini sangat andal untuk mendeteksi pelanggan churn.";
      if (inputMessage.toLowerCase().includes("shap")) {
        botReply = "Berdasarkan hasil SHAP (Shapley Additive Explanations), variabel 'Contract_Length' dan 'Monthly_Charges' merupakan 2 pendorong utama keputusan model. Perubahan pada kedua variabel ini berdampak langsung pada risiko churn.";
      }
      setMessages((prev) => [...prev, { sender: 'copilot', text: botReply }]);
    }, 1000);

    setInputMessage('');
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="h-[calc(100vh-140px)] flex flex-col glass-panel rounded-2xl border border-zinc-800 overflow-hidden"
    >
      {/* Chat Header */}
      <div className="p-4 border-b border-zinc-800 bg-zinc-950/60 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-cyan-500 to-violet-600 flex items-center justify-center text-white">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
              AI Data Science Copilot
              <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
                Senior Data Scientist Persona
              </span>
            </h3>
            <p className="text-[11px] text-zinc-400">Communicative Indonesian Explanations & Insights</p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 p-6 overflow-y-auto space-y-4">
        {messages.map((msg, idx) => (
          <div 
            key={idx} 
            className={`flex gap-3 max-w-3xl ${msg.sender === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
          >
            <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 ${
              msg.sender === 'user' ? 'bg-violet-600 text-white' : 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
            }`}>
              {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            <div className={`p-4 rounded-2xl text-xs leading-relaxed ${
              msg.sender === 'user' 
                ? 'bg-violet-600 text-white rounded-tr-none' 
                : 'bg-zinc-900/90 border border-zinc-800 text-zinc-200 rounded-tl-none whitespace-pre-line'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div className="p-4 border-t border-zinc-800 bg-zinc-950/60 space-y-3">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Tanyakan tentang hasil metrik, SHAP, LIME, atau rekomendasi bisnis..."
            className="flex-1 glass-input px-4 py-2.5 text-xs"
          />
          <button
            onClick={handleSend}
            className="px-4 py-2.5 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-semibold shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-2"
          >
            <Send className="w-3.5 h-3.5" />
            Kirim
          </button>
        </div>

        {/* Suggested Prompts */}
        <div className="flex flex-wrap gap-2 text-[11px] text-zinc-400">
          <span className="text-zinc-500 flex items-center gap-1">
            <HelpCircle className="w-3 h-3" /> Rekomendasi Pertanyaan:
          </span>
          {["Jelaskan hasil F1-Score & Accuracy", "Jelaskan hasil SHAP feature importance", "Berikan rekomendasi bisnis"].map((prompt, idx) => (
            <button 
              key={idx}
              onClick={() => setInputMessage(prompt)}
              className="px-2.5 py-1 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 transition-colors"
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
