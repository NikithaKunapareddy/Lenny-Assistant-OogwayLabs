const API_BASE = '/api';

export const api = {
  // Health
  async getHealth() {
    const res = await fetch('/health');
    return res.json();
  },

  // Models
  async getModels() {
    const res = await fetch(`${API_BASE}/models`);
    return res.json();
  },

  async switchModel(provider) {
    const res = await fetch(`${API_BASE}/models/switch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provider })
    });
    return res.json();
  },

  // Sessions
  async getSessions() {
    const res = await fetch(`${API_BASE}/sessions`);
    return res.json();
  },

  async createSession(title = 'New Strategy Chat', modelProvider = null) {
    const res = await fetch(`${API_BASE}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, model_provider: modelProvider })
    });
    return res.json();
  },

  async getSession(sessionId) {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}`);
    if (!res.ok) throw new Error('Session not found');
    return res.json();
  },

  async deleteSession(sessionId) {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}`, { method: 'DELETE' });
    return res.status === 204;
  },

  async renameSession(sessionId, title) {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    });
    if (!res.ok) throw new Error('Rename failed');
    return res.json();
  },

  async summarizeSession(sessionId, modelProvider = null) {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/summarize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model_provider: modelProvider })
    });
    if (!res.ok) throw new Error('Summarize failed');
    return res.json();
  },

  // Chat
  async sendChatMessage(sessionId, message, modelProvider = null) {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        message,
        model_provider: modelProvider
      })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.message || 'Chat request failed');
    }
    return res.json();
  },

  // Artifact
  async getArtifact(artifactId) {
    const res = await fetch(`${API_BASE}/artifacts/${artifactId}`);
    if (!res.ok) throw new Error('Artifact not found');
    return res.json();
  }
};
