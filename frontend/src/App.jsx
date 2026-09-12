import React, { useState, useEffect } from 'react';
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
  const [streamingToken, setStreamingToken] = useState('');
  const [activeArtifact, setActiveArtifact] = useState(null);
  const [isArtifactViewerOpen, setIsArtifactViewerOpen] = useState(false);
  const [modelInfo, setModelInfo] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Initialize: Load models and sessions
  useEffect(() => {
    loadModels();
    loadSessions();
  }, []);

  // When active session changes, load details
  useEffect(() => {
    if (activeSessionId) {
      loadSessionDetails(activeSessionId);
    }
  }, [activeSessionId]);

  const loadModels = async () => {
    try {
      const data = await api.getModels();
      setModelInfo(data);
    } catch (err) {
      console.error('Failed to load models:', err);
    }
  };

  const loadSessions = async () => {
    try {
      const data = await api.getSessions();
      setSessions(data);
      if (data.length > 0 && !activeSessionId) {
        setActiveSessionId(data[0].id);
      }
    } catch (err) {
      console.error('Failed to load sessions:', err);
    }
  };

  const loadSessionDetails = async (sessionId) => {
    try {
      const data = await api.getSession(sessionId);
      setActiveSession(data);
      setMessages(data.messages || []);

      // If the session has an artifact, set it
      if (data.artifacts && data.artifacts.length > 0) {
        setActiveArtifact(data.artifacts[0]);
      } else {
        setActiveArtifact(null);
        setIsArtifactViewerOpen(false);
      }
    } catch (err) {
      console.error('Failed to load session details:', err);
    }
  };

  const handleNewChat = async () => {
    try {
      const newSess = await api.createSession('New Strategy Chat', modelInfo?.active_provider);
      setSessions([newSess, ...sessions]);
      setActiveSessionId(newSess.id);
      setActiveSession(newSess);
      setMessages([]);
      setActiveArtifact(null);
      setIsArtifactViewerOpen(false);
      setSidebarOpen(false);
    } catch (err) {
      console.error('Failed to create session:', err);
    }
  };

  const handleDeleteSession = async (sessionId) => {
    try {
      await api.deleteSession(sessionId);
      const remaining = sessions.filter((s) => s.id !== sessionId);
      setSessions(remaining);
      if (activeSessionId === sessionId) {
        if (remaining.length > 0) {
          setActiveSessionId(remaining[0].id);
        } else {
          setActiveSessionId(null);
          setActiveSession(null);
          setMessages([]);
          setActiveArtifact(null);
          setIsArtifactViewerOpen(false);
        }
      }
    } catch (err) {
      console.error('Failed to delete session:', err);
    }
  };

  const handleSwitchModel = async (provider) => {
    try {
      const res = await api.switchModel(provider);
      setModelInfo((prev) => ({ ...prev, active_provider: res.active_provider }));
    } catch (err) {
      console.error('Failed to switch model:', err);
    }
  };

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    // Optimistically append user message
    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setStreamingToken('');

    try {
      const res = await api.sendChatMessage(activeSessionId, text, modelInfo?.active_provider);

      // Assistant response
      const assistantMsg = {
        role: 'assistant',
        content: res.response,
        sources: res.sources,
        artifact: res.artifact,
        latency_ms: res.latency_ms,
        skill_used: res.skill_used
      };

      setMessages((prev) => [...prev, assistantMsg]);

      // If an artifact was generated, open the viewer automatically!
      if (res.artifact) {
        setActiveArtifact(res.artifact);
        setIsArtifactViewerOpen(true);
      }

      // If activeSessionId was null, set it to the newly created session
      if (!activeSessionId) {
        setActiveSessionId(res.session_id);
      }

      loadSessions(); // refresh titles
    } catch (err) {
      console.error('Chat error:', err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Error: ${err.message || 'Failed to generate response'}. Please try again.`
        }
      ]);
    } finally {
      setIsLoading(false);
      setStreamingToken('');
    }
  };

  const handleOpenArtifact = (art) => {
    setActiveArtifact(art);
    setIsArtifactViewerOpen(true);
  };

  return (
    <div className="flex h-screen w-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Left Sidebar */}
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={(id) => {
          setActiveSessionId(id);
          setSidebarOpen(false);
        }}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
        modelInfo={modelInfo}
        onSwitchModel={handleSwitchModel}
        onSelectPreset={(prompt) => {
          handleSendMessage(prompt);
          setSidebarOpen(false);
        }}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Chat Interface */}
      <ChatArea
        session={activeSession}
        messages={messages}
        isLoading={isLoading}
        streamingToken={streamingToken}
        onSendMessage={handleSendMessage}
        onOpenArtifact={handleOpenArtifact}
        activeArtifact={activeArtifact}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
      />

      {/* Right Artifact Viewer */}
      {isArtifactViewerOpen && activeArtifact && (
        <ArtifactViewer
          artifact={activeArtifact}
          onClose={() => setIsArtifactViewerOpen(false)}
        />
      )}
    </div>
  );
}
