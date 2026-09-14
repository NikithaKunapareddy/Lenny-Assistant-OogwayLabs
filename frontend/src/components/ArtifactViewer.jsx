import React, { useState, useEffect } from 'react';
import { X, Layers, Code, Eye, Copy, Check, Sun, Moon } from 'lucide-react';

const LIGHT_THEME_CSS = `
<style id="lenny-light-theme-override">
  html, body {
    background: #f8fafc !important;
    background-image: 
      radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.10) 0px, transparent 50%),
      radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.10) 0px, transparent 50%),
      radial-gradient(at 50% 100%, rgba(249, 115, 22, 0.08) 0px, transparent 50%) !important;
    color: #0f172a !important;
  }
  .container {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04) !important;
    color: #0f172a !important;
  }
  .header {
    border-bottom: 1px solid #e2e8f0 !important;
  }
  h1 {
    background: none !important;
    -webkit-background-clip: unset !important;
    -webkit-text-fill-color: #0f172a !important;
    color: #0f172a !important;
  }
  p.subtitle {
    color: #64748b !important;
  }
  .stack-tier, .card {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
  }
  .stack-tier:hover, .card:hover {
    background: #f1f5f9 !important;
    border-color: #cbd5e1 !important;
  }
  .tier-name, .card-title {
    color: #0f172a !important;
  }
  .tier-desc, .card-desc {
    color: #475569 !important;
  }
  .checklist {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
  }
  .checklist-title {
    color: #0f172a !important;
  }
  .item {
    color: #334155 !important;
  }
  .quote {
    background: #eff6ff !important;
    color: #1e40af !important;
    border-left-color: #3b82f6 !important;
  }
  .badge-blue { background: #dbeafe !important; color: #1d4ed8 !important; border-color: #bfdbfe !important; }
  .badge-purple { background: #f3e8ff !important; color: #7e22ce !important; border-color: #e9d5ff !important; }
  .badge-green { background: #dcfce7 !important; color: #15803d !important; border-color: #bbf7d0 !important; }
  .badge-orange { background: #ffedd5 !important; color: #c2410c !important; border-color: #fed7aa !important; }
</style>
`;

export default function ArtifactViewer({ artifact, appTheme = 'dark', onClose }) {
  const [viewMode, setViewMode] = useState('preview'); // 'preview' | 'code'
  const [overrideTheme, setOverrideTheme] = useState(null);
  const [copied, setCopied] = useState(false);

  const artifactTheme = overrideTheme || appTheme;

  // Handle ESC key to close
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!artifact) return null;

  const rawHtml = artifact.content || '';

  // Prepare iframe HTML with theme injection
  const iframeSrcDoc = artifactTheme === 'light'
    ? (rawHtml.includes('</head>')
        ? rawHtml.replace('</head>', `${LIGHT_THEME_CSS}</head>`)
        : `${LIGHT_THEME_CSS}${rawHtml}`)
    : rawHtml;

  const handleCopyCode = () => {
    navigator.clipboard.writeText(rawHtml).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="artifact-panel" data-artifact-theme={artifactTheme}>
      {/* Header */}
      <div className="artifact-panel__header">
        <div className="artifact-panel__header-left">
          <Layers size={16} className="artifact-icon" />
          <span className="artifact-panel__title" title={artifact.title}>
            {artifact.title}
          </span>
        </div>

        <div className="artifact-panel__actions">
          {/* Segmented View Mode Toggle: Preview / Code */}
          <div className="artifact-tabs" role="tablist">
            <button
              className={`artifact-tab ${viewMode === 'preview' ? 'artifact-tab--active' : ''}`}
              onClick={() => setViewMode('preview')}
              title="Interactive Preview"
              role="tab"
              aria-selected={viewMode === 'preview'}
            >
              <Eye size={13} />
              <span>Preview</span>
            </button>
            <button
              className={`artifact-tab ${viewMode === 'code' ? 'artifact-tab--active' : ''}`}
              onClick={() => setViewMode('code')}
              title="View HTML Source Code"
              role="tab"
              aria-selected={viewMode === 'code'}
            >
              <Code size={13} />
              <span>HTML</span>
            </button>
          </div>

          {/* Copy Code button */}
          <button
            className="icon-btn artifact-action-btn"
            onClick={handleCopyCode}
            title={copied ? "Copied!" : "Copy HTML code"}
            aria-label="Copy HTML code"
          >
            {copied ? <Check size={14} style={{ color: '#10b981' }} /> : <Copy size={14} />}
          </button>

          {/* Artifact Light/Dark Theme toggle */}
          <button
            className="icon-btn artifact-action-btn"
            onClick={() => setOverrideTheme(t => (t || appTheme) === 'dark' ? 'light' : 'dark')}
            title={`Preview in ${artifactTheme === 'dark' ? 'light' : 'dark'} mode`}
            aria-label="Toggle artifact theme"
          >
            {artifactTheme === 'dark' ? <Sun size={14} /> : <Moon size={14} />}
          </button>

          <div className="artifact-header-divider" />

          {/* Close Button (Cross Mark) */}
          <button
            className="icon-btn close-artifact-btn"
            onClick={onClose}
            title="Close artifact (Esc)"
            aria-label="Close artifact"
          >
            <X size={16} />
          </button>
        </div>
      </div>

      {/* Main Body: Preview or Code */}
      <div className="artifact-panel__body">
        {viewMode === 'preview' ? (
          <iframe
            key={artifactTheme}
            title={artifact.title}
            srcDoc={iframeSrcDoc}
            sandbox="allow-forms allow-same-origin"
            referrerPolicy="no-referrer"
            className="artifact-panel__iframe"
          />
        ) : (
          <div className="artifact-code-container">
            <div className="artifact-code-toolbar">
              <span className="code-lang-label">HTML / CSS SOURCE</span>
              <button className="code-copy-pill" onClick={handleCopyCode}>
                {copied ? <Check size={12} /> : <Copy size={12} />}
                <span>{copied ? 'Copied' : 'Copy Code'}</span>
              </button>
            </div>
            <pre className="artifact-code-pre">
              <code>{rawHtml}</code>
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
