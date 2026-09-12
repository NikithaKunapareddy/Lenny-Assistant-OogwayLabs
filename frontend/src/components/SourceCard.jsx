import React, { useState } from 'react';
import { BookOpen, ExternalLink, Clock, User, ChevronDown, ChevronUp } from 'lucide-react';

export default function SourceCard({ sources }) {
  const [expanded, setExpanded] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-4 pt-3 border-t border-slate-700/60">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between w-full text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition-colors py-1 px-2 rounded-lg bg-indigo-950/30 hover:bg-indigo-950/50 border border-indigo-800/40"
      >
        <span className="flex items-center gap-1.5">
          <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
          Grounded Sources ({sources.length} Lenny Podcast Citations)
        </span>
        {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
      </button>

      {expanded && (
        <div className="mt-3 space-y-2.5 animate-fadeIn">
          {sources.map((src, idx) => (
            <div
              key={idx}
              className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 text-xs transition-all"
            >
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-indigo-500/20 text-indigo-300 font-bold text-[10px]">
                    {idx + 1}
                  </span>
                  <span className="font-semibold text-slate-200 flex items-center gap-1">
                    <User className="w-3 h-3 text-slate-400" />
                    {src.guest}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="flex items-center gap-1 text-[11px] text-slate-400 font-mono bg-slate-800/70 px-1.5 py-0.5 rounded">
                    <Clock className="w-3 h-3 text-slate-500" />
                    {src.timestamp}
                  </span>
                  {src.youtube_url && (
                    <a
                      href={src.youtube_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-indigo-400 hover:text-indigo-300 flex items-center gap-0.5"
                      title="Watch on YouTube"
                    >
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              </div>

              <div className="text-slate-400 text-[11px] mb-2 font-medium truncate">
                {src.title}
              </div>

              <div className="p-2 rounded bg-slate-950/70 border border-slate-800/80 text-slate-300 text-[11px] font-mono leading-relaxed max-h-32 overflow-y-auto italic">
                "{src.content}"
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
