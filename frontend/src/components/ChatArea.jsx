import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Send, Menu, Layers, TrendingUp, BookOpen,
  RefreshCw, CheckCircle2, Zap, ChevronDown, Sun, Moon
} from 'lucide-react';
import SourceCard from './SourceCard';
import { MODEL_META } from './Sidebar';

const STARTER_CARDS = [
  { title: 'B2B SaaS Retention', sub: 'Elena Verna & Casey Winters on churn and habit loops.', icon: TrendingUp, prompt: 'How can I improve user retention in B2B SaaS?' },
  { title: 'Ship 30 Essay', sub: 'Generate a ~1,250-word piece with 1-3-1 hook rule.', icon: BookOpen, prompt: 'Write a Ship 30 for 30 essay about product retention architecture.' },
  { title: 'Interactive Framework', sub: 'Render native HTML checklists in the side viewer.', icon: Layers, prompt: 'Create a product retention audit framework with an interactive HTML checklist.' },
  { title: 'PMF Survey Method', sub: "Sean Ellis' 40% benchmark test for product-market fit.", icon: CheckCircle2, prompt: 'What is the 40% PMF rule by Sean Ellis and how do I apply it?' },
];

export default function ChatArea({
  session, messages, isLoading, onSendMessage,
  onOpenArtifact, activeArtifact, onToggleSidebar,
  modelInfo, onSwitchModel, onClearChat, onExportChat,
  theme, onToggleTheme
}) {
  const [input, setInput] = useState('');
  const [showCtx, setShowCtx] = useState(false);
  const [showModelPill, setShowModelPill] = useState(false);
  const [summaryModal, setSummaryModal] = useState(false);
  const [summaryData, setSummaryData] = useState({ text: null, loading: false });
  const [copyToast, setCopyToast] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const ctxRef = useRef(null);
  const modelPillRef = useRef(null);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, isLoading]);

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 180) + 'px';
  }, [input]);

  // Close dropdowns on outside click
  useEffect(() => {
    const handler = (e) => {
      if (ctxRef.current && !ctxRef.current.contains(e.target)) setShowCtx(false);
      if (modelPillRef.current && !modelPillRef.current.contains(e.target)) setShowModelPill(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e); }
  };

  // Build chat summary from messages
  const buildSummary = () => {
    if (!messages || messages.length === 0) return 'No messages yet.';
    const pairs = [];
    for (let i = 0; i < messages.length; i += 2) {
      const q = messages[i]?.content || '';
      const a = messages[i + 1]?.content || '';
      if (q) pairs.push(`**Q:** ${q.slice(0, 120)}${q.length > 120 ? '…' : ''}\n**A:** ${a.slice(0, 200)}${a.length > 200 ? '…' : ''}`);
    }
    return pairs.join('\n\n---\n\n') || 'No messages.';
  };

  const handleCopyChat = () => {
    const text = messages.map(m => `[${m.role.toUpperCase()}]\n${m.content}`).join('\n\n---\n\n');
    navigator.clipboard.writeText(text).then(() => {
      setCopyToast(true);
      setTimeout(() => setCopyToast(false), 2000);
    });
    setShowCtx(false);
  };

  const handleExport = () => {
    const text = messages.map(m => `[${m.role.toUpperCase()}]\n${m.content}`).join('\n\n---\n\n');
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${session?.title || 'chat'}.txt`; a.click();
    URL.revokeObjectURL(url);
    setShowCtx(false);
  };

  const activeModel = MODEL_META[modelInfo?.active_provider];

  return (
    <div className="main">
      {/* Topbar */}
      <header className="topbar">
        <div className="topbar__left">
          {/* Hamburger = Actions Menu (not sidebar toggle) */}
          <div style={{ position: 'relative' }} ref={ctxRef}>
            <button
              className="icon-btn"
              onClick={() => setShowCtx(v => !v)}
              aria-label="Chat actions"
              title="Chat actions"
            >
              <Menu size={18} />
            </button>

            {showCtx && (
              <div className="ham-menu glass">
                <div className="ham-menu__title">Chat Actions</div>
                <button className="ham-item" onClick={async () => {
                  setShowCtx(false);
                  setSummaryModal(true);
                  if (messages.length === 0) return;
                  setSummaryData({ text: null, loading: true });
                  try {
                    const res = await api.summarizeSession(session.id, modelInfo?.active_provider);
                    setSummaryData({ text: res.summary, loading: false });
                  } catch (err) {
                    setSummaryData({ text: 'Failed to generate summary.', loading: false });
                  }
                }}>
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                  Summarize this chat
                </button>
                <button className="ham-item" onClick={() => { handleCopyChat(); setShowCtx(false); }} disabled={messages.length === 0}>
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                  Copy all messages
                </button>
                <button className="ham-item" onClick={() => { handleExport(); setShowCtx(false); }} disabled={messages.length === 0}>
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  Extract as .txt
                </button>
                <div className="ham-sep" />
                <button
                  className="ham-item ham-item--danger"
                  onClick={() => { if (window.confirm('Clear all messages in this chat?')) { onClearChat(); setShowCtx(false); } }}
                  disabled={messages.length === 0}
                >
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
                  Clear this chat
                </button>
              </div>
            )}
          </div>

          <span className="topbar__title">{session?.title || 'Lenny Growth Assistant'}</span>
        </div>

        <div className="topbar__right">
          {activeArtifact && (
            <button
              onClick={() => onOpenArtifact(activeArtifact)}
              style={{
                display: 'flex', alignItems: 'center', gap: 6,
                padding: '5px 12px', borderRadius: 8,
                border: '1px solid var(--border)',
                background: 'var(--bg-elevated)',
                color: 'var(--text)', fontSize: 13, fontWeight: 500,
                cursor: 'pointer', fontFamily: 'var(--font)',
                transition: 'background 0.12s'
              }}
            >
              <Layers size={13} /> View Artifact
            </button>
          )}

          {onToggleTheme && (
            <button
              className="icon-btn"
              onClick={onToggleTheme}
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
              aria-label="Toggle theme"
              style={{ width: 34, height: 34, borderRadius: 8 }}
            >
              {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
            </button>
          )}
        </div>
      </header>

      {/* Copy toast */}
      {copyToast && (
        <div style={{
          position: 'fixed', bottom: 100, left: '50%', transform: 'translateX(-50%)',
          background: 'var(--bg-elevated)', border: '1px solid var(--border)',
          borderRadius: 10, padding: '8px 18px', fontSize: 13, fontWeight: 500,
          color: 'var(--text)', boxShadow: 'var(--shadow-md)', zIndex: 999,
          animation: 'fadeUp 0.2s ease'
        }}>
          Copied to clipboard ✓
        </div>
      )}

      {/* Messages */}
      <div className="messages">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">
              <RefreshCw size={21} color="#0f0f0f" />
            </div>
            <h1 className="welcome-title">Lenny Growth Assistant</h1>
            <p className="welcome-sub">
              Ask strategy questions grounded in{' '}
              <strong>Lenny's Podcast transcripts</strong> — 707 curated chunks from Elena Verna,
              Brian Balfour, Casey Winters, Sean Ellis, and more.
            </p>
            <div className="welcome-grid">
              {STARTER_CARDS.map((c, i) => {
                const Icon = c.icon;
                return (
                  <button key={i} className="welcome-card" onClick={() => onSendMessage(c.prompt)}>
                    <div className="welcome-card__title">
                      <Icon size={13} style={{ color: 'var(--accent)' }} />
                      {c.title}
                    </div>
                    <div className="welcome-card__sub">{c.sub}</div>
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="messages-inner">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-row message-row--${msg.role}`}>
                <div className={`msg-avatar msg-avatar--${msg.role === 'user' ? 'user' : 'ai'}`}>
                  {msg.role === 'user' ? (
                    /* Facebook-style default person SVG */
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                      <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                    </svg>
                  ) : 'L'}
                </div>
                <div className="msg-body">
                  {msg.role === 'user' ? (
                    <div className="msg-bubble--user">{msg.content}</div>
                  ) : (
                    <div className="msg-ai-content">
                      <div className="prose">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                      </div>
                      {msg.artifact && (
                        <div className="artifact-inline">
                          <div className="artifact-inline__header">
                            <div className="artifact-inline__label">
                              <Layers size={13} /> {msg.artifact.title}
                            </div>
                            <button className="artifact-inline__open" onClick={() => onOpenArtifact(msg.artifact)}>
                              Open →
                            </button>
                          </div>
                        </div>
                      )}
                      {msg.sources?.length > 0 && <SourceCard sources={msg.sources} />}
                      {msg.latency_ms && (
                        <div className="msg-meta">
                          <Zap size={11} />
                          <span>{msg.latency_ms}ms</span>
                          {msg.skill_used && <span className="msg-meta__badge">{msg.skill_used}</span>}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* Premium loading animation — dots only */}
            {isLoading && (
              <div className="message-row anim-fadeUp">
                <div className="msg-avatar msg-avatar--ai">L</div>
                <div className="msg-body">
                  <div className="typing-indicator">
                    <div className="typing-dot" />
                    <div className="typing-dot" />
                    <div className="typing-dot" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* ── Input area ── */}
      <div className="input-wrap">
        <div className="input-shell">
          <form onSubmit={handleSubmit}>
            <div className="input-container">
              <textarea
                ref={textareaRef}
                className="input-textarea"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a growth or product question from Lenny's Podcast…"
                disabled={isLoading}
                rows={1}
                aria-label="Message input"
              />

              <div className="input-right">
                {/* Model pill dropdown — Gemini-style */}
                <div style={{ position: 'relative' }} ref={modelPillRef}>
                  <button
                    type="button"
                    className="model-pill"
                    onClick={() => setShowModelPill(v => !v)}
                    title="Change model"
                  >
                    <span style={{ fontSize: 11.5 }}>
                      {activeModel?.label || 'Grounded Engine'}
                    </span>
                    <ChevronDown size={11} />
                  </button>

                  {showModelPill && (
                    <div className="model-pill-dropdown">
                      {Object.entries(MODEL_META).map(([key, m]) => (
                        <button
                          key={key}
                          type="button"
                          className={`model-option${modelInfo?.active_provider === key ? ' model-option--active' : ''}`}
                          onClick={() => { onSwitchModel(key); setShowModelPill(false); }}
                        >
                          {modelInfo?.active_provider === key
                            ? <span className="model-option__dot" />
                            : <span className="model-option__spacer" />}
                          <span className="model-option__label">{m.label}</span>
                          <span className="model-option__badge">{m.badge}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                {/* Send */}
                <button
                  type="submit"
                  className={`send-btn${input.trim() && !isLoading ? ' send-btn--active' : ''}`}
                  disabled={!input.trim() || isLoading}
                  aria-label="Send message"
                >
                  <Send size={15} />
                </button>
              </div>
            </div>
          </form>

          <div className="input-hint">Enter to send · Shift+Enter for newline</div>
        </div>
      </div>

      {/* Summary modal */}
      {summaryModal && (
        <div className="modal-backdrop" onClick={() => setSummaryModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal__header">
              <span className="modal__title">📋 Chat Summary</span>
              <button className="icon-btn" onClick={() => setSummaryModal(false)}><span style={{ fontSize: 18 }}>×</span></button>
            </div>
            <div className="modal__body">
              {messages.length === 0
                ? <p style={{ color: 'var(--text-muted)' }}>No messages in this chat yet.</p>
                : (
                  <>
                    <p style={{ marginBottom: 16, color: 'var(--text-muted)', fontSize: 13 }}>
                      Generated by <strong>{modelInfo?.active_provider || 'AI'}</strong> for session: <em>{session?.title}</em>
                    </p>
                    
                    {summaryData.loading ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-muted)' }}>
                        <div className="typing-dot" style={{ background: 'var(--accent)' }} />
                        <div className="typing-dot" style={{ background: 'var(--accent)' }} />
                        <div className="typing-dot" style={{ background: 'var(--accent)' }} />
                        <span style={{ fontSize: 13, marginLeft: 8 }}>Reading conversation...</span>
                      </div>
                    ) : (
                      <div className="md-content glass" style={{ 
                        padding: '14px 18px', 
                        borderRadius: 12, 
                        background: 'var(--bg-hover)', 
                        border: '1px solid var(--border)' 
                      }}>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {summaryData.text || ''}
                        </ReactMarkdown>
                      </div>
                    )}
                  </>
                )}
            </div>
            <div className="modal__footer">
              <button className="btn" onClick={() => setSummaryModal(false)}>Close</button>
              <button className="btn btn--accent" onClick={() => { handleCopyChat(); setSummaryModal(false); }}>Copy all</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
