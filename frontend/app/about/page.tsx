'use client';

import React from 'react';
import ArchitectureDiagram from '../../components/ArchitectureDiagram';
import { Info, Cpu, Database, ShieldCheck, Code, Server, Terminal, Sparkles } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="space-y-12 py-8 max-w-6xl mx-auto px-4">
      
      {/* Header */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <span className="px-4 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider bg-electric-500/10 text-electric-400 border border-electric-500/20 inline-flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-amberAccent-400" />
          Technical Architecture Specification
        </span>
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100">
          Inside the <span className="gradient-text">RAG AI Engine</span>
        </h1>
        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
          Comprehensive technical breakdown of vector indexing, word-based sliding chunking, strict prompt grounding, and multi-tenant FastAPI architecture.
        </p>
      </div>

      {/* Architecture Diagram */}
      <ArchitectureDiagram />

      {/* Tech Stack Grid */}
      <div className="glass-panel-glow rounded-3xl p-8 border border-slate-200/80 dark:border-slate-800/80 space-y-6 shadow-xl">
        <h3 className="text-2xl font-extrabold flex items-center gap-3 text-slate-900 dark:text-slate-100">
          <Cpu className="w-7 h-7 text-electric-500" />
          Enterprise Stack Components
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 text-xs">
          <div className="p-5 rounded-2xl bg-charcoal-900 border border-slate-800 space-y-2.5 shadow-inner">
            <div className="flex items-center gap-2 text-electric-400 font-bold text-sm">
              <Code className="w-4 h-4 text-electric-400" /> Next.js App Router
            </div>
            <p className="text-slate-400 leading-relaxed">
              React 19 Server Components, Tailwind CSS, Lucide icons, and responsive glassmorphism themes.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-charcoal-900 border border-slate-800 space-y-2.5 shadow-inner">
            <div className="flex items-center gap-2 text-purpleAccent-400 font-bold text-sm">
              <Server className="w-4 h-4 text-purpleAccent-400" /> FastAPI Backend
            </div>
            <p className="text-slate-400 leading-relaxed">
              Asynchronous Python backend with Pydantic v2 schemas, CORS middleware, and custom document loaders.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-charcoal-900 border border-slate-800 space-y-2.5 shadow-inner">
            <div className="flex items-center gap-2 text-cyanAccent-400 font-bold text-sm">
              <Database className="w-4 h-4 text-cyanAccent-400" /> TF-IDF Vector Search
            </div>
            <p className="text-slate-400 leading-relaxed">
              scikit-learn TF-IDF Vectorizer with cached matrices and Cosine Similarity score ranking.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-charcoal-900 border border-slate-800 space-y-2.5 shadow-inner">
            <div className="flex items-center gap-2 text-emeraldAccent-400 font-bold text-sm">
              <Sparkles className="w-4 h-4 text-emeraldAccent-400" /> Claude Sonnet LLM
            </div>
            <p className="text-slate-400 leading-relaxed">
              Anthropic Claude 3.7 Sonnet model with strict grounding rules and explicit source citations.
            </p>
          </div>
        </div>
      </div>

    </div>
  );
}
