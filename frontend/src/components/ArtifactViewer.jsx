import React from 'react';
import { X, Layers } from 'lucide-react';

export default function ArtifactViewer({ artifact, onClose }) {
  if (!artifact) return null;

  return (
    <div className="artifact-panel">
      {/* Header */}
      <div className="artifact-panel__header">
        <Layers size={15} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
        <span className="artifact-panel__title">{artifact.title}</span>
        <span className="artifact-panel__type">{(artifact.type || 'html').toUpperCase()}</span>
        <button className="icon-btn" onClick={onClose} title="Close artifact" aria-label="Close artifact">
          <X size={16} />
        </button>
      </div>

      {/* Sandboxed iframe */}
      <iframe
        title={artifact.title}
        srcDoc={artifact.content}
        sandbox="allow-forms"
        referrerPolicy="no-referrer"
        className="artifact-panel__iframe"
      />
    </div>
  );
}
