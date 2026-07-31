'use client';

import React from 'react';
import { RetrievedChunk } from '../services/api';
import { Layers, Target, Tag, Percent, FileText, X, Copy, Check } from 'lucide-react';

interface RetrievalPanelProps {
  chunks: RetrievedChunk[];
  maxScore: number;
  isOpen: boolean;
  onClose: () => void;
}

export default function RetrievalPanel({ chunks, maxScore, isOpen, onClose }: RetrievalPanelProps) {
  const [copiedIndex, setCopiedIndex] = React.useState<number | null>(null);

  if (!isOpen) return null;

  const handleCopyChunk = (text: string, idx: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="glass-panel-glow rounded-3xl p-5 border border-electric-500/40 space-y-4 shadow-glow-blue animate-fade-in">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-200/80 dark:border-slate-800/80">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-gradient-to-tr from-electric-500 to-purpleAccent-500 text-white shadow-md">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-extrabold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-2">
              Retrieved Context Vector Panel
            </h4>
            <p className="text-xs text-slate-400 font-mono">TF-IDF Vector Search & Cosine Similarity Matrix</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="px-3 py-1 rounded-full bg-electric-500/10 text-electric-400 font-mono text-xs font-bold border border-electric-500/20">
            Top Score: {(maxScore * 100).toFixed(1)}%
          </span>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-slate-400 hover:text-slate-200 bg-slate-800/60 hover:bg-slate-800 transition"
            title="Close Panel"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Chunks List */}
      <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
        {chunks.length === 0 ? (
          <p className="text-xs text-slate-400 italic">No vector chunks retrieved for current prompt.</p>
        ) : (
          chunks.map((chunk) => {
            const conf = chunk.confidence_percent || (chunk.similarity_score * 100);
            
            // Color Coding Confidence Bar
            let barColor = 'bg-amberAccent-500';
            let textColor = 'text-amberAccent-400';
            if (conf >= 80) {
              barColor = 'bg-emeraldAccent-500';
              textColor = 'text-emeraldAccent-400';
            } else if (conf >= 50) {
              barColor = 'bg-electric-500';
              textColor = 'text-electric-400';
            }

            return (
              <div
                key={chunk.chunk_index}
                className="p-4 rounded-2xl bg-charcoal-900 border border-slate-800 space-y-3 text-xs shadow-inner"
              >
                <div className="flex items-center justify-between font-mono text-[11px]">
                  <span className="flex items-center gap-1.5 font-bold text-slate-200">
                    <FileText className="w-4 h-4 text-electric-400" /> Chunk #{chunk.chunk_index}
                  </span>

                  <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1 text-slate-400">
                      <Target className="w-3.5 h-3.5 text-purpleAccent-400" /> Cosine Score: {chunk.similarity_score.toFixed(4)}
                    </span>
                    <span className={`font-bold flex items-center gap-1 ${textColor}`}>
                      <Percent className="w-3.5 h-3.5" /> {conf.toFixed(1)}%
                    </span>
                    <button
                      onClick={() => handleCopyChunk(chunk.text, chunk.chunk_index)}
                      className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
                      title="Copy Chunk Text"
                    >
                      {copiedIndex === chunk.chunk_index ? <Check className="w-3.5 h-3.5 text-emeraldAccent-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                </div>

                {/* Progress bar visual */}
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div className={`h-full ${barColor} transition-all duration-500`} style={{ width: `${Math.min(100, Math.max(5, conf))}%` }} />
                </div>

                {/* Chunk text content */}
                <p className="text-slate-200 font-sans leading-relaxed text-xs p-3 rounded-xl bg-navy-950/80 border border-slate-800/80">
                  "{chunk.text}"
                </p>

                {/* Highlighted Keywords chips */}
                {chunk.keywords && chunk.keywords.length > 0 && (
                  <div className="flex items-center gap-1.5 flex-wrap pt-1">
                    <span className="text-[10px] text-slate-400 font-mono flex items-center gap-1">
                      <Tag className="w-3 h-3 text-purpleAccent-400" /> Matched Keywords:
                    </span>
                    {chunk.keywords.map((kw, i) => (
                      <span
                        key={i}
                        className="px-2 py-0.5 rounded-md bg-purpleAccent-500/10 text-purpleAccent-300 text-[10px] font-mono border border-purpleAccent-500/20 font-semibold"
                      >
                        {kw}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

    </div>
  );
}
