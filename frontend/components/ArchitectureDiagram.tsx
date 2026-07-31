'use client';

import React from 'react';
import { User, Layers, Search, ShieldAlert, Cpu, CheckCircle2, ArrowRight } from 'lucide-react';

export default function ArchitectureDiagram() {
  const steps = [
    {
      icon: User,
      title: "1. User Query",
      desc: "Client submits prompt through Next.js 15 app",
      color: "from-blue-500 to-indigo-500"
    },
    {
      icon: Layers,
      title: "2. Sliding Word Chunking",
      desc: "Document split into max_words with sliding overlap",
      color: "from-indigo-500 to-purple-500"
    },
    {
      icon: Search,
      title: "3. TF-IDF & Cosine Search",
      desc: "Cached vectorizer computes top-K cosine scores",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: ShieldAlert,
      title: "4. Grounding System Prompt",
      desc: "Enforces strict context boundaries & fallback",
      color: "from-pink-500 to-rose-500"
    },
    {
      icon: Cpu,
      title: "5. Anthropic Claude API",
      desc: "Claude 3.7 Sonnet synthesizes cited response",
      color: "from-amber-500 to-emerald-500"
    },
    {
      icon: CheckCircle2,
      title: "6. Cited Output",
      desc: "Returns answer with explicit [Source X] badges",
      color: "from-emerald-500 to-teal-500"
    }
  ];

  return (
    <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 space-y-6">
      
      <div className="text-center space-y-2 max-w-xl mx-auto">
        <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-500/10 text-indigo-500 border border-indigo-500/20">
          System Architecture Pipeline
        </span>
        <h3 className="text-xl sm:text-2xl font-bold">End-to-End Grounded RAG Flow</h3>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
          How prompt queries flow from the browser through vector ranking to Anthropic Claude Sonnet LLM.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {steps.map((step, idx) => {
          const IconComp = step.icon;
          return (
            <div
              key={idx}
              className="p-5 rounded-2xl bg-slate-900/60 dark:bg-slate-950/80 border border-slate-800 relative group hover:border-indigo-500/50 transition-all duration-300 space-y-3"
            >
              <div className="flex items-center justify-between">
                <div className={`p-3 rounded-xl bg-gradient-to-tr ${step.color} text-white shadow-md`}>
                  <IconComp className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono text-slate-500">STEP 0{idx + 1}</span>
              </div>

              <div>
                <h4 className="font-semibold text-sm text-slate-100">{step.title}</h4>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">{step.desc}</p>
              </div>

              {idx < steps.length - 1 && (
                <div className="hidden lg:block absolute -right-3 top-1/2 -translate-y-1/2 z-10 p-1 rounded-full bg-slate-800 text-indigo-400 border border-slate-700">
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              )}
            </div>
          );
        })}
      </div>

    </div>
  );
}
