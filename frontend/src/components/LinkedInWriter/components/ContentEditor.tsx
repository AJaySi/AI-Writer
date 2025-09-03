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
  // Grounding data props
  researchSources?: any[];
  citations?: any[];
  qualityMetrics?: any;
  groundingEnabled?: boolean;
  searchQueries?: string[];
  onConfirmChanges: () => void;
  onDiscardChanges: () => void;
  onDraftChange: (value: string) => void;
  onPreviewToggle: () => void;
}

// Extend HTMLDivElement interface for custom tooltip properties
interface ExtendedDivElement extends HTMLDivElement {
  _researchTooltip?: HTMLDivElement | null;
  _citationsTooltip?: HTMLDivElement | null;
  _searchQueriesTooltip?: HTMLDivElement | null;
}

export { ContentEditor };

const ContentEditor: React.FC<ContentEditorProps> = ({
  isPreviewing,
  pendingEdit,
  livePreviewHtml,
  draft,
  showPreview,
  isGenerating,
  loadingMessage,
  // Grounding data props
  researchSources,
  citations,
  qualityMetrics,
  groundingEnabled,
  searchQueries,
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

  // Debug logging for quality metrics and research sources
  useEffect(() => {
    console.log('🔍 [ContentEditor] Props received:', {
      researchSources: researchSources,
      citations: citations,
      qualityMetrics: qualityMetrics,
      groundingEnabled: groundingEnabled,
      draftLength: draft?.length || 0
    });
    
    if (qualityMetrics) {
      console.log('🔍 [ContentEditor] Quality metrics details:', {
        overall_score: qualityMetrics.overall_score,
        factual_accuracy: qualityMetrics.factual_accuracy,
        source_verification: qualityMetrics.source_verification,
        professional_tone: qualityMetrics.professional_tone,
        industry_relevance: qualityMetrics.industry_relevance,
        citation_coverage: qualityMetrics.citation_coverage
      });
    }
    
    if (researchSources && researchSources.length > 0) {
      console.log('🔍 [ContentEditor] Research sources details:', {
        count: researchSources.length,
        sample: researchSources.slice(0, 3).map(s => ({
          title: s.title,
          url: s.url,
          source_type: s.source_type,
          credibility_score: s.credibility_score,
          relevance_score: s.relevance_score,
          domain_authority: s.domain_authority
        }))
      });
    }
  }, [researchSources, citations, qualityMetrics, groundingEnabled, draft]);

  // Citation hover functionality
  useEffect(() => {
    if (!researchSources || researchSources.length === 0) return;

    console.log('🔍 [Citation Hover] useEffect triggered with', researchSources.length, 'sources');

    // Keep track of currently open tooltip
    let currentOpenTooltip: HTMLDivElement | null = null;

    // Extend Element interface for our custom property
    interface ExtendedElement extends Element {
      _liwTip?: HTMLDivElement | null;
    }

    const initCitationHover = () => {
      try {
        console.log('🔍 [Citation Hover] Script starting...');
        console.log('🔍 [Citation Hover] Research sources count:', researchSources.length);
        
        // Test if script is running
        document.body.style.setProperty('--citation-hover-active', 'true');
        console.log('🔍 [Citation Hover] Script is running, CSS variable set');
        
        // Wait for content to be rendered
        const waitForCitations = () => {
          const citations = document.querySelectorAll('.liw-cite');
          console.log('🔍 [Citation Hover] Looking for citations, found:', citations.length);
          
          if (citations.length === 0) {
            // If no citations found, wait a bit and try again
            console.log('🔍 [Citation Hover] No citations found, waiting...');
            setTimeout(waitForCitations, 200);
            return;
          }
          
          console.log('🔍 [Citation Hover] Found', citations.length, 'citation elements');
          citations.forEach((cite, idx) => {
            console.log(`🔍 [Citation Hover] Citation ${idx}: ${cite.outerHTML}`);
            console.log(`🔍 [Citation Hover] Citation classes: ${cite.className}`);
            console.log(`🔍 [Citation Hover] Citation data-source-index: ${cite.getAttribute('data-source-index')}`);
          });
          setupCitationHover();
        };
        
        const setupCitationHover = () => {
          console.log('🔍 [Citation Hover] Initializing hover functionality...');
          const data = researchSources;
          console.log('🔍 [Citation Hover] Research data loaded:', data.length, 'sources');

          const openOverlay = (idx: string, src: any) => {
            console.log('🔍 [Citation Hover] Opening overlay for source', idx, src);
            const existing = document.getElementById('liw-cite-overlay');
            if (existing) existing.remove();

            const overlay = document.createElement('div');
            overlay.id = 'liw-cite-overlay';
            overlay.style.position = 'fixed';
            overlay.style.inset = '0';
            overlay.style.background = 'rgba(0,0,0,0.35)';
            overlay.style.backdropFilter = 'blur(2px)';
            overlay.style.zIndex = '100000';
            overlay.style.display = 'flex';
            overlay.style.alignItems = 'center';
            overlay.style.justifyContent = 'center';

            const modal = document.createElement('div');
            modal.style.width = 'min(720px, 92vw)';
            modal.style.maxHeight = '80vh';
            modal.style.overflow = 'auto';
            modal.style.borderRadius = '14px';
            modal.style.background = 'linear-gradient(180deg, #ffffff, #f8fdff)';
            modal.style.border = '1px solid #cfe9f7';
            modal.style.boxShadow = '0 24px 80px rgba(10,102,194,0.25)';
            modal.style.padding = '18px 20px';
            
            const title = (src.title || 'Untitled').replace(/</g, '&lt;');
            const url = (src.url || '').replace(/</g, '&lt;');
            const sourceType = src.source_type ? String(src.source_type).replace('_', ' ') : '';
            
            modal.innerHTML = 
              '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">' +
                '<div style="font-size:16px;font-weight:800;color:#0a66c2">Source ' + idx + '</div>' +
                '<button id="liw-cite-close" style="border:none;background:#eff6ff;color:#0a66c2;border-radius:8px;padding:8px 12px;cursor:pointer;font-weight:700">✕ Close</button>' +
              '</div>' +
              '<div style="font-size:18px;font-weight:700;color:#1f2937;margin-bottom:8px">' + title + '</div>' +
              '<a href="' + (src.url || '#') + '" target="_blank" style="display:inline-block;color:#0a66c2;text-decoration:none;margin-bottom:12px;font-size:14px;font-weight:600;">View Source →</a>' +
              (src.content ? '<div style="margin-bottom:16px;color:#374151;font-size:14px;line-height:1.6;background:#f9fafb;padding:16px;border-radius:8px;border-left:4px solid #0a66c2;">' + src.content + '</div>' : '') +
              '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">' +
                (typeof src.relevance_score === 'number' ? '<span style="background:#eef6ff;border:1px solid #d9ecff;border-radius:999px;padding:8px 12px;font-size:13px;color:#055a8c;font-weight:600">Relevance: ' + Math.round(src.relevance_score * 100) + '%</span>' : '') +
                (typeof src.credibility_score === 'number' ? '<span style="background:#eef6ff;border:1px solid #d9ecff;border-radius:999px;padding:8px 12px;font-size:13px;color:#055a8c;font-weight:600">Credibility: ' + Math.round(src.credibility_score * 100) + '%</span>' : '') +
                (typeof src.domain_authority === 'number' ? '<span style="background:#eef6ff;border:1px solid #d9ecff;border-radius:999px;padding:8px 12px;font-size:13px;color:#055a8c;font-weight:600">Authority: ' + Math.round(src.domain_authority * 100) + '%</span>' : '') +
              '</div>' +
              '<div style="display:flex;gap:16px;color:#6b7280;font-size:13px;padding-top:12px;border-top:1px solid #e5e7eb">' +
                (src.source_type ? '<div>Type: <span style="color:#374151;font-weight:600">' + src.source_type.replace('_', ' ') + '</span></div>' : '') +
                (src.publication_date ? '<div>Published: <span style="color:#374151;font-weight:600">' + src.publication_date + '</span></div>' : '') +
              '</div>' +
              (src.raw_result ? '<div style="color:#6b7280;font-size:12px;margin-top:12px;padding:8px;background:#f3f4f6;border-radius:6px;border-top:1px solid #e5e7eb;">Raw Data: ' + JSON.stringify(src.raw_result).substring(0, 150) + (JSON.stringify(src.raw_result).length > 150 ? '...' : '') + '</div>' : '');

            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            const close = () => { 
              try { overlay.remove(); } catch(_){} 
            };
            overlay.addEventListener('click', (e) => { 
              if(e.target === overlay) close(); 
            });
            document.getElementById('liw-cite-close')?.addEventListener('click', close);
            document.addEventListener('keydown', function esc(ev: KeyboardEvent) { 
              if(ev.key === 'Escape') { 
                close(); 
                document.removeEventListener('keydown', esc);
              } 
            });
          };

          // Add event listeners directly to each citation element
          const citations = document.querySelectorAll('.liw-cite');
          
          citations.forEach((cite) => {
            console.log('🔍 [Citation Hover] Adding event listeners to citation:', cite.outerHTML);
            
            cite.addEventListener('mouseenter', () => {
              console.log('🔍 [Citation Hover] Mouse enter on citation:', cite.outerHTML);
              
              // Close any existing tooltip first
              if (currentOpenTooltip) {
                try { currentOpenTooltip.remove(); } catch(_) {}
                currentOpenTooltip = null;
              }
              
              const idx = cite.getAttribute('data-source-index');
              console.log('🔍 [Citation Hover] Citation index:', idx);
              
              if (!idx) return;
              const i = parseInt(idx, 10) - 1;
              const src = data[i];
              if (!src) {
                console.log('🔍 [Citation Hover] No source found for index:', idx);
                return;
              }

              console.log('🔍 [Citation Hover] Creating tooltip for source:', src);

              let tip = document.createElement('div');
              tip.className = 'liw-cite-tip';
              tip.style.position = 'fixed';
              tip.style.zIndex = '99999';
              tip.style.maxWidth = '420px';
              tip.style.background = 'linear-gradient(180deg, #ffffff, #f8fdff)';
              tip.style.border = '1px solid #cfe9f7';
              tip.style.borderRadius = '10px';
              tip.style.boxShadow = '0 12px 40px rgba(10,102,194,0.18)';
              tip.style.padding = '12px 14px';
              tip.style.fontSize = '12px';
              tip.style.color = '#1f2937';
              tip.style.backdropFilter = 'blur(5px)';
              
              const title = (src.title || 'Untitled').replace(/</g, '&lt;');
              const url = (src.url || '').replace(/</g, '&lt;');
              const sourceType = src.source_type ? String(src.source_type).replace('_', ' ') : '';
              
              tip.innerHTML = 
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">' +
                  '<div style="font-weight:700;color:#0a66c2">Source ' + idx + '</div>' +
                  '<button class="liw-pin" title="Pin" style="border:none;background:#eef6ff;border-radius:8px;padding:4px 8px;cursor:pointer;color:#0a66c2;font-weight:800">📌</button>' +
                '</div>' +
                '<div style="font-weight:600;margin-bottom:6px;color:#1f2937">' + title + '</div>' +
                '<a href="' + (src.url || '#') + '" target="_blank" style="color:#0a66c2;text-decoration:none;margin-bottom:8px;display:block;font-weight:600;">View Source →</a>' +
                (src.content ? '<div style="margin-bottom:8px;color:#374151;font-size:11px;line-height:1.4;background:#f9fafb;padding:8px;border-radius:6px;border-left:3px solid #0a66c2;">' + src.content + '</div>' : '') +
                '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px">' +
                  (typeof src.relevance_score === 'number' ? '<span style="background:#eef6ff;border:1px solid #d9ecff;border-radius:999px;padding:4px 8px;font-size:11px;color:#055a8c;font-weight:600">Relevance: ' + Math.round(src.relevance_score * 100) + '%</span>' : '') +
                  (typeof src.credibility_score === 'number' ? '<span style="background:#eef6ff;border:1px solid #d9ecff;border-radius:999px;padding:4px 8px;font-size:11px;color:#055a8c;font-weight:600">Credibility: ' + Math.round(src.credibility_score * 100) + '%</span>' : '') +
                  (typeof src.domain_authority === 'number' ? '<span style="background:#eef6ff;border:1px solid #d9ecff;border-radius:999px;padding:4px 8px;font-size:11px;color:#055a8c;font-weight:600">Authority: ' + Math.round(src.domain_authority * 100) + '%</span>' : '') +
                '</div>' +
                (src.source_type ? '<div style="color:#6b7280;font-size:11px;margin-bottom:4px">Type: <span style="color:#374151;font-weight:600">' + src.source_type.replace('_', ' ') + '</span></div>' : '') +
                (src.publication_date ? '<div style="color:#6b7280;font-size:11px">Published: <span style="color:#374151;font-weight:600">' + src.publication_date + '</span></div>' : '') +
                (src.raw_result ? '<div style="color:#6b7280;font-size:11px;margin-top:4px;padding:4px;background:#f3f4f6;border-radius:4px;">Raw Data: ' + JSON.stringify(src.raw_result).substring(0, 100) + (JSON.stringify(src.raw_result).length > 100 ? '...' : '') + '</div>' : '');
                
              document.body.appendChild(tip);
              const rect = cite.getBoundingClientRect();
              tip.style.left = Math.min(rect.left, window.innerWidth - 460) + 'px';
              tip.style.top = (rect.bottom + 8) + 'px';

              tip.querySelector('.liw-pin')?.addEventListener('click', (ev) => {
                ev.stopPropagation();
                openOverlay(idx, src);
                try { tip.remove(); } catch(_) { 
                  // Remove the custom property reference
                  const extendedTip = tip as any;
                  extendedTip._liwTip = undefined;
                }
                currentOpenTooltip = null;
              });

              (cite as ExtendedElement)._liwTip = tip;
              currentOpenTooltip = tip;
              console.log('🔍 [Citation Hover] Tooltip created and positioned');
            });

            cite.addEventListener('mouseleave', () => {
              console.log('🔍 [Citation Hover] Mouse leave on citation:', cite.outerHTML);
              const extendedCite = cite as ExtendedElement;
              if (extendedCite._liwTip) { 
                try { extendedCite._liwTip.remove(); } catch(_) {} 
                extendedCite._liwTip = null; 
                currentOpenTooltip = null;
              }
            });
          });
          
          console.log('✅ [Citation Hover] Hover functionality initialized for', citations.length, 'citations');
        };
        
        // Start waiting for citations with a longer delay to ensure content is rendered
        setTimeout(waitForCitations, 500);
        
      } catch(e: any) { 
        console.warn('liw cite tooltip init failed', e); 
        console.error('Error details:', e);
        // Show error in UI
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = 'position:fixed;top:10px;right:10px;background:#ffebee;border:1px solid #f44336;border-radius:4px;padding:10px;z-index:100000;color:#c62828;';
        errorDiv.innerHTML = 'Citation hover failed: ' + e.message;
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
      }
    };

    // Initialize citation hover after a short delay to ensure content is rendered
    const timer = setTimeout(initCitationHover, 100);
    
    // Cleanup function
    return () => {
      clearTimeout(timer);
      // Remove any existing tooltips
      const tooltips = document.querySelectorAll('.liw-cite-tip');
      tooltips.forEach(tip => tip.remove());
      // Remove overlay if exists
      const overlay = document.getElementById('liw-cite-overlay');
      if (overlay) overlay.remove();
      // Reset current tooltip reference
      currentOpenTooltip = null;
    };
  }, [researchSources]); // Dependency on researchSources

  const formatPercent = (v?: number) => typeof v === 'number' ? `${Math.round(v * 100)}%` : '—';
  const getChipColor = (v?: number) => {
    if (typeof v !== 'number') return '#6b7280';
    if (v >= 0.8) return '#10b981';
    if (v >= 0.6) return '#f59e0b';
    return '#ef4444';
  };
  const chips = qualityMetrics ? [
    { label: 'Overall', value: qualityMetrics.overall_score },
    { label: 'Accuracy', value: qualityMetrics.factual_accuracy },
    { label: 'Verification', value: qualityMetrics.source_verification },
    { label: 'Coverage', value: qualityMetrics.citation_coverage }
  ] : [];
  
  console.log('🔍 [ContentEditor] Chips array created:', {
    qualityMetrics: qualityMetrics,
    chips: chips,
    chipsLength: chips.length
  });

  // Helper to build descriptive chip tooltip text
  const chipDescriptions: Record<string, string> = {
    Overall: 'Overall blends accuracy, verification and coverage into a single reliability score for this draft.',
    Accuracy: 'Factual Accuracy estimates how likely statements are to be factually correct based on grounding signals.',
    Verification: 'Source Verification reflects how well claims are linked to credible sources and whether citations match claims.',
    Coverage: 'Citation Coverage indicates how much of the content is supported with citations. Higher is better.'
  };

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
            height: 'auto'
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
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <span>LinkedIn Content Preview</span>
                
                {/* Research Sources & Citations Count Chips */}
                {researchSources && researchSources.length > 0 && (
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    {/* Research Sources Count Chip */}
                    <div
                      style={{
                        background: 'rgba(255, 255, 255, 0.9)',
                        border: '1px solid rgba(2, 119, 189, 0.3)',
                        borderRadius: '999px',
                        padding: '4px 10px',
                        fontSize: '11px',
                        fontWeight: '600',
                        color: '#0277bd',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        position: 'relative',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                      title={`${researchSources.length} research sources available. Hover to see details.`}
                      onMouseEnter={(e) => {
                        // Create and show research sources tooltip
                        const tooltip = document.createElement('div');
                        tooltip.style.cssText = `
                          position: fixed;
                          z-index: 100000;
                          background: white;
                          border: 1px solid #cfe9f7;
                          border-radius: 8px;
                          box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                          padding: 16px;
                          max-width: 500px;
                          max-height: 400px;
                          overflow-y: auto;
                          font-size: 12px;
                        `;
                        
                        tooltip.innerHTML = `
                          <div style="margin-bottom: 12px; font-weight: 600; color: #0a66c2; font-size: 14px;">
                            Research Sources (${researchSources.length})
                          </div>
                          ${researchSources.map((source, idx) => `
                            <div style="margin-bottom: 12px; padding: 8px; background: #f8f9fa; border-radius: 6px; border-left: 3px solid #0a66c2;">
                              <div style="font-weight: 600; margin-bottom: 4px;">${source.title || 'Untitled'}</div>
                              <div style="color: #666; margin-bottom: 4px;">${source.content || 'No description'}</div>
                              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                                ${source.relevance_score ? `<span style="background: #eef6ff; padding: 2px 6px; border-radius: 4px; font-size: 10px;">Relevance: ${Math.round(source.relevance_score * 100)}%</span>` : ''}
                                ${source.credibility_score ? `<span style="background: #eef6ff; padding: 2px 6px; border-radius: 4px; font-size: 10px;">Credibility: ${Math.round(source.credibility_score * 100)}%</span>` : ''}
                                ${source.domain_authority ? `<span style="background: #eef6ff; padding: 2px 6px; border-radius: 4px; font-size: 10px;">Authority: ${Math.round(source.domain_authority * 100)}%</span>` : ''}
                              </div>
                            </div>
                          `).join('')}
                        `;
                        
                        document.body.appendChild(tooltip);
                        const rect = e.currentTarget.getBoundingClientRect();
                        tooltip.style.left = Math.min(rect.left, window.innerWidth - 520) + 'px';
                        tooltip.style.top = (rect.bottom + 8) + 'px';
                        
                        (e.currentTarget as ExtendedDivElement)._researchTooltip = tooltip;
                      }}
                      onMouseLeave={(e) => {
                        const target = e.currentTarget as ExtendedDivElement;
                        if (target._researchTooltip) {
                          target._researchTooltip.remove();
                          target._researchTooltip = null;
                        }
                      }}
                    >
                      <div style={{
                        width: '6px',
                        height: '6px',
                        borderRadius: '50%',
                        background: '#10b981',
                        flexShrink: 0
                      }} />
                      Sources: {researchSources.length}
                    </div>
                    
                    {/* Citations Count Chip */}
                    {citations && citations.length > 0 && (
                      <div
                        style={{
                          background: 'rgba(255, 255, 255, 0.9)',
                          border: '1px solid rgba(2, 119, 189, 0.3)',
                          borderRadius: '999px',
                          padding: '4px 10px',
                          fontSize: '11px',
                          fontWeight: '600',
                          color: '#0277bd',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                          position: 'relative',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px'
                        }}
                        title={`${citations.length} citations in content. Hover to see details.`}
                        onMouseEnter={(e) => {
                          // Create and show citations tooltip
                          const tooltip = document.createElement('div');
                          tooltip.style.cssText = `
                            position: fixed;
                            z-index: 100000;
                            background: white;
                            border: 1px solid #cfe9f7;
                            border-radius: 8px;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                            padding: 16px;
                            max-width: 500px;
                            max-height: 400px;
                            overflow-y: auto;
                            font-size: 12px;
                          `;
                          
                          tooltip.innerHTML = `
                            <div style="margin-bottom: 12px; font-weight: 600; color: #0a66c2; font-size: 14px;">
                              Citations (${citations.length})
                            </div>
                            ${citations.map((citation, idx) => `
                              <div style="margin-bottom: 8px; padding: 6px; background: #f8f9fa; border-radius: 4px;">
                                <div style="font-weight: 600; color: #0a66c2;">Citation ${idx + 1}</div>
                                <div style="color: #666; font-size: 11px;">Type: ${citation.type || 'inline'}</div>
                                ${citation.reference ? `<div style="color: #666; font-size: 11px;">Reference: ${citation.reference}</div>` : ''}
                              </div>
                            `).join('')}
                          `;
                          
                          document.body.appendChild(tooltip);
                          const rect = e.currentTarget.getBoundingClientRect();
                          tooltip.style.left = Math.min(rect.left, window.innerWidth - 520) + 'px';
                          tooltip.style.top = (rect.bottom + 8) + 'px';
                          
                          (e.currentTarget as ExtendedDivElement)._citationsTooltip = tooltip;
                        }}
                        onMouseLeave={(e) => {
                          const target = e.currentTarget as ExtendedDivElement;
                          if (target._citationsTooltip) {
                            target._citationsTooltip.remove();
                            target._citationsTooltip = null;
                          }
                        }}
                      >
                        <div style={{
                          width: '6px',
                          height: '6px',
                          borderRadius: '50%',
                          background: '#f59e0b',
                          flexShrink: 0
                        }} />
                        Citations: {citations.length}
                      </div>
                    )}
                    
                    {/* Search Queries Count Chip */}
                    {searchQueries && searchQueries.length > 0 && (
                      <div
                        style={{
                          background: 'rgba(255, 255, 255, 0.9)',
                          border: '1px solid rgba(2, 119, 189, 0.3)',
                          borderRadius: '999px',
                          padding: '4px 10px',
                          fontSize: '11px',
                          fontWeight: '600',
                          color: '#0277bd',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                          position: 'relative',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px'
                        }}
                        title={`${searchQueries.length} search queries used for research. Hover to see details.`}
                        onMouseEnter={(e) => {
                          // Create and show search queries tooltip
                          const tooltip = document.createElement('div');
                          tooltip.style.cssText = `
                            position: fixed;
                            z-index: 100000;
                            background: white;
                            border: 1px solid #cfe9f7;
                            border-radius: 8px;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                            padding: 16px;
                            max-width: 500px;
                            max-height: 400px;
                            overflow-y: auto;
                            font-size: 12px;
                          `;
                          
                          tooltip.innerHTML = `
                            <div style="margin-bottom: 12px; font-weight: 600; color: #0a66c2; font-size: 14px;">
                              Search Queries Used (${searchQueries.length})
                            </div>
                            ${searchQueries.map((query, idx) => `
                              <div style="margin-bottom: 8px; padding: 8px; background: #f8f9fa; border-radius: 6px; border-left: 3px solid #8b5cf6;">
                                <div style="font-weight: 600; color: #7c3aed; margin-bottom: 4px;">Query ${idx + 1}</div>
                                <div style="color: #374151; font-size: 12px; line-height: 1.4;">${query}</div>
                              </div>
                            `).join('')}
                          `;
                          
                          document.body.appendChild(tooltip);
                          const rect = e.currentTarget.getBoundingClientRect();
                          tooltip.style.left = Math.min(rect.left, window.innerWidth - 520) + 'px';
                          tooltip.style.top = (rect.bottom + 8) + 'px';
                          
                          (e.currentTarget as ExtendedDivElement)._searchQueriesTooltip = tooltip;
                        }}
                        onMouseLeave={(e) => {
                          const target = e.currentTarget as ExtendedDivElement;
                          if (target._searchQueriesTooltip) {
                            target._searchQueriesTooltip.remove();
                            target._searchQueriesTooltip = null;
                          }
                        }}
                      >
                        <div style={{
                          width: '6px',
                          height: '6px',
                          borderRadius: '50%',
                          background: '#8b5cf6',
                          flexShrink: 0
                        }} />
                        Queries: {searchQueries.length}
                      </div>
                    )}
                  </div>
                )}
              </div>
              <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
                {/* Quality Chips */}
                {chips.length > 0 && (
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
                    {chips.map((c, idx) => (
                      <div key={idx}
                        title={`${c.label}: ${formatPercent(c.value)}. ${chipDescriptions[c.label] || ''}`}
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: 6,
                          padding: '6px 10px',
                          borderRadius: 999,
                          background: 'linear-gradient(135deg, rgba(255,255,255,0.9), rgba(225,245,254,0.9))',
                          boxShadow: '0 6px 14px rgba(2,119,189,0.12), inset 0 0 8px rgba(2,119,189,0.08)',
                          border: '1px solid rgba(2,119,189,0.25)',
                          transform: 'translateZ(0)',
                          willChange: 'transform, box-shadow',
                          position: 'relative',
                          overflow: 'hidden'
                        }}
                      >
                        <span style={{
                          width: 8, height: 8, borderRadius: 999,
                          background: getChipColor(c.value),
                          boxShadow: `0 0 10px ${getChipColor(c.value)}`
                        }} />
                        <span style={{ color: '#055a8c', fontWeight: 700 }}>{formatPercent(c.value)}</span>
                        <span style={{ color: '#0a66c2', fontWeight: 600, opacity: 0.9 }}>{c.label}</span>
                        <span style={{
                          position: 'absolute',
                          inset: 0,
                          background: 'linear-gradient(120deg, transparent, rgba(255,255,255,0.6), transparent)',
                          transform: 'translateX(-100%)',
                          animation: 'liw-shimmer 2.2s infinite'
                        }} />
                      </div>
                    ))}
                    <style>{`
                      @keyframes liw-shimmer { 0% { transform: translateX(-100%); } 60% { transform: translateX(100%); } 100% { transform: translateX(100%); } }
                    `}</style>
                  </div>
                )}
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
                maxHeight: '68vh',
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
                  <div dangerouslySetInnerHTML={{ __html: formatDraftContent(draft, citations, researchSources) }} />
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
                
                {/* Citation Styling */}
                <style>{`
                  .liw-cite {
                    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
                    border: 1px solid #64b5f6;
                    border-radius: 4px;
                    padding: 2px 6px;
                    margin: 0 2px;
                    font-size: 0.8em;
                    font-weight: 600;
                    color: #1976d2;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    box-shadow: 0 2px 4px rgba(25, 118, 210, 0.1);
                  }
                  .liw-cite:hover {
                    background: linear-gradient(135deg, #bbdefb, #90caf9);
                    border-color: #42a5f5;
                    box-shadow: 0 4px 8px rgba(25, 118, 210, 0.2);
                    transform: translateY(-1px);
                  }
                  .liw-cite:active {
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(25, 118, 210, 0.1);
                  }
                `}</style>
              </div>



            </div>
          </div>
        )}
      </div>
      {/* Citation Hover Handler - Now working automatically via useEffect */}
    </div>
  );
};
