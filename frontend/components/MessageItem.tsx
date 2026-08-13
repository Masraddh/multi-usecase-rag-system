'use client';

import React, { useState } from 'react';
import { ChatResponse, RetrievedChunk } from '../services/api';
import { User, Bot, Copy, Check, Sparkles, BookOpen, Layers, ShieldCheck, ChevronDown, ChevronUp } from 'lucide-react';

export interface Message {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  timestamp: string;
  responseMeta?: ChatResponse;
}

interface MessageItemProps {
  message: Message;
  onInspectRetrieval?: (chunks: RetrievedChunk[]) => void;
}

export default function MessageItem({ message, onInspectRetrieval }: MessageItemProps) {
  const [copied, setCopied] = useState(false);
  const [showSources, setShowSources] = useState(false);

  const isUser = message.sender === 'user';

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Replace citation tags like [Source 1] with styled badges
  const renderFormattedContent = (text: string) => {
    const parts = text.split(/(\[Source \d+\])/g);
    return parts.map((part, index) => {
      if (/^\[Source \d+\]$/.test(part)) {
        return (
          <span
            key={index}
            className="inline-flex items-center gap-1 px-2 py-0.5 mx-1 rounded-lg text-xs font-mono font-bold bg-electric-500/10 text-electric-400 border border-electric-500/30"
          >
            <BookOpen className="w-3 h-3" />
            {part.replace('[Source ', 'Src ')}
          </span>
        );
      }
      return <span key={index}>{part}</span>;
    });
  };

  return (
    <div className={`flex gap-3.5 sm:gap-4 p-4 rounded-3xl transition-all duration-300 ${
      isUser
        ? 'bg-gradient-to-r from-electric-600 to-purpleAccent-600 text-white shadow-glow-blue ml-auto max-w-[85%] border border-electric-500/30'
        : 'glass-panel-glow text-slate-900 dark:text-slate-100 max-w-[95%]'
    }`}>
      
      {/* Avatar Icon */}
      <div className={`w-9 h-9 rounded-2xl flex items-center justify-center shrink-0 shadow-md ${
        isUser
          ? 'bg-white/20 text-white border border-white/30'
          : 'bg-gradient-to-tr from-electric-500 via-purpleAccent-500 to-cyanAccent-500 text-white shadow-glow-purple'
      }`}>
        {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
      </div>

      {/* Content Body */}
      <div className="flex-1 space-y-2 overflow-hidden">
        
        {/* Header line */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className={`font-bold text-xs ${isUser ? 'text-white' : 'text-slate-900 dark:text-slate-100'}`}>
              {isUser ? 'You' : 'AI Assistant'}
            </span>
            {!isUser && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emeraldAccent-500/10 text-emeraldAccent-400 border border-emeraldAccent-500/20">
                <ShieldCheck className="w-3 h-3" /> Grounded RAG
              </span>
            )}
            <span className={`text-[10px] font-mono ${isUser ? 'text-blue-100/80' : 'text-slate-400'}`}>
              {message.timestamp}
            </span>
          </div>

          {!isUser && (
            <button
              onClick={handleCopy}
              className="p-1.5 rounded-xl text-slate-400 hover:text-electric-400 hover:bg-slate-800/50 transition"
              title="Copy text"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emeraldAccent-400" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          )}
        </div>

        {/* Message Text */}
        <div className={`text-sm leading-relaxed whitespace-pre-wrap ${isUser ? 'text-white' : 'text-slate-800 dark:text-slate-200'}`}>
          {renderFormattedContent(message.content)}
        </div>

        {/* Assistant Retrieval Metadata Footer */}
        {!isUser && message.responseMeta && (
          <div className="pt-2 border-t border-slate-200/60 dark:border-slate-800/60 space-y-2">
            <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-slate-400">
              <div className="flex items-center gap-3 font-mono text-[11px]">
                <span>Score: <strong className="text-electric-400">{(message.responseMeta.max_similarity_score * 100).toFixed(1)}%</strong></span>
                <span>•</span>
                <span>Latency: <strong className="text-purpleAccent-400">{message.responseMeta.latency_ms}ms</strong></span>
              </div>

              {message.responseMeta.retrieved_chunks && message.responseMeta.retrieved_chunks.length > 0 && (
                <button
                  onClick={() => setShowSources(!showSources)}
                  className="flex items-center gap-1.5 text-xs font-semibold text-electric-400 hover:underline"
                >
                  <Layers className="w-3.5 h-3.5" />
                  {showSources ? 'Hide Vector Sources' : `Inspect Chunks (${message.responseMeta.retrieved_chunks.length})`}
                  {showSources ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>
              )}
            </div>

            {/* Expandable Chunks Preview */}
            {showSources && message.responseMeta.retrieved_chunks && (
              <div className="mt-2 space-y-2 p-3.5 rounded-2xl bg-charcoal-900 text-slate-200 text-xs font-mono border border-slate-800 shadow-inner">
                <div className="flex justify-between items-center text-[11px] text-slate-400 pb-1.5 border-b border-slate-800">
                  <span className="font-sans font-bold text-slate-300">Retrieved TF-IDF Vector Chunks</span>
                  <span className="text-electric-400">{message.responseMeta.retrieved_chunks.length} Matched</span>
                </div>
                {message.responseMeta.retrieved_chunks.map((chunk, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-navy-950/80 border border-slate-800 space-y-1.5">
                    <div className="flex justify-between text-[11px] text-electric-400 font-bold">
                      <span>[Source {chunk.chunk_index}]</span>
                      <span className="text-emeraldAccent-400">Cosine Similarity: {(chunk.similarity_score * 100).toFixed(1)}%</span>
                    </div>
                    <p className="text-[11px] leading-relaxed text-slate-300 font-sans">{chunk.text}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}
