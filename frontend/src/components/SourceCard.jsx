import React, { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink, BookOpen, Clock } from 'lucide-react';

export default function SourceCard({ sources }) {
  const [expanded, setExpanded] = useState(false);
  if (!sources || sources.length === 0) return null;

  return (
    <div style={{ marginTop: 14 }}>
      <button className="sources-toggle" onClick={() => setExpanded(!expanded)}>
        <BookOpen size={13} />
        <span>{sources.length} source{sources.length > 1 ? 's' : ''} from Lenny's Podcast</span>
        {expanded ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
      </button>

      {expanded && (
        <div className="sources-list">
          {sources.map((src, idx) => (
            <div key={idx} className="source-card">
              <div className="source-card__meta">
                <span className="source-card__guest">{src.guest}</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span className="source-card__ts">
                    <Clock size={11} />
                    {src.timestamp}
                  </span>
                  {src.youtube_url && (
                    <a
                      href={src.youtube_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: 'var(--accent)', display: 'flex' }}
                      title={`Watch on YouTube at ${src.timestamp}`}
                    >
                      <ExternalLink size={12} />
                    </a>
                  )}
                </div>
              </div>
              <div className="source-card__title">{src.title}</div>
              <blockquote className="source-card__quote">{src.content}</blockquote>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
