'use client';

import React from 'react';
import Link from 'next/link';
import { Brain, Github, Terminal, Cpu, ShieldCheck } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-800/80 bg-slate-50 dark:bg-obsidian-950/80 py-12 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          <div className="space-y-4 md:col-span-2">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-roseGold-600 flex items-center justify-center text-white font-bold shadow-glow-rose">
                <Brain className="w-5 h-5" />
              </div>
              <span className="font-bold text-lg">RAG AI Assistant Suite</span>
            </div>
            <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed max-w-md">
              Enterprise-grade multi-use case platform showcasing TF-IDF Cosine Similarity vector search, sliding-window word chunking, and Anthropic Claude Sonnet grounded completion across 5 specialized AI Assistants.
            </p>
            <div className="flex items-center gap-3 text-xs text-slate-400 font-mono">
              <span className="flex items-center gap-1"><Cpu className="w-3.5 h-3.5 text-roseGold-400" /> Next.js 15</span>
              <span>•</span>
              <span className="flex items-center gap-1"><Terminal className="w-3.5 h-3.5 text-amethyst-400" /> FastAPI</span>
              <span>•</span>
              <span className="flex items-center gap-1"><ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /> Claude Sonnet</span>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wider mb-4">Assistants</h4>
            <ul className="space-y-2 text-sm text-slate-500 dark:text-slate-400">
              <li><Link href="/chat" className="hover:text-roseGold-500 transition">Interview Coach</Link></li>
              <li><Link href="/chat" className="hover:text-roseGold-500 transition">Campus FAQ</Link></li>
              <li><Link href="/chat" className="hover:text-roseGold-500 transition">Exam Study Buddy</Link></li>
              <li><Link href="/chat" className="hover:text-roseGold-500 transition">Ecommerce Support</Link></li>
              <li><Link href="/chat" className="hover:text-roseGold-500 transition">Code Documentation</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wider mb-4">Navigation</h4>
            <ul className="space-y-2 text-sm text-slate-500 dark:text-slate-400">
              <li><Link href="/" className="hover:text-roseGold-500 transition">Landing Page</Link></li>
              <li><Link href="/chat" className="hover:text-roseGold-500 transition">AI Studio Workspace</Link></li>
              <li><Link href="/dashboard" className="hover:text-roseGold-500 transition">Platform Analytics</Link></li>
              <li><Link href="/settings" className="hover:text-roseGold-500 transition">Settings & API Key</Link></li>
              <li><Link href="/about" className="hover:text-roseGold-500 transition">Architecture Docs</Link></li>
            </ul>
          </div>

        </div>

        <div className="pt-8 border-t border-slate-200 dark:border-slate-800/60 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-slate-500 dark:text-slate-400">
          <p>© {new Date().getFullYear()} RAG AI Assistant Suite. Designed for Capstone Evaluation & Technical Portfolio.</p>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" /> System Operational
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
