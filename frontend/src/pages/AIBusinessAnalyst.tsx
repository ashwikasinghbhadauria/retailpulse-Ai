import React, { useState } from 'react';
import {
  Bot,
  Send,
  Sparkles,
  ShieldCheck,
  CheckCircle,
  Lightbulb,
  AlertCircle,
  Code2,
  Terminal
} from 'lucide-react';

import { api } from '../services/api';
import { AIAnswerResponse } from '../types';

export const AIBusinessAnalyst: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState<AIAnswerResponse[]>([
    {
      question: 'Which category is most profitable?',
      tool_called: 'get_category_profit',
      answer: "'Electronics' is the most profitable category with $3,450,120.50 in gross profit (48.5% margin), generating $7,112,400.00 in total revenue.",
      evidence: {
        top_category: 'Electronics',
        top_category_profit: '$3,450,120.50',
        top_category_margin: '48.5%',
        revenue_share: '37.9%'
      },
      interpretation: 'Category demand is heavily concentrated in Electronics with strong customer price tolerance, delivering the highest absolute contribution to enterprise gross profit.',
      recommendation: 'Increase marketing allocation for top Electronics SKUs while maintaining disciplined promotional discount caps.',
      caveat: 'Category margins account for COGS and discounts, but exclude regional freight adjustments.'
    }
  ]);
  const [loading, setLoading] = useState(false);

  const suggestedQuestions = [
    "Which category is most profitable?",
    "Which region is underperforming?",
    "What is our churn risk distribution?",
    "What will future sales look like?",
    "Who are our highest-value customers?",
    "What should management focus on next month?"
  ];

  const handleAsk = async (qText: string) => {
    if (!qText.trim() || loading) return;
    const currentQ = qText.trim();
    setQuestion('');
    setLoading(true);

    try {
      const response = await api.askAIAnalyst(currentQ);
      setHistory(prev => [response, ...prev]);
    } catch (err) {
      console.error('AI Query failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 pb-12 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-sky-950/50 via-indigo-950/40 to-purple-950/40 border border-sky-500/20 rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-sky-500/20 border border-sky-500/30 flex items-center justify-center">
            <Bot className="w-5 h-5 text-sky-400" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">
              Generative AI Business Analyst
            </h2>
            <p className="text-xs text-gray-400">
              Tool-grounded AI analytics engine. Responses are strictly anchored in live warehouse metrics.
            </p>
          </div>
        </div>

        {/* Security & Tooling Transparency Notice */}
        <div className="mt-4 pt-3 border-t border-gray-800/80 flex flex-wrap items-center gap-4 text-xs text-gray-400">
          <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
            <ShieldCheck className="w-4 h-4" />
            Zero Arbitrary SQL (Safe Tool Calling)
          </span>
          <span className="flex items-center gap-1.5 text-sky-400 font-medium">
            <Code2 className="w-4 h-4" />
            Verified Numerical Evidence
          </span>
          <span className="flex items-center gap-1.5 text-purple-400 font-medium">
            <Lightbulb className="w-4 h-4" />
            Prescriptive Directives
          </span>
        </div>
      </div>

      {/* Query Input Box */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 shadow-lg space-y-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleAsk(question);
          }}
          className="flex items-center gap-3"
        >
          <input
            type="text"
            placeholder="Ask anything about retail sales, margins, churn, forecast, or strategy..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={loading}
            className="flex-1 px-4 py-3 bg-gray-950 border border-gray-800 rounded-xl text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-sky-500 transition"
          />
          <button
            type="submit"
            disabled={!question.trim() || loading}
            className="px-5 py-3 bg-sky-500 hover:bg-sky-400 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-xl transition flex items-center gap-2 shadow-lg shadow-sky-500/20"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            <span>Analyze</span>
          </button>
        </form>

        {/* Suggested Queries */}
        <div className="space-y-2">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-gray-400 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-sky-400" />
            Recommended Questions:
          </p>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((q) => (
              <button
                key={q}
                onClick={() => handleAsk(q)}
                disabled={loading}
                className="px-3 py-1.5 rounded-lg bg-gray-950 hover:bg-gray-800 border border-gray-800 text-xs text-gray-300 hover:text-white transition font-medium text-left"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Answer Stream History */}
      <div className="space-y-6">
        {history.map((item, idx) => (
          <div
            key={idx}
            className="bg-gray-900 border border-gray-800 rounded-2xl p-6 space-y-5 hover:border-gray-700 transition"
          >
            {/* Question Header & Tool Badge */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-gray-800">
              <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-sky-500/20 text-sky-400 flex items-center justify-center text-xs font-bold">
                  Q
                </span>
                {item.question}
              </h3>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-gray-950 text-sky-400 text-xs font-mono border border-gray-800">
                <Terminal className="w-3.5 h-3.5" />
                <span>tool: {item.tool_called}()</span>
              </div>
            </div>

            {/* 1. Answer Card */}
            <div className="space-y-1.5">
              <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">
                Executive Answer
              </span>
              <p className="text-sm font-semibold text-gray-100 leading-relaxed pt-1">
                {item.answer}
              </p>
            </div>

            {/* 2. Numerical Evidence Chips */}
            {item.evidence && Object.keys(item.evidence).length > 0 && (
              <div className="space-y-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-sky-400 px-2 py-0.5 rounded bg-sky-500/10 border border-sky-500/20">
                  Verified Data Evidence
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1">
                  {Object.entries(item.evidence).map(([key, val]) => (
                    <div key={key} className="p-2.5 rounded-xl bg-gray-950 border border-gray-800 text-xs">
                      <p className="text-[10px] text-gray-400 uppercase font-medium line-clamp-1">{key.replace(/_/g, ' ')}</p>
                      <p className="text-xs font-bold text-white mt-0.5">{String(val)}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 3. Interpretation & 4. Recommendation */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
              <div className="p-4 rounded-xl bg-gray-950/70 border border-gray-800 space-y-1.5">
                <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-400">
                  <CheckCircle className="w-4 h-4" />
                  <span>Business Interpretation</span>
                </div>
                <p className="text-xs text-gray-300 leading-relaxed">{item.interpretation}</p>
              </div>

              <div className="p-4 rounded-xl bg-gray-950/70 border border-gray-800 space-y-1.5">
                <div className="flex items-center gap-1.5 text-xs font-bold text-amber-400">
                  <Lightbulb className="w-4 h-4" />
                  <span>Prescriptive Recommendation</span>
                </div>
                <p className="text-xs text-gray-300 leading-relaxed">{item.recommendation}</p>
              </div>
            </div>

            {/* 5. Caveat Footer */}
            {item.caveat && (
              <div className="pt-2 flex items-center gap-2 text-[11px] text-gray-500">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                <span>{item.caveat}</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
