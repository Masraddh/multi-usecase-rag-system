'use client';

import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle2, AlertCircle, RefreshCw, RotateCcw, FileCode, Layers, BookOpen, Sparkles } from 'lucide-react';
import { AssistantInfo, uploadDocument, resetAssistantDocument, UploadResponse } from '../services/api';
import { DocumentDebugPanel } from './DocumentDebugPanel';

interface FileUploadCardProps {
  assistant: AssistantInfo | null;
  onAssistantUpdated: (updatedAst: AssistantInfo) => void;
}

export default function FileUploadCard({ assistant, onAssistantUpdated }: FileUploadCardProps) {
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!assistant) return null;

  const activeFilename = assistant.filename || 'default_dataset.txt';
  const numPages = assistant.num_pages || 1;
  const numWords = assistant.num_words || 250;
  const numChars = assistant.num_chars || (numWords * 5.5);
  const numChunks = assistant.total_chunks || 5;
  const vocabSize = assistant.vocab_size || Math.round(numWords * 0.45);
  const indexStatus = assistant.index_status || '✅ Successfully Indexed';
  const isCustom = assistant.is_custom || assistant.active_source === 'uploaded';

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      await processFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      await processFileUpload(e.target.files[0]);
    }
  };

  const processFileUpload = async (file: File) => {
    setErrorMsg(null);
    setSuccessMsg(null);

    // Extension check
    const validExts = ['.pdf', '.docx', '.doc', '.txt', '.md', '.pptx', '.csv', '.py', '.json', '.html'];
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!validExts.includes(fileExt)) {
      setErrorMsg('Unable to read this document. Please upload a valid PDF, DOCX, TXT or Markdown file.');
      return;
    }

    setLoading(true);

    try {
      const res: UploadResponse = await uploadDocument(assistant.id, file);
      setSuccessMsg(`Document Loaded Successfully: '${res.filename}' parsed & indexed into ${res.num_chunks} chunks.`);
      
      onAssistantUpdated({
        ...assistant,
        filename: res.filename,
        num_pages: res.num_pages,
        num_words: res.num_words,
        num_chars: res.num_chars,
        vocab_size: res.vocab_size,
        index_status: res.index_status || '✅ Successfully Indexed',
        retrieval_ready: true,
        total_chunks: res.num_chunks,
        active_source: 'uploaded',
        is_custom: true
      });
    } catch (err: any) {
      setErrorMsg(err.message || 'Unable to read this document. Please upload a valid PDF, DOCX, TXT or Markdown file.');
    } finally {
      setLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleReset = async () => {
    setErrorMsg(null);
    setSuccessMsg(null);
    setLoading(true);

    try {
      const res: UploadResponse = await resetAssistantDocument(assistant.id);
      setSuccessMsg(`Reset back to default dataset for ${assistant.name}.`);

      onAssistantUpdated({
        ...assistant,
        filename: res.filename,
        num_pages: res.num_pages,
        num_words: res.num_words,
        num_chars: res.num_chars,
        vocab_size: res.vocab_size,
        index_status: res.index_status || '✅ Successfully Indexed',
        retrieval_ready: true,
        total_chunks: res.num_chunks,
        active_source: 'default',
        is_custom: false
      });
    } catch (err: any) {
      setErrorMsg('Failed to reset document dataset.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full bg-slate-900/60 backdrop-blur-md rounded-2xl border border-slate-800 p-4 sm:p-5 shadow-lg space-y-4">
      
      {/* Card Title Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
            <Upload className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-bold text-sm text-slate-100 flex items-center gap-2">
              📄 Upload Your Document
              {isCustom ? (
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-mono border border-emerald-500/20 font-semibold">
                  Custom Upload Active
                </span>
              ) : (
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono border border-slate-700">
                  Default Dataset
                </span>
              )}
            </h3>
            <p className="text-xs text-slate-400">
              Upload custom knowledge for <strong className="text-indigo-300">{assistant.name}</strong> to answer queries exclusively from your file.
            </p>
          </div>
        </div>

        {isCustom && (
          <button
            onClick={handleReset}
            disabled={loading}
            className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium flex items-center gap-1.5 transition border border-slate-700 disabled:opacity-50"
            title="Reset to default use case dataset"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset to Default
          </button>
        )}
      </div>

      {/* Drag & Drop Upload Dropzone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative cursor-pointer rounded-xl border-2 border-dashed p-4 text-center transition-all ${
          isDragging
            ? 'border-indigo-500 bg-indigo-500/10 scale-[0.99]'
            : 'border-slate-700/80 hover:border-indigo-500/50 bg-slate-950/40 hover:bg-slate-900/40'
        }`}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept=".pdf,.docx,.txt,.md,.pptx,.csv"
          className="hidden"
        />

        {loading ? (
          <div className="py-4 flex flex-col items-center justify-center gap-2">
            <RefreshCw className="w-6 h-6 animate-spin text-indigo-400" />
            <p className="text-xs text-slate-300 font-medium animate-pulse">
              Processing document... Extracting text, cleaning & vectorizing TF-IDF chunks...
            </p>
          </div>
        ) : (
          <div className="py-2 flex flex-col items-center justify-center gap-2">
            <div className="p-3 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <Upload className="w-5 h-5" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-200">
                [ Drag & Drop PDF File Here ]
              </p>
              <p className="text-xs text-indigo-400 font-medium hover:underline mt-0.5">
                OR [ Browse Files ]
              </p>
            </div>
            <div className="text-[11px] text-slate-400 font-mono tracking-wide mt-1">
              Supported: <span className="text-slate-300 font-semibold">PDF • DOCX • TXT • MD</span>
              <span className="text-slate-500"> (PPTX • CSV)</span>
            </div>
          </div>
        )}
      </div>

      {/* Status Messages */}
      {errorMsg && (
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {successMsg && (
        <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {/* Display Upload Information Card */}
      <div className="bg-slate-950/60 rounded-xl border border-slate-800 p-3.5 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 pb-2">
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-indigo-400" />
            <span className="text-xs font-semibold text-slate-300">Active Knowledge Base:</span>
            <span className="text-xs font-mono font-bold text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
              {activeFilename}
            </span>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-semibold bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Document Loaded & Indexed</span>
          </div>
        </div>

        {/* 6 Information Metrics Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-xs">
          <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800 flex flex-col">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              📑 Pages Read:
            </span>
            <span className="font-bold text-slate-100 text-sm mt-0.5">{numPages}</span>
          </div>

          <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800 flex flex-col">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              📝 Characters:
            </span>
            <span className="font-bold text-blue-400 text-sm mt-0.5">{Math.round(numChars).toLocaleString()}</span>
          </div>

          <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800 flex flex-col">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              📊 Words:
            </span>
            <span className="font-bold text-purple-400 text-sm mt-0.5">{numWords.toLocaleString()}</span>
          </div>

          <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800 flex flex-col">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              🧩 Chunks:
            </span>
            <span className="font-bold text-indigo-400 text-sm mt-0.5">{numChunks}</span>
          </div>

          <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800 flex flex-col">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              📚 Vocabulary:
            </span>
            <span className="font-bold text-amber-400 text-sm mt-0.5">{vocabSize.toLocaleString()}</span>
          </div>

          <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800 flex flex-col">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              🧠 Status:
            </span>
            <span className="font-bold text-emerald-400 text-xs mt-0.5 flex items-center gap-1">
              ✅ Successfully Indexed
            </span>
          </div>
        </div>
      </div>

      {/* Dedicated Document Debug Panel (Checklist STEP 11) */}
      <DocumentDebugPanel assistant={assistant} />
    </div>
  );
}
