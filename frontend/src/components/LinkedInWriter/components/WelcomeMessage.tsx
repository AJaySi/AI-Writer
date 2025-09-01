import React from 'react';

interface WelcomeMessageProps {
  draft: string;
  isGenerating: boolean;
}

export const WelcomeMessage: React.FC<WelcomeMessageProps> = ({
  draft,
  isGenerating
}) => {
  if (draft || isGenerating) return null;

  return (
    <div style={{
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '48px 24px',
      color: '#666'
    }}>
      <div style={{
        fontSize: '64px',
        marginBottom: '24px',
        opacity: 0.4
      }}>
        ✍️
      </div>
      <h3 style={{
        margin: '0 0 20px 0',
        color: '#333',
        fontSize: '28px',
        fontWeight: '600',
        textAlign: 'center'
      }}>
        Welcome to LinkedIn Writer
      </h3>
      <p style={{
        margin: '0 0 32px 0',
        color: '#666', 
        fontSize: '16px',
        lineHeight: '1.6',
        textAlign: 'center',
        maxWidth: '500px'
      }}>
        Click the ALwrity Co-Pilot icon in the bottom-right corner to access the AI assistant. You can generate LinkedIn posts, articles, carousels, video scripts, and comment responses.
      </p>
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: '12px',
        padding: '16px 20px',
        background: '#f8f9fa',
        borderRadius: '8px',
        border: '1px solid #e9ecef',
        boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
      }}>
        <div style={{
          width: '10px',
          height: '10px',
          background: '#0a66c2',
          borderRadius: '50%',
          animation: 'pulse 2s infinite'
        }} />
        <span style={{ fontSize: '15px', color: '#666', fontWeight: '500' }}>
          AI Assistant is ready - look for the ALwrity Co-Pilot icon
        </span>
        <style>{`
          @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
          }
        `}</style>
      </div>
    </div>
  );
};
