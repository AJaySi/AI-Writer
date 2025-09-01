import React, { useEffect } from 'react';
import { formatDraftContent, diffMarkup } from '../utils/contentFormatters';

interface ContentEditorProps {
  isPreviewing: boolean;
  pendingEdit: { src: string; target: string } | null;
  livePreviewHtml: string;
  draft: string;
  showPreview: boolean;
  isGenerating: boolean;
  loadingMessage: string;
  onConfirmChanges: () => void;
  onDiscardChanges: () => void;
  onDraftChange: (value: string) => void;
  onPreviewToggle: () => void;
}

export const ContentEditor: React.FC<ContentEditorProps> = ({
  isPreviewing,
  pendingEdit,
  livePreviewHtml,
  draft,
  showPreview,
  isGenerating,
  loadingMessage,
  onConfirmChanges,
  onDiscardChanges,
  onDraftChange,
  onPreviewToggle
}) => {
  // Auto-show preview when content is generated
  useEffect(() => {
    if (draft && !showPreview) {
      onPreviewToggle();
    }
  }, [draft, showPreview, onPreviewToggle]);

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* Predictive Diff Preview - Show when there are pending changes */}
      {isPreviewing && pendingEdit && (
        <div style={{
          margin: '24px',
          border: '1px solid #e0e0e0',
          borderRadius: 8,
          background: '#fff',
          boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
        }}>
          <div style={{
            padding: '12px 16px',
            borderBottom: '1px solid #eee',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <strong style={{ color: '#0a66c2' }}>Preview Changes</strong>
            <div style={{ display: 'flex', gap: 8 }}>
              <button
                onClick={onConfirmChanges}
                style={{
                  padding: '6px 12px',
                  background: '#0a66c2',
                  color: '#fff',
                  border: '1px solid #0a66c2',
                  borderRadius: 6,
                  cursor: 'pointer',
                  fontSize: 14,
                  fontWeight: 600
                }}
              >
                Confirm Changes
              </button>
              <button
                onClick={onDiscardChanges}
                style={{
                  padding: '6px 12px',
                  background: '#fff',
                  color: '#444',
                  border: '1px solid #ddd',
                  borderRadius: 6,
                  cursor: 'pointer',
                  fontSize: 14,
                  fontWeight: 500
                }}
              >
                Discard
              </button>
            </div>
          </div>
          <div style={{ padding: 16 }}>
            <div
              style={{ fontFamily: 'inherit', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}
              dangerouslySetInnerHTML={{ __html: livePreviewHtml || diffMarkup(pendingEdit.src, pendingEdit.target) }}
            />
            <style>{`
              .liw-add { background: rgba(46, 204, 113, 0.18); font-style: normal; }
              .liw-del { color: #c0392b; text-decoration: line-through; opacity: 0.8; }
              .liw-more { color: #999; }
            `}</style>
          </div>
        </div>
      )}

      {/* Full Width Content Preview */}
      <div style={{ flex: 1, padding: '24px' }}>
        {/* Content Preview */}
        {showPreview && (
          <div style={{
            border: '1px solid #e1f5fe',
            borderRadius: '8px',
            background: '#f8fdff',
            overflow: 'hidden',
            height: '100%'
          }}>
            <div style={{
              padding: '12px 16px',
              background: '#e1f5fe',
              borderBottom: '1px solid #b3e5fc',
              fontSize: '12px',
              fontWeight: '600',
              color: '#0277bd',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <span>LinkedIn Content Preview</span>
              <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
                <span style={{ fontSize: '10px', opacity: 0.8 }}>
                  {draft.split(/\s+/).length} words • {Math.ceil(draft.split(/\s+/).length / 200)} min read
                </span>
                <button
                  onClick={onPreviewToggle}
                  style={{
                    padding: '6px 12px',
                    background: showPreview ? '#0a66c2' : '#f8f9fa',
                    color: showPreview ? 'white' : '#666',
                    border: '1px solid #dee2e6',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '12px',
                    fontWeight: 500,
                    transition: 'all 0.2s ease'
                  }}
                >
                  {showPreview ? 'Hide Preview' : 'Show Preview'}
                </button>
              </div>
            </div>
            <div 
              style={{ 
                padding: '20px',
                height: 'calc(100% - 60px)',
                overflowY: 'auto',
                lineHeight: '1.6',
                position: 'relative'
              }}
            >
              {/* Loading State */}
              {isGenerating && (
                <div style={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  textAlign: 'center',
                  zIndex: 10
                }}>
                  <div style={{
                    width: '40px',
                    height: '40px',
                    border: '3px solid #e1f5fe',
                    borderTop: '3px solid #0a66c2',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite',
                    margin: '0 auto 16px auto'
                  }} />
                  <div style={{ 
                    color: '#0277bd', 
                    fontSize: '16px', 
                    fontWeight: '500',
                    marginBottom: '8px'
                  }}>
                    {loadingMessage || 'Generating LinkedIn content...'}
                  </div>
                  <div style={{ 
                    color: '#666', 
                    fontSize: '14px',
                    maxWidth: '300px',
                    lineHeight: '1.4'
                  }}>
                    Crafting professional content tailored to your industry and audience...
                  </div>
                  <style>{`
                    @keyframes spin {
                      0% { transform: rotate(0deg); }
                      100% { transform: rotate(360deg); }
                    }
                  `}</style>
                </div>
              )}
              
              {/* Content Display */}
              <div style={{
                opacity: isGenerating ? 0.3 : 1,
                transition: 'opacity 0.3s ease'
              }}>
                {draft ? (
                  <div dangerouslySetInnerHTML={{ __html: formatDraftContent(draft) }} />
                ) : (
                  <p style={{
                    color: '#666', 
                    fontStyle: 'italic', 
                    textAlign: 'center', 
                    marginTop: '40px'
                  }}>
                    Content will appear here when generated. Use the AI assistant to create your LinkedIn content.
                  </p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
