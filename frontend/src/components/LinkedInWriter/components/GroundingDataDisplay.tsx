import React from 'react';
import { ResearchSource, Citation, ContentQualityMetrics } from '../../../services/linkedInWriterApi';

interface GroundingDataDisplayProps {
  researchSources: ResearchSource[];
  citations: Citation[];
  qualityMetrics?: ContentQualityMetrics;
  groundingEnabled: boolean;
}

export const GroundingDataDisplay: React.FC<GroundingDataDisplayProps> = ({
  researchSources,
  citations,
  qualityMetrics,
  groundingEnabled
}) => {
  
  if (!groundingEnabled || researchSources.length === 0) {
    return null;
  }

  const formatScore = (score: number) => `${(score * 100).toFixed(0)}%`;
  const getQualityColor = (score: number) => {
    if (score >= 0.8) return '#10b981'; // Green
    if (score >= 0.6) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  return (
    <div style={{
      margin: '24px 0',
      padding: '20px',
      border: '1px solid #e5e7eb',
      borderRadius: '12px',
      backgroundColor: '#fff',
      boxShadow: '0 4px 16px rgba(0,0,0,0.06)',
      position: 'relative',
      zIndex: 1,
      minHeight: '120px',
      fontSize: '16px'
    }}>
      {/* Header */}
 
      <div style={{
        display: 'flex',
        alignItems: 'center',
        marginBottom: '20px',
        paddingBottom: '12px',
        borderBottom: '2px solid #e5e7eb'
      }}>
        <div style={{
          width: '24px',
          height: '24px',
          borderRadius: '50%',
          backgroundColor: '#0a66c2',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginRight: '12px'
        }}>
          <span style={{ color: 'white', fontSize: '14px', fontWeight: 'bold' }}>✓</span>
        </div>
        <h3 style={{
          margin: 0,
          color: '#0a66c2',
          fontSize: '18px',
          fontWeight: '600'
        }}>
          AI-Generated Content with Factual Grounding
        </h3>
      </div>
 
      {/* Note: Quality chips moved to header bar; keep detail cards minimal here if needed */}
 
      {/* Research Sources */}
      <div style={{ marginBottom: '24px' }}>
        <h4 style={{
          margin: '0 0 16px 0',
          fontSize: '16px',
          fontWeight: '600',
          color: '#374151'
        }}>
          Research Sources ({researchSources.length})
        </h4>
        <div style={{
          display: 'grid',
          gap: '12px'
        }}>
          {researchSources.map((source, index) => (
            <div key={index} style={{
              padding: '16px',
              backgroundColor: 'white',
              borderRadius: '8px',
              border: '1px solid #e5e7eb',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                marginBottom: '8px'
              }}>
                <h5 style={{
                  margin: '0 0 8px 0',
                  fontSize: '14px',
                  fontWeight: '600',
                  color: '#1f2937'
                }}>
                  {source.title}
                </h5>
                <div style={{
                  fontSize: '12px',
                  color: '#6b7280',
                  backgroundColor: '#f3f4f6',
                  padding: '4px 8px',
                  borderRadius: '12px'
                }}>
                  Source {index + 1}
                </div>
              </div>
              
              <div style={{
                fontSize: '13px',
                color: '#6b7280',
                marginBottom: '8px',
                wordBreak: 'break-all'
              }}>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    color: '#0a66c2',
                    textDecoration: 'none'
                  }}
                >
                  {source.url}
                </a>
              </div>

              {/* Source Metrics */}
              <div style={{
                display: 'flex',
                gap: '16px',
                fontSize: '12px',
                color: '#6b7280'
              }}>
                {source.relevance_score && (
                  <span>Relevance: {formatScore(source.relevance_score)}</span>
                )}
                {source.credibility_score && (
                  <span>Credibility: {formatScore(source.credibility_score)}</span>
                )}
                {source.domain_authority && (
                  <span>Authority: {formatScore(source.domain_authority)}</span>
                )}
                {source.source_type && (
                  <span>Type: {source.source_type.replace('_', ' ')}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Citations */}
      {citations.length > 0 && (
        <div>
          <h4 style={{
            margin: '0 0 16px 0',
            fontSize: '16px',
            fontWeight: '600',
            color: '#374151'
          }}>
            Inline Citations ({citations.length})
          </h4>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            border: '1px solid #e5e7eb',
            padding: '16px'
          }}>
            <div style={{
              fontSize: '13px',
              color: '#6b7280',
              marginBottom: '12px'
            }}>
              The content includes {citations.length} inline citations linking to research sources.
            </div>
            <div style={{
              display: 'grid',
              gap: '8px'
            }}>
              {citations.map((citation, index) => (
                <div key={index} style={{
                  padding: '8px 12px',
                  backgroundColor: '#f9fafb',
                  borderRadius: '6px',
                  fontSize: '13px',
                  color: '#374151'
                }}>
                  <strong>{citation.reference}</strong>
                  {citation.text && (
                    <span style={{ marginLeft: '8px', color: '#6b7280' }}>
                      "{citation.text.substring(0, 100)}..."
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={{
        marginTop: '20px',
        paddingTop: '16px',
        borderTop: '1px solid #e5e7eb',
        fontSize: '12px',
        color: '#6b7280',
        textAlign: 'center'
      }}>
        This content was generated using AI with real-time web research and factual grounding.
        All claims are supported by current, verifiable sources.
      </div>
    </div>
  );
};
