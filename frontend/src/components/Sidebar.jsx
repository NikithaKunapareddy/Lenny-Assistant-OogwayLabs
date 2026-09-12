import React from 'react';
import { 
  Plus, MessageSquare, Trash2, Cpu, Sparkles, 
  TrendingUp, BookOpen, Layers, Repeat, CheckCircle2, ChevronRight 
} from 'lucide-react';

export default function Sidebar({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
  modelInfo,
  onSwitchModel,
  onSelectPreset,
  isOpen,
  onClose
}) {
  const PRESET_PROMPTS = [
    { 
      label: "B2B SaaS Retention", 
      color: "text-emerald-400 border-emerald-500/30 bg-emerald-950/20",
      icon: TrendingUp,
      prompt: "How do I improve user retention in B2B SaaS according to Lenny's guests?" 
    },
    { 
      label: "Ship 30 Retention Essay", 
      color: "text-purple-400 border-purple-500/30 bg-purple-950/20",
      icon: BookOpen,
      prompt: "Turn this into a comprehensive Ship 30 for 30 style essay on retention architecture." 
    },
    { 
      label: "Interactive Growth Framework", 
      color: "text-orange-400 border-orange-500/30 bg-orange-950/20",
      icon: Layers,
      prompt: "Create a product retention audit framework with an interactive HTML checklist." 
    },
    { 
      label: "Brian Balfour Growth Loops", 
      color: "text-sky-400 border-sky-500/30 bg-sky-950/20",
      icon: Repeat,
      prompt: "What does Brian Balfour say about growth loops vs linear funnels?" 
    },
    { 
      label: "Sean Ellis 40% PMF Test", 
      color: "text-amber-400 border-amber-500/30 bg-amber-950/20",
      icon: CheckCircle2,
      prompt: "How do you calculate and apply the 40% product-market fit survey?" 
    }
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/70 backdrop-blur-md lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed lg:static inset-y-0 left-0 z-40 flex flex-col w-72 bg-slate-950/90 border-r border-slate-800/80 backdrop-blur-2xl transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Brand Header */}
        <div className="p-4 border-b border-slate-800/80 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-emerald-500 via-indigo-600 to-pink-500 flex items-center justify-center text-white font-extrabold shadow-lg shadow-indigo-500/30 text-sm">
              L
            </div>
            <div>
              <h1 className="text-sm font-extrabold text-white tracking-tight flex items-center gap-1">
                Lenny Assistant
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              </h1>
              <p className="text-[10px] text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 font-bold uppercase tracking-wider">
                Growth & Strategy Intelligence
              </p>
            </div>
          </div>
        </div>

        {/* New Chat Button */}
        <div className="p-3">
          <button
            onClick={onNewChat}
            className="w-full py-2.5 px-3.5 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-lg shadow-purple-600/20 transition-all active:scale-[0.98]"
          >
            <Plus className="w-4 h-4" />
            New Strategy Chat
          </button>
        </div>

        {/* Model Selector Card */}
        <div className="px-3 py-1">
          <div className="p-3 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 text-xs shadow-inner">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-[11px] font-semibold flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-purple-400" />
                Model Provider
              </span>
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[9px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Active
              </span>
            </div>

            <select
              value={modelInfo?.active_provider || 'ollama'}
              onChange={(e) => onSwitchModel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700/80 text-slate-200 text-xs rounded-xl px-2.5 py-2 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 font-medium"
            >
              <option value="ollama">⚡ Ollama Local (llama3:latest)</option>
              <option value="anthropic">🧠 Anthropic Claude (Cloud)</option>
              <option value="openai">✨ OpenAI GPT-4o (Cloud)</option>
              <option value="mock">🛡️ Grounded Engine (Offline)</option>
            </select>
          </div>
        </div>

        {/* Session History */}
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-2 py-1 flex items-center justify-between">
            <span>Recent Sessions</span>
            <span className="text-[9px] text-slate-600">{sessions.length} chats</span>
          </div>

          {sessions.length === 0 ? (
            <div className="text-center py-8 text-slate-500 text-xs">
              No sessions yet.<br />Ask a question to start!
            </div>
          ) : (
            sessions.map((s) => (
              <div
                key={s.id}
                onClick={() => onSelectSession(s.id)}
                className={`group flex items-center justify-between p-2.5 rounded-xl text-xs cursor-pointer transition-all ${
                  activeSessionId === s.id
                    ? 'bg-gradient-to-r from-indigo-950/80 to-purple-950/40 text-indigo-300 border border-indigo-500/40 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                <div className="flex items-center gap-2 truncate pr-2">
                  <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${activeSessionId === s.id ? 'text-indigo-400' : 'text-slate-500'}`} />
                  <span className="truncate font-medium">{s.title}</span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteSession(s.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 text-slate-500 hover:text-red-400 hover:bg-slate-800 rounded-lg transition-all"
                  title="Delete Session"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            ))
          )}
        </div>

        {/* Multi-Color Quick Strategy Presets */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-950/80">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-2 flex items-center gap-1.5">
            <Sparkles className="w-3 h-3 text-amber-400" />
            Strategy Presets
          </div>
          <div className="space-y-1.5 max-h-40 overflow-y-auto">
            {PRESET_PROMPTS.map((p, idx) => {
              const IconComp = p.icon;
              return (
                <button
                  key={idx}
                  onClick={() => onSelectPreset(p.prompt)}
                  className={`w-full text-left p-2 rounded-xl text-[11px] font-medium border truncate flex items-center gap-2 group transition-all hover:scale-[1.01] ${p.color}`}
                >
                  <IconComp className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate flex-1">{p.label}</span>
                  <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 shrink-0" />
                </button>
              );
            })}
          </div>
        </div>
      </aside>
    </>
  );
}
