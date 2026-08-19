'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Sparkles, Home, MessageSquare, LayoutDashboard, Settings, HelpCircle } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center px-4 space-y-6">
      <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-rose-500/10 text-rose-400 text-xs font-mono font-bold border border-rose-500/20">
        <HelpCircle className="w-4 h-4" /> 404 Route Not Found
      </div>

      <h1 className="text-6xl sm:text-8xl font-black text-slate-900 dark:text-slate-100 font-mono tracking-tight">
        404
      </h1>

      <div className="space-y-2 max-w-md mx-auto">
        <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-200">
          Page Could Not Be Found
        </h2>
        <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
          The requested page URL does not exist or has been moved. Use the navigation quick links below to jump straight to the AI Studio Workspace or Home page.
        </p>
      </div>

      {/* Quick Action Navigation Buttons */}
      <div className="flex flex-wrap items-center justify-center gap-3 pt-4">
        <Link
          href="/chat"
          className="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-electric-500 via-purpleAccent-500 to-cyanAccent-500 hover:from-electric-600 hover:to-purpleAccent-600 text-white font-extrabold text-sm shadow-glow-blue transition-transform hover:scale-105 flex items-center gap-2"
        >
          <Sparkles className="w-4 h-4 text-amberAccent-400" />
          Launch AI Studio Workspace (/chat)
        </Link>

        <Link
          href="/"
          className="px-5 py-3.5 rounded-2xl glass-panel hover:bg-slate-800/50 text-slate-700 dark:text-slate-300 font-bold text-sm border border-slate-700 transition flex items-center gap-2"
        >
          <Home className="w-4 h-4 text-electric-400" />
          Return Home (/)
        </Link>
      </div>

      {/* Additional Route Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 max-w-lg mx-auto pt-6 text-xs">
        <Link
          href="/dashboard"
          className="p-3 rounded-xl glass-panel hover:border-electric-500/50 text-slate-300 flex items-center gap-2 font-medium"
        >
          <LayoutDashboard className="w-4 h-4 text-purpleAccent-400" />
          Dashboard
        </Link>
        <Link
          href="/settings"
          className="p-3 rounded-xl glass-panel hover:border-electric-500/50 text-slate-300 flex items-center gap-2 font-medium"
        >
          <Settings className="w-4 h-4 text-cyanAccent-400" />
          Settings
        </Link>
        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noreferrer"
          className="p-3 rounded-xl glass-panel hover:border-electric-500/50 text-slate-300 flex items-center gap-2 font-medium col-span-2 sm:col-span-1"
        >
          <HelpCircle className="w-4 h-4 text-emeraldAccent-400" />
          FastAPI Docs
        </a>
      </div>
    </div>
  );
}
