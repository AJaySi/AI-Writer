import React from 'react';

interface LoadingIndicatorProps {
  isGenerating: boolean;
  loadingMessage: string;
  currentAction: string | null;
}

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  isGenerating,
  loadingMessage,
  currentAction
}) => {
  if (!isGenerating) return null;

  return (
    <div style={{
      marginBottom: '24px',
      padding: '16px',
      background: '#f8f9fa',
      border: '1px solid #e9ecef',
      borderRadius: '8px',
      textAlign: 'center'
    }}>
      <div style={{ marginBottom: '8px' }}>
        <div style={{
          width: '20px',
          height: '20px',
          border: '2px solid #e9ecef',
          borderTop: '2px solid #0a66c2',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
          margin: '0 auto'
        }} />
      </div>
      <div style={{ color: '#666', fontSize: '14px' }}>
        {loadingMessage || 'Generating content...'}
      </div>
      {currentAction && (
        <div style={{ color: '#999', fontSize: '12px', marginTop: '4px' }}>
          Action: {currentAction}
        </div>
      )}
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};
