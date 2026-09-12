import React, { useState } from 'react';
import { Eye, Code, Copy, Check, Download, X, Maximize2, Minimize2, ShieldCheck } from 'lucide-react';

export default function ArtifactViewer({ artifact, onClose }) {
  const [activeTab, setActiveTab] = useState('preview');
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  if (!artifact) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(artifact.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([artifact.content], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${artifact.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.html`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div
      className={`fixed lg:static inset-y-0 right-0 z-40 flex flex-col bg-slate-900 border-l border-slate-800 transition-all duration-300 shadow-2xl ${
        isExpanded ? 'w-full lg:w-[85vw]' : 'w-full lg:w-[480px] xl:w-[560px]'
      }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
        <div className="flex items-center gap-2 overflow-hidden">
          <span className="p-1 rounded bg-indigo-500/20 text-indigo-400">
            <Eye className="w-4 h-4" />
          </span>
          <div className="truncate">
            <h2 className="text-sm font-bold text-slate-100 truncate">{artifact.title}</h2>
            <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
              <span className="uppercase text-[10px] font-semibold tracking-wider text-indigo-400 bg-indigo-950/50 px-1.5 py-0.2 rounded border border-indigo-800/40">
                {artifact.type || 'HTML'} Artifact
              </span>
              <span>•</span>
              <span className="flex items-center gap-1 text-emerald-400 text-[10px]">
                <ShieldCheck className="w-3 h-3" /> Sandboxed
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          <button
            onClick={handleCopy}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg text-xs flex items-center gap-1 transition-colors"
            title="Copy Code"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          </button>
          <button
            onClick={handleDownload}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg text-xs flex items-center gap-1 transition-colors"
            title="Download HTML"
          >
            <Download className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg text-xs transition-colors hidden lg:block"
            title={isExpanded ? "Collapse" : "Expand"}
          >
            {isExpanded ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
          </button>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-slate-800 rounded-lg text-xs transition-colors"
            title="Close Viewer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center border-b border-slate-800 bg-slate-900/90 px-4">
        <button
          onClick={() => setActiveTab('preview')}
          className={`flex items-center gap-1.5 py-2.5 px-3 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'preview'
              ? 'border-indigo-500 text-indigo-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Eye className="w-3.5 h-3.5" />
          Preview
        </button>
        <button
          onClick={() => setActiveTab('code')}
          className={`flex items-center gap-1.5 py-2.5 px-3 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'code'
              ? 'border-indigo-500 text-indigo-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Code className="w-3.5 h-3.5" />
          Source Code
        </button>
      </div>

      {/* Content Body */}
      <div className="flex-1 overflow-hidden bg-slate-950 relative">
        {activeTab === 'preview' ? (
          <iframe
            title={artifact.title}
            srcDoc={artifact.content}
            sandbox="allow-scripts"
            className="w-full h-full border-0 bg-slate-950"
          />
        ) : (
          <div className="w-full h-full overflow-auto p-4 font-mono text-xs text-slate-300 bg-slate-950 leading-relaxed selection:bg-indigo-500/30">
            <pre className="whitespace-pre-wrap">{artifact.content}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
