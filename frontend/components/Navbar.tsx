'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Brain, MessageSquare, LayoutDashboard, Settings, Info, Sparkles, Activity } from 'lucide-react';
import ThemeToggle from './ThemeToggle';

export default function Navbar() {
  const pathname = usePathname();

  const navLinks = [
    { href: '/', label: 'Home', icon: Brain },
    { href: '/chat', label: 'AI Studio', icon: MessageSquare },
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/settings', label: 'Settings', icon: Settings },
    { href: '/about', label: 'Architecture', icon: Info },
  ];

  return (
    <nav className="sticky top-0 z-50 border-b border-slate-200/80 dark:border-slate-800/80 bg-white/80 dark:bg-navy-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo Brand */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-electric-500 via-purpleAccent-500 to-cyanAccent-500 flex items-center justify-center shadow-glow-blue group-hover:scale-105 transition-transform duration-300">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg leading-none tracking-tight flex items-center gap-1.5 text-slate-900 dark:text-slate-100">
                RAG AI <span className="gradient-text">Suite</span>
                <span className="text-[10px] uppercase font-mono font-semibold px-2 py-0.5 rounded-full bg-electric-500/10 text-electric-400 border border-electric-500/20">
                  PRO
                </span>
              </span>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 font-medium">Enterprise Knowledge Engine</span>
            </div>
          </Link>

          {/* System Operational Status Badge */}
          <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-emeraldAccent-500/10 border border-emeraldAccent-500/20 text-emeraldAccent-400 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-emeraldAccent-500 animate-pulse" />
            <span>System Operational</span>
          </div>

          {/* Nav Links */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-sm font-semibold transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-electric-600 to-purpleAccent-600 text-white shadow-glow-blue'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {link.label}
                </Link>
              );
            })}
          </div>

          {/* Right Actions */}
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <Link
              href="/chat"
              className="hidden sm:inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-electric-500 via-purpleAccent-500 to-cyanAccent-500 hover:from-electric-600 hover:to-purpleAccent-600 text-white font-bold text-sm shadow-glow-purple transition-all hover:scale-[1.03] active:scale-[0.97]"
            >
              <Sparkles className="w-4 h-4 text-amberAccent-400" />
              Launch Studio
            </Link>
          </div>

        </div>
      </div>
    </nav>
  );
}
