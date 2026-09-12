import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  Send, Menu, Sparkles, Layers, ArrowRight, User, Bot, 
  Compass, Zap, TrendingUp, BookOpen, CheckCircle2 
} from 'lucide-react';
import SourceCard from './SourceCard';

export default function ChatArea({
  session,
  messages,
  isLoading,
  streamingToken,
  onSendMessage,
  onOpenArtifact,
  activeArtifact,
  onToggleSidebar
}) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingToken]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-950/40 backdrop-blur-xl overflow-hidden relative">
      {/* Top Navigation Bar */}
      <header className="h-16 border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-xl px-4 md:px-6 flex items-center justify-between shrink-0 z-10">
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="p-2 text-slate-400 hover:text-white hover:bg-slate-800/60 rounded-xl lg:hidden transition-colors"
          >
            <Menu className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-bold text-white truncate max-w-xs sm:max-w-md tracking-tight">
                {session ? session.title : 'The Lenny Growth Assistant'}
              </h2>
              <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ● Live Knowledge Base
              </span>
            </div>
            <div className="flex items-center gap-2 text-[11px] text-slate-400 mt-0.5">
              <span className="flex items-center gap-1 text-indigo-400 font-medium">
                <Sparkles className="w-3 h-3 text-amber-400" />
                707 Curated Lenny Podcast Chunks • Elena Verna, Brian Balfour, Casey Winters
              </span>
            </div>
          </div>
        </div>

        {activeArtifact && (
          <button
            onClick={() => onOpenArtifact(activeArtifact)}
            className="flex items-center gap-2 py-1.5 px-3 rounded-xl bg-gradient-to-r from-purple-600 via-pink-600 to-orange-500 text-white text-xs font-bold hover:shadow-lg hover:shadow-purple-500/25 transition-all shadow-md active:scale-95"
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Open {activeArtifact.title.slice(0, 18)}...</span>
          </button>
        )}
      </header>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center max-w-2xl mx-auto py-8">
            {/* Multi-color glowing icon */}
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 p-0.5 shadow-xl shadow-purple-500/25 mb-4 animate-gradient">
              <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center text-white">
                <Compass className="w-8 h-8 text-transparent bg-clip-text bg-gradient-to-tr from-sky-400 via-indigo-400 to-pink-400" />
              </div>
            </div>

            <h3 className="text-2xl font-extrabold text-white mb-2 tracking-tight">
              Lenny Growth Assistant
            </h3>
            <p className="text-slate-400 text-sm mb-8 max-w-lg leading-relaxed">
              Ask deep strategy questions grounded strictly in <span className="text-emerald-400 font-semibold">Lenny's Podcast transcripts</span>. 
              Generate <span className="text-purple-400 font-semibold">Ship 30 essays</span> and render <span className="text-orange-400 font-semibold">interactive HTML frameworks</span> natively.
            </p>

            {/* Colorful Strategy Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 w-full text-left">
              {/* Card 1: Emerald Green for Retention */}
              <div
                onClick={() => onSendMessage("How can I improve user retention in B2B SaaS?")}
                className="p-4 rounded-2xl bg-gradient-to-br from-slate-900/90 to-emerald-950/30 border border-emerald-500/30 hover:border-emerald-400/70 hover:shadow-lg hover:shadow-emerald-500/10 cursor-pointer transition-all group"
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400">
                    <TrendingUp className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-bold text-emerald-300">B2B SaaS Retention</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-auto opacity-0 group-hover:opacity-100 transition-opacity text-emerald-400" />
                </div>
                <div className="text-xs text-slate-400 leading-relaxed">
                  Elena Verna & Casey Winters playbook on churn diagnosis and habit loops.
                </div>
              </div>

              {/* Card 2: Neon Purple for Ship 30 */}
              <div
                onClick={() => onSendMessage("Turn this into a Ship 30 for 30 essay about retention")}
                className="p-4 rounded-2xl bg-gradient-to-br from-slate-900/90 to-purple-950/30 border border-purple-500/30 hover:border-purple-400/70 hover:shadow-lg hover:shadow-purple-500/10 cursor-pointer transition-all group"
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className="p-1.5 rounded-lg bg-purple-500/20 text-purple-400">
                    <BookOpen className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-bold text-purple-300">Ship 30 for 30 Essay</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-auto opacity-0 group-hover:opacity-100 transition-opacity text-purple-400" />
                </div>
                <div className="text-xs text-slate-400 leading-relaxed">
                  Generate a ~1,250-word structured piece with 1-3-1 hook rule and subheadings.
                </div>
              </div>

              {/* Card 3: Sunset Orange for Artifact Framework */}
              <div
                onClick={() => onSendMessage("Create a product retention audit framework with an HTML checklist")}
                className="p-4 rounded-2xl bg-gradient-to-br from-slate-900/90 to-orange-950/30 border border-orange-500/30 hover:border-orange-400/70 hover:shadow-lg hover:shadow-orange-500/10 cursor-pointer transition-all group"
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className="p-1.5 rounded-lg bg-orange-500/20 text-orange-400">
                    <Layers className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-bold text-orange-300">Interactive Framework</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-auto opacity-0 group-hover:opacity-100 transition-opacity text-orange-400" />
                </div>
                <div className="text-xs text-slate-400 leading-relaxed">
                  Render native HTML/CSS cards and interactive checklists in the side viewer.
                </div>
              </div>

              {/* Card 4: Cyan / Electric Blue for 40% PMF */}
              <div
                onClick={() => onSendMessage("What is the 40% PMF rule by Sean Ellis?")}
                className="p-4 rounded-2xl bg-gradient-to-br from-slate-900/90 to-sky-950/30 border border-sky-500/30 hover:border-sky-400/70 hover:shadow-lg hover:shadow-sky-500/10 cursor-pointer transition-all group"
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className="p-1.5 rounded-lg bg-sky-500/20 text-sky-400">
                    <CheckCircle2 className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-bold text-sky-300">40% PMF Survey</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-auto opacity-0 group-hover:opacity-100 transition-opacity text-sky-400" />
                </div>
                <div className="text-xs text-slate-400 leading-relaxed">
                  Sean Ellis benchmark test to determine true product-market fit before scaling.
                </div>
              </div>
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role !== 'user' && (
                <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-emerald-500 via-indigo-600 to-pink-500 flex items-center justify-center text-white shrink-0 mt-1 shadow-lg shadow-indigo-500/20 p-0.5">
                  <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
                    <Bot className="w-4 h-4 text-emerald-400" />
                  </div>
                </div>
              )}

              <div
                className={`max-w-2xl rounded-2xl p-5 text-sm leading-relaxed transition-all ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 text-white rounded-tr-sm shadow-lg shadow-indigo-600/20 font-medium'
                    : 'bg-slate-900/90 border border-slate-800 text-slate-200 rounded-tl-sm shadow-md'
                }`}
              >
                {/* Real Markdown Rendering: Eliminates raw stars and hashes */}
                {msg.role === 'user' ? (
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                ) : (
                  <div className="markdown-content">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                )}

                {/* If an artifact is attached to this message */}
                {msg.artifact && (
                  <div className="mt-4 pt-4 border-t border-slate-800/80 flex items-center justify-between gap-3">
                    <div>
                      <div className="text-xs font-bold text-white flex items-center gap-1.5">
                        <Layers className="w-3.5 h-3.5 text-orange-400" />
                        {msg.artifact.title}
                      </div>
                      <div className="text-[11px] text-slate-400">Interactive framework ready in viewer</div>
                    </div>
                    <button
                      onClick={() => onOpenArtifact(msg.artifact)}
                      className="px-3.5 py-2 rounded-xl bg-gradient-to-r from-orange-500 via-pink-600 to-purple-600 hover:from-orange-400 hover:to-purple-500 text-white font-bold text-xs shadow-md shadow-orange-500/20 transition-all active:scale-95 shrink-0"
                    >
                      Open Artifact
                    </button>
                  </div>
                )}

                {/* Grounded Citations */}
                {msg.sources && msg.sources.length > 0 && (
                  <SourceCard sources={msg.sources} />
                )}

                {/* Latency & Skill Badge */}
                {msg.latency_ms && (
                  <div className="mt-3 pt-2 border-t border-slate-800/50 text-[10px] text-slate-500 flex items-center justify-between">
                    <span className="flex items-center gap-1">
                      <Zap className="w-3 h-3 text-amber-400" />
                      Latency: <strong className="text-slate-400 font-mono">{msg.latency_ms}ms</strong>
                    </span>
                    {msg.skill_used && (
                      <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono uppercase text-[9px] font-semibold">
                        Skill: {msg.skill_used}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-purple-600 to-pink-600 flex items-center justify-center text-white shrink-0 mt-1 shadow-md shadow-purple-600/25">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))
        )}

        {/* Streaming message indicator */}
        {isLoading && (
          <div className="flex gap-3.5 justify-start">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-emerald-500 via-indigo-600 to-pink-500 flex items-center justify-center text-white shrink-0 mt-1 shadow-lg shadow-indigo-500/20 p-0.5">
              <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
                <Bot className="w-4 h-4 text-emerald-400" />
              </div>
            </div>
            <div className="max-w-2xl rounded-2xl p-5 text-sm bg-slate-900/90 border border-slate-800 text-slate-200 rounded-tl-sm">
              {streamingToken ? (
                <div className="markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {streamingToken}
                  </ReactMarkdown>
                </div>
              ) : (
                <div className="flex items-center gap-3 text-slate-300 text-xs py-1">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 rounded-full bg-sky-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                  <span className="font-medium text-slate-400">Searching transcripts & synthesizing grounded insights...</span>
                </div>
              )}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Box with Colorful Ring */}
      <div className="p-4 md:p-6 border-t border-slate-800/80 bg-slate-950/80 backdrop-blur-xl shrink-0">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a PM or growth question from Lenny's transcripts (e.g. retention, activation, loops)..."
            disabled={isLoading}
            className="w-full bg-slate-900/90 border border-slate-800 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 text-slate-100 placeholder-slate-500 rounded-2xl px-5 py-3.5 pr-14 text-sm focus:outline-none transition-all shadow-inner"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2.5 p-2.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 disabled:from-slate-800 disabled:to-slate-800 text-white disabled:text-slate-600 rounded-xl transition-all shadow-md active:scale-95"
            title="Send Message"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
