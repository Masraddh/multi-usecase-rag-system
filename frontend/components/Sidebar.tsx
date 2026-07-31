'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { AssistantInfo } from '../services/api';
import {
  UserCheck,
  GraduationCap,
  BookOpen,
  ShoppingBag,
  Code,
  Sliders,
  Cpu,
  FileText,
  Layers,
  CheckCircle2,
  Trash2,
  RotateCcw,
  Sparkles,
  Home,
  LayoutDashboard,
  Settings,
  Info,
  ChevronRight,
  Database
} from 'lucide-react';

interface SidebarProps {
  assistants: AssistantInfo[];
  selectedAssistant: AssistantInfo | null;
  onSelectAssistant: (ast: AssistantInfo) => void;
  maxWords: number;
  setMaxWords: (val: number) => void;
  overlap: number;
  setOverlap: (val: number) => void;
  topK: number;
  setTopK: (val: number) => void;
  groundedMode?: boolean;
  setGroundedMode?: (val: boolean) => void;
  onClearChat: () => void;
  onResetApp: () => void;
  apiStatus: boolean;
}

const ICON_MAP: Record<string, any> = {
  UserCheck: UserCheck,
  GraduationCap: GraduationCap,
  BookOpen: BookOpen,
  ShoppingBag: ShoppingBag,
  Code: Code,
};

