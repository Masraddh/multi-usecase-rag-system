'use client';

import React, { useState, useEffect, useRef } from 'react';
import Sidebar from '../../components/Sidebar';
import MessageItem, { Message } from '../../components/MessageItem';
import RetrievalPanel from '../../components/RetrievalPanel';
import FileUploadCard from '../../components/FileUploadCard';
import { fetchAssistants, sendQuery, fetchAssistantDocument, AssistantInfo, ChatResponse, RetrievedChunk } from '../../services/api';
import { Send, Sparkles, Download, Layers, AlertCircle, RefreshCw, FileText, CheckCircle2, Eye, X, Cpu } from 'lucide-react';

export default function ChatPage() {
  const [assistants, setAssistants] = useState<AssistantInfo[]>([]);
  const [selectedAssistant, setSelectedAssistant] = useState<AssistantInfo | null>(null);
  
  // Execution Mode: 'rag' or 'ai'
  const [mode, setMode] = useState<'rag' | 'ai'>('rag');

  // Custom RAG Parameters
  const [maxWords, setMaxWords] = useState<number>(80);
  const [overlap, setOverlap] = useState<number>(15);
  const [topK, setTopK] = useState<number>(3);

  // Chat State
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputQuery, setInputQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Active Retrieval Inspector State
  const [activeRetrievalChunks, setActiveRetrievalChunks] = useState<RetrievedChunk[]>([]);
  const [activeMaxScore, setActiveMaxScore] = useState<number>(0);
  const [showRetrievalPanel, setShowRetrievalPanel] = useState<boolean>(false);

  // Document Fetching Modal State
  const [docModalOpen, setDocModalOpen] = useState<boolean>(false);
  const [docContent, setDocContent] = useState<string>('');
  const [fetchingDoc, setFetchingDoc] = useState<boolean>(false);

  const handleFetchDocument = async () => {
    if (!selectedAssistant) return;
    setFetchingDoc(true);
    setErrorMsg(null);
    try {
      const res = await fetchAssistantDocument(selectedAssistant.id);
      setDocContent(res.text || 'No content found in this document file.');
      setDocModalOpen(true);
    } catch (err: any) {
      setErrorMsg(`Unable to fetch document payload: ${err.message}`);
    } finally {
      setFetchingDoc(false);
    }
  };

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Load assistants on mount
  useEffect(() => {
    fetchAssistants()
      .then((data) => {
        setAssistants(data);
        if (data.length > 0) {
          const initial = data[0];
          setSelectedAssistant(initial);
          setMaxWords(initial.max_words);
          setOverlap(initial.overlap);
          setTopK(initial.top_k);

          // Add welcome message
          setMessages([
            {
              id: 'welcome-1',
              sender: 'assistant',
              content: `Hello! I am your **${initial.name}** (${initial.persona}).\n\nAsk me anything about my knowledge base or upload your own custom document above!`,
              timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }
          ]);
        }
      })
      .catch(() => {
        setErrorMsg('Failed to connect to backend server. Operating in offline demo mode.');
      });
  }, []);

  // Switch assistant handler
  const handleSelectAssistant = (ast: AssistantInfo) => {
    setSelectedAssistant(ast);
    setMaxWords(ast.max_words);
    setOverlap(ast.overlap);
    setTopK(ast.top_k);
    setShowRetrievalPanel(false);

    setMessages([
      {
        id: `welcome-${ast.id}`,
        sender: 'assistant',
        content: `Switched to **${ast.name}** (${ast.persona}).\n\n${ast.description}\n\nFeel free to upload a document or ask a question!`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ]);
  };

  // Assistant updated handler (e.g. document upload or reset)
  const handleAssistantUpdated = (updatedAst: AssistantInfo) => {
    setSelectedAssistant(updatedAst);
    setAssistants((prev) =>
      prev.map((a) => (a.id === updatedAst.id ? updatedAst : a))
    );

    const sourceLabel = updatedAst.is_custom || updatedAst.active_source === 'uploaded' ? 'custom document' : 'default dataset';
    
    setMessages((prev) => [
      ...prev,
      {
        id: `update-${Date.now()}`,
        sender: 'assistant',
        content: `Knowledge base updated for **${updatedAst.name}**! Now using **${updatedAst.filename}** (${sourceLabel}) with **${updatedAst.total_chunks} chunks**. Ready for your questions!`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ]);
  };

  // Submit Query Handler
  const handleSend = async (queryText?: string) => {
    const q = queryText || inputQuery;
    if (!q.trim() || !selectedAssistant || loading) return;

    const userMsg: Message = {
      id: `user-${Date.now()}`,
      sender: 'user',
      content: q.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);
    setErrorMsg(null);

    try {
      const response: ChatResponse = await sendQuery({
        assistant_id: selectedAssistant.id,
        query: q.trim(),
        mode: mode,
        max_words: maxWords,
        overlap: overlap,
        top_k: topK
      });

      const aiMsg: Message = {
        id: `ai-${Date.now()}`,
        sender: 'assistant',
        content: response.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        responseMeta: response
      };

      setMessages((prev) => [...prev, aiMsg]);

      if (response.retrieved_chunks && response.retrieved_chunks.length > 0) {
        setActiveRetrievalChunks(response.retrieved_chunks);
        setActiveMaxScore(response.max_similarity_score);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'An unexpected error occurred while generating answer.');
    } finally {
      setLoading(false);
    }
  };

  // Clear Chat Handler
  const handleClearChat = () => {
    setMessages([]);
    setShowRetrievalPanel(false);
  };

  // Reset App Handler
  const handleResetApp = () => {
    if (selectedAssistant) {
      setMaxWords(selectedAssistant.max_words);
      setOverlap(selectedAssistant.overlap);
      setTopK(selectedAssistant.top_k);
    }
    handleClearChat();
  };

  // Download Transcript Handler
  const handleDownloadTranscript = () => {
    const text = messages
      .map((m) => `[${m.timestamp}] ${m.sender.toUpperCase()}: ${m.content}`)
      .join('\n\n');
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `RAG_Transcript_${selectedAssistant?.id || 'session'}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6 min-h-[calc(100vh-140px)]">
      
      {/* Left Sidebar */}
      <Sidebar
        assistants={assistants}
        selectedAssistant={selectedAssistant}
        onSelectAssistant={handleSelectAssistant}
        mode={mode}
        setMode={setMode}
        maxWords={maxWords}
        setMaxWords={setMaxWords}
        overlap={overlap}
        setOverlap={setOverlap}
        topK={topK}
        setTopK={setTopK}
        onClearChat={handleClearChat}
        onResetApp={handleResetApp}
        apiStatus={!errorMsg}
      />

      {/* Main Chat Studio */}
      <div className="flex-1 flex flex-col glass-panel rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-xl">
        
        {/* Chat Studio Header */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3 bg-slate-100/50 dark:bg-slate-900/50">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-indigo-600 text-white font-bold">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-bold text-base flex items-center gap-2">
                {selectedAssistant?.name || 'RAG Studio'}
                <span className="text-xs px-2 py-0.5 rounded-md bg-indigo-500/10 text-indigo-400 font-mono font-medium border border-indigo-500/20">
                  {selectedAssistant?.persona}
                </span>
              </h2>
              <p className="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
                <span>Chunk Size: {maxWords}w | Overlap: {overlap}w | Top-K: {topK}</span>
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* Mode Selection Button Group */}
            <div className="flex items-center gap-1 p-1 rounded-xl bg-slate-900/80 border border-slate-800">
              <button
                onClick={() => setMode('rag')}
                className={`px-3 py-1.5 rounded-lg text-xs font-extrabold transition flex items-center gap-1.5 ${
                  mode === 'rag'
                    ? 'bg-electric-500 text-white shadow-glow-blue'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <span>🧠</span> RAG Mode
              </button>
              <button
                onClick={() => setMode('ai')}
                className={`px-3 py-1.5 rounded-lg text-xs font-extrabold transition flex items-center gap-1.5 ${
                  mode === 'ai'
                    ? 'bg-purpleAccent-500 text-white shadow-glow-purple'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <span>🤖</span> Pure AI Mode
              </button>
            </div>

            {activeRetrievalChunks.length > 0 && mode === 'rag' && (
              <button
                onClick={() => setShowRetrievalPanel(!showRetrievalPanel)}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition ${
                  showRetrievalPanel
                    ? 'bg-indigo-600 text-white'
                    : 'glass-panel text-slate-300 hover:text-indigo-400'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                {showRetrievalPanel ? 'Hide Vector Panel' : `Inspect Chunks (${activeRetrievalChunks.length})`}
              </button>
            )}

            <button
              onClick={handleDownloadTranscript}
              disabled={messages.length === 0}
              className="p-2 rounded-xl glass-panel text-slate-400 hover:text-indigo-400 disabled:opacity-40 transition"
              title="Download Conversation Transcript"
            >
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Dynamic File Upload Component (Visible for ALL 5 Use Cases) */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-950/40">
          <FileUploadCard
            assistant={selectedAssistant}
            onAssistantUpdated={handleAssistantUpdated}
          />
        </div>

        {/* Active Document Indicator Bar Above Chat Messages */}
        <div className="px-6 py-2.5 bg-indigo-950/40 border-b border-indigo-500/20 flex flex-wrap items-center justify-between gap-2 text-xs">
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-indigo-400" />
            <span className="text-slate-300 font-medium">Active Knowledge Base:</span>
            <span className="font-mono font-bold text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20 flex items-center gap-1">
              {selectedAssistant?.filename || 'default_dataset.txt'}
              <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            </span>

            <button
              onClick={handleFetchDocument}
              disabled={fetchingDoc}
              className="px-2.5 py-1 rounded-lg bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 border border-indigo-500/30 text-xs font-semibold flex items-center gap-1.5 transition disabled:opacity-50"
              title="Fetch raw document content from backend"
            >
              {fetchingDoc ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Eye className="w-3.5 h-3.5" />}
              Fetch & View Document
            </button>
          </div>
          <div className="text-slate-400 font-mono text-[11px]">
            {selectedAssistant?.total_chunks || 0} Chunks Indexing Active • {mode === 'rag' ? 'Grounded RAG Mode' : 'Pure AI Mode'}
          </div>
        </div>

        {/* Retrieval Panel Drawer */}
        <div className="px-4 pt-2">
          <RetrievalPanel
            chunks={activeRetrievalChunks}
            maxScore={activeMaxScore}
            isOpen={showRetrievalPanel}
            onClose={() => setShowRetrievalPanel(false)}
          />
        </div>

        {/* Chat Messages Body */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 max-h-[500px]">
          
          {messages.map((msg) => (
            <MessageItem key={msg.id} message={msg} />
          ))}

          {/* Loading Skeleton */}
          {loading && (
            <div className="flex gap-4 p-4 rounded-2xl glass-panel animate-pulse">
              <div className="w-9 h-9 rounded-xl bg-indigo-600/30 shrink-0" />
              <div className="space-y-2 flex-1">
                <div className="h-3 bg-slate-700/50 rounded w-24" />
                <div className="h-4 bg-slate-700/30 rounded w-3/4" />
                <div className="h-4 bg-slate-700/30 rounded w-1/2" />
              </div>
            </div>
          )}

          {/* Error Banner */}
          {errorMsg && (
            <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Sample Prompt Chips */}
        {selectedAssistant?.sample_queries && (
          <div className="px-4 py-2 border-t border-slate-200/60 dark:border-slate-800/60 bg-slate-900/30 flex items-center gap-2 overflow-x-auto text-xs">
            <span className="text-[11px] font-semibold text-slate-400 shrink-0">Try Query:</span>
            {selectedAssistant.sample_queries.map((sq, i) => (
              <button
                key={i}
                onClick={() => handleSend(sq)}
                className="px-3 py-1 rounded-full glass-panel hover:bg-indigo-600 hover:text-white transition text-slate-300 text-ellipsis whitespace-nowrap shrink-0 border border-slate-700/50"
              >
                "{sq}"
              </button>
            ))}
          </div>
        )}

        {/* Input Bar */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-100/50 dark:bg-slate-900/50">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              placeholder={`Ask ${selectedAssistant?.name || 'assistant'} based on ${selectedAssistant?.filename || 'document'}...`}
              disabled={loading}
              className="flex-1 bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 text-slate-900 dark:text-slate-100 placeholder-slate-400 transition"
            />
            <button
              type="submit"
              disabled={loading || !inputQuery.trim()}
              className="px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-sm shadow-md shadow-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center gap-2"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              Send
            </button>
          </form>
        </div>

      </div>

      {/* Document Content View Modal */}
      {docModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 max-w-3xl w-full space-y-4 shadow-2xl relative max-h-[85vh] flex flex-col">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-electric-400" />
                <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                  Active Document Payload: <span className="font-mono text-electric-300 bg-electric-500/10 px-2 py-0.5 rounded border border-electric-500/20">{selectedAssistant?.filename}</span>
                </h3>
              </div>
              <button
                onClick={() => setDocModalOpen(false)}
                className="p-1.5 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 rounded-xl bg-slate-950/90 border border-slate-800 text-xs font-mono text-slate-300 leading-relaxed whitespace-pre-wrap shadow-inner">
              {docContent}
            </div>

            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-800 pt-3 text-xs">
              <span className="text-slate-400 font-mono">
                Total Characters: <strong className="text-slate-200 font-bold">{docContent.length.toLocaleString()}</strong> | Words: <strong className="text-purple-400 font-bold">{docContent.split(/\s+/).filter(Boolean).length.toLocaleString()}</strong>
              </span>
              <button
                onClick={() => {
                  const blob = new Blob([docContent], { type: 'text/plain' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = selectedAssistant?.filename || 'document.txt';
                  a.click();
                  URL.revokeObjectURL(url);
                }}
                className="px-4 py-2 rounded-xl bg-electric-500 hover:bg-electric-600 text-white font-bold text-xs shadow-glow-blue flex items-center gap-1.5 transition"
              >
                <Download className="w-4 h-4" /> Download Document File
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
