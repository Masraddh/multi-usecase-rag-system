'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import {
  Brain,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap,
  Layers,
  Search,
  UserCheck,
  GraduationCap,
  BookOpen,
  ShoppingBag,
  Code,
  CheckCircle2,
  Lock,
  Cpu,
  Upload,
  BarChart3,
  FileText
} from 'lucide-react';
import ArchitectureDiagram from '../components/ArchitectureDiagram';
import { fetchStats, SystemStats } from '../services/api';

export default function LandingPage() {
  const [stats, setStats] = useState<SystemStats | null>(null);

  useEffect(() => {
    fetchStats().then(setStats).catch(() => {});
  }, []);

  const assistants = [
    {
      id: 'interview_coach',
      name: '🎤 Interview Preparation Coach',
      persona: 'Professional Interview Coach',
      desc: 'Rehearses candidate profile, React Native, Power BI, SQL, and ML engineering questions with grounded feedback.',
      icon: UserCheck,
      color: 'from-electric-500 to-indigo-600',
      badge: 'Resume RAG'
    },
    {
      id: 'campus_faq',
      name: '🎓 Campus FAQ Helpdesk',
      persona: 'Friendly Student Helpdesk',
      desc: 'Instant assistance for library borrowing limits, hostel curfew hours, fee penalties, and exam attendance rules.',
      icon: GraduationCap,
      color: 'from-emeraldAccent-500 to-teal-600',
      badge: 'Handbook RAG'
    },
    {
      id: 'study_buddy',
      name: '📚 Exam Study Buddy',
      persona: 'Patient OS Teacher',
      desc: 'Fine-tuned chunking (50 words/chunk, 12 overlap) explaining FCFS, SJF, Round Robin, and Convoy Effect.',
      icon: BookOpen,
      color: 'from-purpleAccent-500 to-pink-600',
      badge: 'Textbook RAG'
    },
    {
      id: 'ecommerce_support',
      name: '🛒 Ecommerce Support Agent',
      persona: 'Customer Support Agent',
      desc: 'Product specs helper for Voyager Pro 30L backpack sizing, color options, 15-day return policy, and warranty.',
      icon: ShoppingBag,
      color: 'from-amberAccent-500 to-orange-600',
      badge: 'Catalogue RAG'
    },
    {
      id: 'code_docs',
      name: '💻 Code Documentation Expert',
      persona: 'Technical Docs Expert',
      desc: 'Grounded API reference assistant for RAGEngine methods: chunk_text(), retrieve(), and ask().',
      icon: Code,
      color: 'from-cyanAccent-500 to-blue-600',
      badge: 'API Spec RAG'
    }
  ];

  return (
    <div className="space-y-20 py-8 sm:py-12 bg-grid-pattern relative">
      
      {/* Background Radial Glow */}
      <div className="absolute top-10 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-electric-500/20 via-purpleAccent-500/20 to-cyanAccent-500/10 blur-[120px] rounded-full pointer-events-none -z-10" />

      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-4xl mx-auto pt-4 px-4">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-pill border border-electric-500/30 text-electric-400 text-xs font-mono font-semibold shadow-glow-blue animate-pulse-glow">
          <Sparkles className="w-3.5 h-3.5 text-amberAccent-400" />
          <span>Next-Generation Enterprise RAG Engine Suite</span>
        </div>

        <h1 className="text-4xl sm:text-7xl font-extrabold tracking-tight leading-[1.15] text-slate-900 dark:text-slate-100">
          One Intelligent Engine. <br />
          <span className="gradient-text">Five Domain AI Assistants.</span>
        </h1>

        <p className="text-base sm:text-xl text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl mx-auto font-medium">
          Transform static datasets or custom uploaded documents into interactive, strictly grounded AI conversation assistants powered by TF-IDF vector search and Anthropic Claude Sonnet.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            href="/chat"
            className="px-8 py-4 rounded-2xl bg-gradient-to-r from-electric-500 via-purpleAccent-500 to-cyanAccent-500 hover:from-electric-600 hover:to-purpleAccent-600 text-white font-extrabold text-base shadow-glow-blue transition-all hover:scale-[1.04] active:scale-[0.98] flex items-center gap-3 group"
          >
            Launch Studio Workspace 
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          
          <Link
            href="/about"
            className="px-6 py-4 rounded-2xl glass-panel hover:bg-slate-200/50 dark:hover:bg-slate-800/50 text-slate-700 dark:text-slate-200 font-bold text-base border border-slate-300 dark:border-slate-800 transition-all hover:scale-[1.02]"
          >
            Explore Architecture
          </Link>
        </div>

        {/* Dynamic Telemetry Metrics Bar */}
        {stats && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-3xl mx-auto pt-8">
            <div className="p-4 rounded-2xl glass-panel-glow text-left">
              <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 flex items-center gap-1">
                <FileText className="w-3.5 h-3.5 text-electric-400" /> Active Docs
              </span>
              <p className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 font-mono mt-1">
                {stats.total_documents} Files
              </p>
            </div>

            <div className="p-4 rounded-2xl glass-panel-glow text-left">
              <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 flex items-center gap-1">
                <Layers className="w-3.5 h-3.5 text-purpleAccent-400" /> Total Chunks
              </span>
              <p className="text-2xl font-extrabold text-purpleAccent-400 font-mono mt-1">
                {stats.total_chunks} Chunks
              </p>
            </div>

            <div className="p-4 rounded-2xl glass-panel-glow text-left">
              <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 flex items-center gap-1">
                <BarChart3 className="w-3.5 h-3.5 text-cyanAccent-400" /> Avg Score
              </span>
              <p className="text-2xl font-extrabold text-cyanAccent-400 font-mono mt-1">
                {(stats.avg_retrieval_score * 100).toFixed(1)}%
              </p>
            </div>

            <div className="p-4 rounded-2xl glass-panel-glow text-left">
              <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 flex items-center gap-1">
                <Zap className="w-3.5 h-3.5 text-amberAccent-400" /> Latency
              </span>
              <p className="text-2xl font-extrabold text-amberAccent-400 font-mono mt-1">
                {stats.avg_response_time_ms} ms
              </p>
            </div>
          </div>
        )}

      </section>

      {/* Dynamic Upload Highlight Banner */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-navy-900 via-charcoal-900 to-navy-900 border border-electric-500/30 shadow-2xl relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-2 max-w-xl">
            <span className="text-xs font-mono font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-electric-500/10 text-electric-400 border border-electric-500/20 inline-flex items-center gap-1.5">
              <Upload className="w-3.5 h-3.5" /> Dynamic Knowledge Base
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-100">
              Upload Your Own Documents
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Drag & Drop PDF, Word (.docx), Text (.txt), Markdown (.md), PowerPoint (.pptx), or CSV files to instantly replace default datasets and query your own knowledge base.
            </p>
          </div>

          <Link
            href="/chat"
            className="px-6 py-3.5 rounded-2xl bg-electric-500 hover:bg-electric-600 text-white font-extrabold text-sm shadow-glow-blue transition-all shrink-0 flex items-center gap-2"
          >
            Try File Upload Studio <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* 5 AI Use Cases Grid */}
      <section className="max-w-6xl mx-auto px-4 space-y-8">
        <div className="text-center space-y-3">
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-slate-100">
            Explore 5 Specialized AI Assistants
          </h2>
          <p className="text-slate-600 dark:text-slate-400 text-sm max-w-xl mx-auto">
            Each assistant is pre-configured with tuned sliding-window word chunking, TF-IDF vectorization parameters, and specialized persona instructions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {assistants.map((ast) => {
            const Icon = ast.icon;
            return (
              <div
                key={ast.id}
                className="group glass-panel-glow rounded-3xl p-6 space-y-4 flex flex-col justify-between transition-all duration-300 hover:-translate-y-1"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className={`p-3 rounded-2xl bg-gradient-to-tr ${ast.color} text-white shadow-md`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                      {ast.badge}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 group-hover:text-electric-400 transition-colors">
                    {ast.name}
                  </h3>

                  <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                    {ast.desc}
                  </p>
                </div>

                <div className="pt-3 border-t border-slate-200/60 dark:border-slate-800/60 flex items-center justify-between">
                  <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400">
                    Persona: <strong className="text-slate-300 font-semibold">{ast.persona}</strong>
                  </span>
                  <Link
                    href="/chat"
                    className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:text-electric-400 hover:bg-electric-500/10 transition"
                    title="Launch this assistant"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            );
          })}

          {/* Architecture Highlight Card */}
          <div className="glass-panel-glow rounded-3xl p-6 space-y-4 flex flex-col justify-between border-2 border-dashed border-electric-500/40 bg-electric-500/5">
            <div className="space-y-3">
              <div className="p-3 rounded-2xl bg-gradient-to-tr from-cyanAccent-500 to-electric-600 text-white shadow-md w-fit">
                <Cpu className="w-6 h-6" />
              </div>

              <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                Strict Grounding Engine
              </h3>

              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Zero hallucination guarantee. If retrieved TF-IDF vector chunks do not contain sufficient evidence, the engine replies: <strong className="text-roseAccent-400 font-mono">"I don't have that information."</strong>
              </p>
            </div>

            <Link
              href="/about"
              className="w-full py-2.5 rounded-xl bg-slate-900 text-slate-200 font-bold text-xs hover:bg-slate-800 text-center transition border border-slate-700"
            >
              View System Architecture
            </Link>
          </div>
        </div>
      </section>

      {/* Architecture Section */}
      <section className="max-w-6xl mx-auto px-4 space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-slate-100">
            System Architecture Overview
          </h2>
          <p className="text-slate-600 dark:text-slate-400 text-sm">
            How documents pass through sliding-window chunking, TF-IDF vectorization, Cosine similarity search, and Claude Sonnet completion.
          </p>
        </div>

        <ArchitectureDiagram />
      </section>

      {/* Bottom CTA */}
      <section className="max-w-4xl mx-auto text-center py-12 px-4 space-y-6">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-slate-100">
          Ready to Experience Modern Grounded RAG?
        </h2>
        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-300 max-w-xl mx-auto">
          Start chatting with any of our 5 pre-loaded assistants or upload your custom PDF, DOCX, TXT, or MD documents now.
        </p>

        <Link
          href="/chat"
          className="inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-electric-500 via-purpleAccent-500 to-cyanAccent-500 text-white font-extrabold text-base shadow-glow-purple hover:scale-105 transition-transform"
        >
          Launch AI Studio Workspace <ArrowRight className="w-5 h-5" />
        </Link>
      </section>

    </div>
  );
}
