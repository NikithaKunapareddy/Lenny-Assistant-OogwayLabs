import React, { useState, useEffect } from 'react';
import './index.css';
import './App.css';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import ArtifactViewer from './components/ArtifactViewer';
import { api } from './services/api';

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [activeSession, setActiveSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeArtifact, setActiveArtifact] = useState(null);
  const [isArtifactOpen, setIsArtifactOpen] = useState(false);
  const [modelInfo, setModelInfo] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false); // only used for mobile overlay
  const [theme, setTheme] = useState(() => localStorage.getItem('lenny-theme') || 'dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('lenny-theme', theme);
  }, [theme]);

  useEffect(() => { loadModels(); loadSessions(); }, []);
  useEffect(() => { if (activeSessionId) loadSessionDetails(activeSessionId); }, [activeSessionId]);

  const loadModels = async () => {
    try { setModelInfo(await api.getModels()); } catch {}
  };

  const loadSessions = async () => {
    try {
      const data = await api.getSessions();
      setSessions(data);
      if (data.length > 0 && !activeSessionId) setActiveSessionId(data[0].id);
    } catch {}
  };

  const loadSessionDetails = async (id) => {
    try {
      const data = await api.getSession(id);
      setActiveSession(data);
      setMessages(data.messages || []);
      if (data.artifacts?.length > 0) { setActiveArtifact(data.artifacts[0]); }
      else { setActiveArtifact(null); setIsArtifactOpen(false); }
    } catch {}
  };

  const handleNewChat = async () => {
    try {
      const s = await api.createSession('New chat', modelInfo?.active_provider);
      setSessions([s, ...sessions]);
      setActiveSessionId(s.id);
      setActiveSession(s);
      setMessages([]);
      setActiveArtifact(null);
      setIsArtifactOpen(false);
      setSidebarOpen(false);
    } catch {}
  };

  const handleDeleteSession = async (id) => {
    try {
      await api.deleteSession(id);
      const remaining = sessions.filter(s => s.id !== id);
      setSessions(remaining);
      if (activeSessionId === id) {
        if (remaining.length > 0) { setActiveSessionId(remaining[0].id); }
        else { setActiveSessionId(null); setActiveSession(null); setMessages([]); setActiveArtifact(null); setIsArtifactOpen(false); }
      }
    } catch {}
  };

  const handleRenameSession = async (id, title) => {
    try {
      await api.renameSession(id, title);
      setSessions(prev => prev.map(s => s.id === id ? { ...s, title } : s));
      if (activeSessionId === id) setActiveSession(prev => ({ ...prev, title }));
    } catch {}
  };

  const handleSwitchModel = async (provider) => {
    try {
      const res = await api.switchModel(provider);
      setModelInfo(prev => ({ ...prev, active_provider: res.active_provider }));
    } catch {}
  };

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setIsLoading(true);
    try {
      const res = await api.sendChatMessage(activeSessionId, text, modelInfo?.active_provider);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.response,
        sources: res.sources,
        artifact: res.artifact,
        latency_ms: res.latency_ms,
        skill_used: res.skill_used,
      }]);
      if (res.artifact) { setActiveArtifact(res.artifact); setIsArtifactOpen(true); }
      if (!activeSessionId && res.session_id) setActiveSessionId(res.session_id);
      loadSessions();
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${err.message || 'Please try again.'}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = async () => {
    if (activeSessionId) {
      try {
        await api.clearSessionMessages(activeSessionId);
      } catch {}
    }
    setMessages([]);
    setActiveArtifact(null);
    setIsArtifactOpen(false);
    loadSessions();
  };

  return (
    <div className="app">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={id => { setActiveSessionId(id); if (window.innerWidth < 768) setSidebarOpen(false); }}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
        onRenameSession={handleRenameSession}
        modelInfo={modelInfo}
        onSwitchModel={handleSwitchModel}
        onSelectPreset={text => { handleSendMessage(text); if (window.innerWidth < 768) setSidebarOpen(false); }}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <ChatArea
        session={activeSession}
        messages={messages}
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
        onOpenArtifact={art => { setActiveArtifact(art); setIsArtifactOpen(true); }}
        activeArtifact={activeArtifact}
        onToggleSidebar={() => setSidebarOpen(o => !o)}
        modelInfo={modelInfo}
        onSwitchModel={handleSwitchModel}
        onClearChat={handleClearChat}
        theme={theme}
        onToggleTheme={() => setTheme(t => t === 'dark' ? 'light' : 'dark')}
      />

      {isArtifactOpen && activeArtifact && (
        <ArtifactViewer
          artifact={activeArtifact}
          appTheme={theme}
          onClose={() => setIsArtifactOpen(false)}
        />
      )}
    </div>
  );
}
