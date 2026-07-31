'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  color?: string;
  trend?: string;
}

export default function StatsCard({ title, value, subtitle, icon: Icon, color = 'indigo', trend }: StatsCardProps) {
  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-3 relative overflow-hidden group hover:border-indigo-500/40 transition-all duration-300">
      
      {/* Background Glow */}
      <div className="absolute -right-6 -bottom-6 w-24 h-24 rounded-full bg-gradient-to-tr from-indigo-500/10 to-purple-500/10 blur-xl group-hover:scale-150 transition-transform duration-500 pointer-events-none" />

      <div className="flex items-center justify-between">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400">{title}</span>
        <div className="p-2.5 rounded-xl bg-indigo-600/10 text-indigo-500 dark:text-indigo-400 group-hover:scale-110 transition-transform">
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div>
        <div className="text-2xl sm:text-3xl font-extrabold tracking-tight gradient-text">
          {value}
        </div>
        {subtitle && <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{subtitle}</p>}
      </div>

      {trend && (
        <div className="pt-2 border-t border-slate-200/60 dark:border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
          <span>{trend}</span>
          <span className="text-emerald-500 font-semibold">Active</span>
        </div>
      )}

    </div>
  );
}
