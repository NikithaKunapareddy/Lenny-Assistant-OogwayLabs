import React, { useState, useRef, useEffect } from 'react';
import {
  Plus, MessageSquare, Trash2,
  TrendingUp, BookOpen, Layers, RefreshCw, CheckCircle2,
  Pencil, Check, X
} from 'lucide-react';

const PRESETS = [
  { label: 'B2B SaaS Retention', icon: TrendingUp, prompt: "How do I improve user retention in B2B SaaS according to Lenny's guests?" },
  { label: 'Ship 30 Essay', icon: BookOpen, prompt: "Write a Ship 30 for 30 essay about retention architecture in SaaS." },
  { label: 'Growth Framework HTML', icon: Layers, prompt: "Create a product retention audit framework with an interactive HTML checklist." },
  { label: 'Growth Loops vs Funnels', icon: RefreshCw, prompt: "What does Brian Balfour say about growth loops vs linear funnels?" },
  { label: '40% PMF Test', icon: CheckCircle2, prompt: "How do you calculate and apply the 40% product-market fit survey?" },
];

export const MODEL_META = {
  ollama:    { label: 'Ollama Local',        badge: 'local' },
  anthropic: { label: 'Claude (Cloud)',       badge: 'cloud' },
  openai:    { label: 'GPT-4o (Cloud)',        badge: 'cloud' },
  mock:      { label: 'Grounded Engine',      badge: 'offline' },
};

export default function Sidebar({
  sessions, activeSessionId, onSelectSession, onNewChat,
  onDeleteSession, onRenameSession, modelInfo, onSwitchModel,
  onSelectPreset, isOpen, onClose
}) {
  const [renamingId, setRenamingId] = useState(null);
  const [renameVal, setRenameVal] = useState('');
  const renameRef = useRef(null);

  useEffect(() => {
    if (renamingId && renameRef.current) renameRef.current.focus();
  }, [renamingId]);

  const startRename = (s, e) => {
    e.stopPropagation();
    setRenamingId(s.id);
    setRenameVal(s.title);
  };

  const commitRename = async (id) => {
    if (renameVal.trim()) await onRenameSession(id, renameVal.trim());
    setRenamingId(null);
  };

  const cancelRename = () => setRenamingId(null);

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="overlay"
          onClick={onClose}
          style={{ display: window.innerWidth < 768 ? 'block' : 'none' }}
        />
      )}

      {/* Sidebar — always visible on desktop, slide-in on mobile */}
      <aside className={`sidebar${window.innerWidth < 768 && isOpen ? ' sidebar--open' : ''}`}>
        {/* Logo */}
        <div className="sb-logo">
          <div className="sb-logo-mark">L</div>
          <span className="sb-logo-name">Lenny Assistant</span>
        </div>

        {/* New Chat */}
        <button className="sb-new-btn" onClick={onNewChat}>
          <Plus size={15} />
          New chat
        </button>

        {/* Sessions */}
        <div className="sb-scroll">
          {sessions.length === 0 ? (
            <div className="sb-empty">No conversations yet.<br />Ask something to get started.</div>
          ) : (
            <>
              <div className="sb-section-label">Recent</div>
              {sessions.map(s => (
                <div
                  key={s.id}
                  className={`session-item${activeSessionId === s.id ? ' session-item--active' : ''}`}
                  onClick={() => { if (renamingId !== s.id) { onSelectSession(s.id); onClose(); } }}
                >
                  <MessageSquare size={13} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />

                  {renamingId === s.id ? (
                    <>
                      <input
                        ref={renameRef}
                        className="session-item__input"
                        value={renameVal}
                        onChange={e => setRenameVal(e.target.value)}
                        onKeyDown={e => { if (e.key === 'Enter') commitRename(s.id); if (e.key === 'Escape') cancelRename(); }}
                        onClick={e => e.stopPropagation()}
                      />
                      <div className="session-item__actions" style={{ opacity: 1 }}>
                        <button className="session-item__btn" onClick={e => { e.stopPropagation(); commitRename(s.id); }} title="Save">
                          <Check size={12} />
                        </button>
                        <button className="session-item__btn" onClick={e => { e.stopPropagation(); cancelRename(); }} title="Cancel">
                          <X size={12} />
                        </button>
                      </div>
                    </>
                  ) : (
                    <>
                      <span className="session-item__text">{s.title}</span>
                      <div className="session-item__actions">
                        <button className="session-item__btn" onClick={e => startRename(s, e)} title="Rename">
                          <Pencil size={11} />
                        </button>
                        <button
                          className="session-item__btn session-item__btn--danger"
                          onClick={e => { e.stopPropagation(); onDeleteSession(s.id); }}
                          title="Delete"
                        >
                          <Trash2 size={11} />
                        </button>
                      </div>
                    </>
                  )}
                </div>
              ))}
            </>
          )}
        </div>

        {/* Quick Presets */}
        <div className="sb-presets">
          <div className="sb-section-label" style={{ padding: '6px 4px 5px' }}>Try these</div>
          {PRESETS.map((p, i) => {
            const Icon = p.icon;
            return (
              <button key={i} className="preset-pill"
                onClick={() => { onSelectPreset(p.prompt); onClose(); }}>
                <Icon size={12} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
                <span className="preset-pill__text">{p.label}</span>
              </button>
            );
          })}
        </div>

      </aside>
    </>
  );
}
