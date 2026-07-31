'use client';

import React, { useState } from 'react';
import { updateSettings } from '../../services/api';
import { Settings, Key, Eye, EyeOff, Save, CheckCircle2, Sliders, ShieldCheck, Cpu, Sparkles } from 'lucide-react';

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    if (!apiKey.trim()) return;
    setLoading(true);
    try {
      await updateSettings(apiKey.trim());
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      alert('Failed to update API Key');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-10">
      
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-electric-500/10 text-electric-400 font-mono text-xs font-semibold border border-electric-500/20 mb-2">
          <Sparkles className="w-3.5 h-3.5 text-amberAccent-400" />
          <span>Global Engine Parameters</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold flex items-center gap-3 text-slate-900 dark:text-slate-100">
          <Settings className="w-8 h-8 text-electric-500" />
          System Settings & <span className="gradient-text">Configuration</span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1">
          Configure API keys, model presets, default RAG hyperparameter overrides, and runtime environment settings.
        </p>
      </div>

      {/* API Key Configuration Card */}
      <div className="glass-panel-glow rounded-3xl p-6 sm:p-8 border border-slate-200/80 dark:border-slate-800/80 space-y-6 shadow-xl">
        <div className="flex items-center gap-4 border-b border-slate-200/80 dark:border-slate-800/80 pb-5">
          <div className="p-3.5 rounded-2xl bg-gradient-to-tr from-electric-500 to-purpleAccent-500 text-white shadow-glow-blue">
            <Key className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-extrabold text-lg text-slate-900 dark:text-slate-100">Anthropic API Key Authentication</h3>
            <p className="text-xs text-slate-600 dark:text-slate-400">Set runtime ANTHROPIC_API_KEY for Anthropic Claude Sonnet AI response completion.</p>
          </div>
        </div>

        <div className="space-y-4">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 font-mono">
            Anthropic API Key (<code className="text-electric-400">ANTHROPIC_API_KEY</code>)
          </label>
          <div className="relative">
            <input
              type={showKey ? 'text' : 'password'}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-ant-api03-..."
              className="w-full bg-navy-950/80 border border-slate-800 rounded-2xl px-4 py-3.5 text-sm font-mono text-slate-100 focus:outline-none focus:border-electric-500 transition pr-12 shadow-inner"
            />
            <button
              type="button"
              onClick={() => setShowKey(!showKey)}
              className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 p-1"
            >
              {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
            <p className="text-[11px] text-slate-400 flex items-center gap-1.5 font-mono">
              <ShieldCheck className="w-4 h-4 text-emeraldAccent-400" />
              API keys are encrypted in-memory and never written to disk logs.
            </p>

            <button
              onClick={handleSave}
              disabled={loading || !apiKey.trim()}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-electric-500 via-purpleAccent-500 to-cyanAccent-500 hover:from-electric-600 hover:to-purpleAccent-600 text-white font-extrabold text-xs shadow-glow-blue disabled:opacity-50 transition flex items-center gap-2"
            >
              {saved ? <CheckCircle2 className="w-4 h-4 text-emeraldAccent-400" /> : <Save className="w-4 h-4" />}
              {saved ? 'Key Saved Successfully!' : 'Save API Key'}
            </button>
          </div>
        </div>
      </div>

      {/* Hyperparameter Information Card */}
      <div className="glass-panel-glow rounded-3xl p-6 sm:p-8 border border-slate-200/80 dark:border-slate-800/80 space-y-6 shadow-xl">
        <div className="flex items-center gap-4 border-b border-slate-200/80 dark:border-slate-800/80 pb-5">
          <div className="p-3.5 rounded-2xl bg-gradient-to-tr from-purpleAccent-500 to-cyanAccent-500 text-white shadow-glow-purple">
            <Sliders className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-extrabold text-lg text-slate-900 dark:text-slate-100">Default RAG Hyperparameter Presets</h3>
            <p className="text-xs text-slate-600 dark:text-slate-400">Baseline configuration tuning for sliding-window word chunking & vector retrieval.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-2xl bg-charcoal-900 border border-slate-800 space-y-1.5 shadow-inner">
            <span className="font-bold text-electric-400 text-sm font-mono">Max Words: 80w</span>
            <p className="text-slate-400 text-[11px] leading-relaxed">Optimal word ceiling per chunk for technical resumes, FAQs, and API docs.</p>
          </div>
          <div className="p-4 rounded-2xl bg-charcoal-900 border border-slate-800 space-y-1.5 shadow-inner">
            <span className="font-bold text-purpleAccent-400 text-sm font-mono">Overlap: 15w</span>
            <p className="text-slate-400 text-[11px] leading-relaxed">Sliding boundary overlap preserving context across sequential chunk breaks.</p>
          </div>
          <div className="p-4 rounded-2xl bg-charcoal-900 border border-slate-800 space-y-1.5 shadow-inner">
            <span className="font-bold text-cyanAccent-400 text-sm font-mono">Top-K: 3 Chunks</span>
            <p className="text-slate-400 text-[11px] leading-relaxed">Retrieval cutoff depth for TF-IDF cosine similarity vector match.</p>
          </div>
        </div>
      </div>

    </div>
  );
}