export default function Sidebar({
  assistants,
  selectedAssistant,
  onSelectAssistant,
  maxWords,
  setMaxWords,
  overlap,
  setOverlap,
  topK,
  setTopK,
  groundedMode = true,
  setGroundedMode,
  onClearChat,
  onResetApp,
  apiStatus,
}: SidebarProps) {
  const pathname = usePathname();

  const navCards = [
    { href: '/', label: 'Home', icon: Home, desc: 'Landing Overview' },
    { href: '/knowledge-base', label: 'Knowledge Base', icon: Database, desc: 'Documents' },
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, desc: 'Analytics' },
    { href: '/settings', label: 'Settings', icon: Settings, desc: 'API & Config' },
  ];

  return (
    <aside className="w-full lg:w-80 glass-panel-glow rounded-3xl p-5 space-y-6 flex flex-col justify-between shrink-0 shadow-xl border border-slate-200/80 dark:border-slate-800/80">
      
      <div className="space-y-6">

        {/* Quick Nav Cards */}
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2.5 flex items-center gap-1.5 font-mono">
            <span>Navigation</span>
          </h3>
          <div className="grid grid-cols-2 gap-2">
            {navCards.map((nc) => {
              const Icon = nc.icon;
              const isActive = pathname === nc.href;
              return (
                <Link
                  key={nc.href}
                  href={nc.href}
                  className={`p-2.5 rounded-2xl flex flex-col justify-between border transition-all ${
                    isActive
                      ? 'bg-gradient-to-br from-electric-600/20 to-purpleAccent-600/20 border-electric-500/50 text-electric-400 font-bold shadow-sm'
                      : 'border-slate-200/60 dark:border-slate-800/80 hover:bg-slate-100/60 dark:hover:bg-slate-800/40 text-slate-600 dark:text-slate-400'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <Icon className="w-4 h-4 text-electric-400" />
                    <ChevronRight className="w-3 h-3 opacity-40" />
                  </div>
                  <span className="text-xs font-semibold">{nc.label}</span>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Assistant Selector Section */}
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5 font-mono">
            <Sparkles className="w-3.5 h-3.5 text-purpleAccent-400" />
            Select AI Assistant
          </h3>
          <div className="space-y-2">
            {assistants.map((ast) => {
              const IconComp = ICON_MAP[ast.icon] || UserCheck;
              const isSelected = selectedAssistant?.id === ast.id;
              return (
                <button
                  key={ast.id}
                  onClick={() => onSelectAssistant(ast)}
                  className={`w-full text-left p-3 rounded-2xl transition-colors duration-100 active:scale-[0.99] flex items-center gap-3 border ${
                    isSelected
                      ? 'bg-gradient-to-r from-electric-600/20 to-purpleAccent-600/20 border-electric-500/50 text-electric-400 dark:text-electric-300 font-bold shadow-glow-blue'
                      : 'border-slate-200/60 dark:border-slate-800/80 hover:bg-slate-100 dark:hover:bg-slate-800/40 text-slate-700 dark:text-slate-300'
                  }`}
                >
                  <div className={`p-2.5 rounded-xl ${isSelected ? 'bg-electric-500 text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400'}`}>
                    <IconComp className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-bold truncate text-slate-900 dark:text-slate-100">{ast.name}</p>
                    <p className="text-[11px] text-slate-400 truncate mt-0.5">{ast.persona}</p>
                  </div>
                  {isSelected && <span className="w-2.5 h-2.5 rounded-full bg-electric-400 animate-pulse shadow-glow-blue shrink-0" />}
                </button>
              );
            })}
          </div>
        </div>

        {/* Live RAG Parameters Controls */}
        <div className="pt-4 border-t border-slate-200/80 dark:border-slate-800/80 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5 font-mono">
            <Sliders className="w-3.5 h-3.5 text-purpleAccent-400" />
            RAG Hyperparameters
          </h3>

          {/* Max Words Slider */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-slate-600 dark:text-slate-300">Chunk Size (Words)</span>
              <span className="text-electric-400 font-mono font-bold">{maxWords}w</span>
            </div>
            <input
              type="range"
              min={30}
              max={150}
              step={5}
              value={maxWords}
              onChange={(e) => setMaxWords(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-lg appearance-none cursor-pointer accent-electric-500"
            />
          </div>

          {/* Overlap Slider */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-slate-600 dark:text-slate-300">Overlap (Words)</span>
              <span className="text-purpleAccent-400 font-mono font-bold">{overlap}w</span>
            </div>
            <input
              type="range"
              min={5}
              max={30}
              step={1}
              value={overlap}
              onChange={(e) => setOverlap(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purpleAccent-500"
            />
          </div>

          {/* Strict Grounded RAG Toggle Switch */}
          <div className="p-3 rounded-2xl bg-roseGold-500/10 border border-roseGold-500/20 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-800 dark:text-slate-200 flex items-center gap-1.5 font-mono">
                <Sparkles className="w-3.5 h-3.5 text-roseGold-400" />
                Grounded RAG Mode
              </span>
              <button
                type="button"
                onClick={() => setGroundedMode && setGroundedMode(!groundedMode)}
                className={`w-11 h-6 rounded-full p-0.5 transition-colors duration-200 ease-in-out ${
                  groundedMode ? 'bg-roseGold-500' : 'bg-slate-400 dark:bg-slate-700'
                }`}
              >
                <div
                  className={`w-5 h-5 rounded-full bg-white shadow-md transform transition-transform duration-200 ease-in-out ${
                    groundedMode ? 'translate-x-5' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-tight">
              {groundedMode 
                ? "🔒 Grounded RAG ON: Answers ONLY using facts from indexed documents." 
                : "🌐 Grounded RAG OFF: Answers using documents + general AI knowledge."}
            </p>
          </div>

          {/* Top K Slider */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-slate-600 dark:text-slate-300">Top-K Chunks</span>
              <span className="text-cyanAccent-400 font-mono font-bold">{topK}</span>
            </div>
            <input
              type="range"
              min={1}
              max={5}
              step={1}
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyanAccent-500"
            />
          </div>
        </div>

        {/* Engine Telemetry Metrics */}
        <div className="pt-4 border-t border-slate-200/80 dark:border-slate-800/80 space-y-2 text-xs">
          <div className="flex justify-between py-1.5 px-3 rounded-xl bg-slate-100/60 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 border border-slate-200/40 dark:border-slate-800/40">
            <span className="flex items-center gap-1.5"><Cpu className="w-3.5 h-3.5 text-electric-400" /> AI Engine</span>
            <span className="font-semibold text-slate-800 dark:text-slate-200 font-mono">Claude Sonnet</span>
          </div>

          <div className="flex justify-between py-1.5 px-3 rounded-xl bg-slate-100/60 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 border border-slate-200/40 dark:border-slate-800/40">
            <span className="flex items-center gap-1.5"><FileText className="w-3.5 h-3.5 text-emeraldAccent-400" /> Active Document</span>
            <span className="font-semibold text-slate-800 dark:text-slate-200 font-mono truncate max-w-[110px]">{selectedAssistant?.filename || 'default'}</span>
          </div>

          <div className="flex justify-between py-1.5 px-3 rounded-xl bg-slate-100/60 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 border border-slate-200/40 dark:border-slate-800/40">
            <span className="flex items-center gap-1.5"><Layers className="w-3.5 h-3.5 text-amberAccent-400" /> Active Chunks</span>
            <span className="font-semibold text-slate-800 dark:text-slate-200 font-mono">{selectedAssistant?.total_chunks || 4} Chunks</span>
          </div>

          <div className="flex justify-between py-1.5 px-3 rounded-xl bg-slate-100/60 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 border border-slate-200/40 dark:border-slate-800/40">
            <span className="flex items-center gap-1.5"><CheckCircle2 className="w-3.5 h-3.5 text-emeraldAccent-400" /> Engine Status</span>
            <span className="font-semibold text-emeraldAccent-400 flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emeraldAccent-400 animate-ping" /> Online
            </span>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="pt-4 border-t border-slate-200/80 dark:border-slate-800/80 flex gap-2">
        <button
          onClick={onClearChat}
          className="flex-1 py-2.5 px-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 text-xs font-bold flex items-center justify-center gap-1.5 transition border border-slate-200 dark:border-slate-700"
        >
          <Trash2 className="w-3.5 h-3.5" /> Clear Chat
        </button>
        <button
          onClick={onResetApp}
          className="py-2.5 px-3 rounded-xl bg-roseAccent-500/10 hover:bg-roseAccent-500/20 text-roseAccent-400 text-xs font-bold flex items-center justify-center gap-1.5 transition border border-roseAccent-500/20"
          title="Reset Parameters & Conversation"
        >
          <RotateCcw className="w-3.5 h-3.5" /> Reset
        </button>
      </div>

    </aside>
  );
}
