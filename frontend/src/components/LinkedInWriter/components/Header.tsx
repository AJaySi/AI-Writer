import React from 'react';
import { LinkedInPreferences } from '../utils/storageUtils';
// Temporary fix: use require for image import
const alwrityLogo = require('../../../assets/images/alwrity_logo.png');

interface HeaderProps {
  userPreferences: LinkedInPreferences;
  chatHistory: any[];
  showPreferencesModal: boolean;
  showContextModal: boolean;
  context: string;
  onPreferencesModalChange: (show: boolean) => void;
  onContextModalChange: (show: boolean) => void;
  onContextChange: (value: string) => void;
  onPreferencesChange: (prefs: Partial<LinkedInPreferences>) => void;
  onCopy: () => void;
  onClear: () => void;
  onClearHistory: () => void;
  draft: string;
  getHistoryLength: () => number;
}

export const Header: React.FC<HeaderProps> = ({
  userPreferences,
  chatHistory,
  showPreferencesModal,
  showContextModal,
  context,
  onPreferencesModalChange,
  onContextModalChange,
  onContextChange,
  onPreferencesChange,
  onCopy,
  onClear,
  onClearHistory,
  draft,
  getHistoryLength
}) => {
  const handlePreferenceChange = (key: keyof LinkedInPreferences, value: any) => {
    onPreferencesChange({ [key]: value });
  };

  return (
    <div style={{
      background: 'linear-gradient(135deg, #0a66c2 0%, #0056b3 100%)',
      color: 'white',
      padding: '20px 24px',
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        {/* Left Section - Logo and Title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <img 
              src={alwrityLogo} 
              alt="ALwrity Logo" 
              style={{ 
                height: '36px', 
                width: 'auto',
                filter: 'brightness(0) invert(1) drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2))'
              }} 
            />
            <div>
              <h1 style={{ 
                margin: 0, 
                fontSize: '26px', 
                fontWeight: 700,
                letterSpacing: '-0.5px'
              }}>
                LinkedIn Writer
              </h1>
              <p style={{ 
                margin: '6px 0 0 0', 
                fontSize: '14px', 
                opacity: 0.9,
                fontWeight: 400
              }}>
                Professional content creation for LinkedIn
              </p>
            </div>
          </div>
          
          {/* Control Buttons */}
          <div style={{ display: 'flex', gap: '12px' }}>
            {/* Preferences Button */}
            <div 
              style={{ 
                position: 'relative',
                cursor: 'pointer'
              }}
              onMouseEnter={() => onPreferencesModalChange(true)}
              onMouseLeave={() => onPreferencesModalChange(false)}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 16px',
                background: 'rgba(255, 255, 255, 0.15)',
                borderRadius: '24px',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                transition: 'all 0.2s ease',
                backdropFilter: 'blur(10px)'
              }}>
                <span style={{ fontSize: '14px', opacity: 0.9 }}>⚙️</span>
                <span style={{ fontSize: '13px', fontWeight: 600 }}>Preferences</span>
                <span style={{ fontSize: '10px', opacity: 0.7 }}>▼</span>
              </div>
              
              {/* Preferences Modal */}
              {showPreferencesModal && (
                <div style={{
                  position: 'absolute',
                  top: '100%',
                  left: '0',
                  width: '400px',
                  background: 'white',
                  borderRadius: '12px',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
                  border: '1px solid #e9ecef',
                  padding: '20px',
                  zIndex: 1000,
                  marginTop: '8px',
                  animation: 'slideIn 0.2s ease-out'
                }}>
                  <div style={{ marginBottom: '16px' }}>
                    <h4 style={{ margin: '0 0 12px 0', color: '#333', fontSize: '16px', fontWeight: 600 }}>
                      Content Preferences & Context
                    </h4>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '16px' }}>
                      <strong>Current Settings:</strong> {userPreferences.tone} tone • {userPreferences.industry || 'Not set'} industry • {chatHistory.length} messages
                    </div>
                  </div>
                  
                  {/* Preferences Grid */}
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: '12px',
                    marginBottom: '16px'
                  }}>
                    <div>
                      <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Tone</div>
                      <select
                        value={userPreferences.tone}
                        onChange={(e) => handlePreferenceChange('tone', e.target.value)}
                        style={{
                          width: '100%',
                          padding: '6px 8px',
                          border: '1px solid #ddd',
                          borderRadius: 4,
                          background: '#f8f9fa',
                          fontSize: '12px'
                        }}
                      >
                        <option>Professional</option>
                        <option>Casual</option>
                        <option>Thought Leadership</option>
                        <option>Conversational</option>
                        <option>Technical</option>
                      </select>
                    </div>
                    <div>
                      <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Industry</div>
                      <input
                        value={userPreferences.industry}
                        onChange={(e) => handlePreferenceChange('industry', e.target.value)}
                        placeholder="e.g., Technology"
                        style={{
                          width: '100%',
                          padding: '6px 8px',
                          border: '1px solid #ddd',
                          borderRadius: 4,
                          background: '#f8f9fa',
                          fontSize: '12px'
                        }}
                      />
                    </div>
                    <div>
                      <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Target Audience</div>
                      <input
                        value={userPreferences.target_audience}
                        onChange={(e) => handlePreferenceChange('target_audience', e.target.value)}
                        placeholder="e.g., Product Managers"
                        style={{
                          width: '100%',
                          padding: '6px 8px',
                          border: '1px solid #ddd',
                          borderRadius: 4,
                          background: '#f8f9fa',
                          fontSize: '12px'
                        }}
                      />
                    </div>
                    <div>
                      <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Writing Style</div>
                      <select
                        value={userPreferences.writing_style}
                        onChange={(e) => handlePreferenceChange('writing_style', e.target.value)}
                        style={{
                          width: '100%',
                          padding: '6px 8px',
                          border: '1px solid #ddd',
                          borderRadius: 4,
                          background: '#f8f9fa',
                          fontSize: '12px'
                        }}
                      >
                        <option>Clear and Concise</option>
                        <option>Storytelling</option>
                        <option>Analytical</option>
                        <option>Persuasive</option>
                      </select>
                    </div>
                  </div>
                  
                  {/* Checkboxes */}
                  <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
                    <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '12px' }}>
                      <input
                        type="checkbox"
                        checked={userPreferences.hashtag_preferences}
                        onChange={(e) => handlePreferenceChange('hashtag_preferences', e.target.checked)}
                        style={{ margin: 0 }}
                      />
                      Include Hashtags
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '12px' }}>
                      <input
                        type="checkbox"
                        checked={userPreferences.cta_preferences}
                        onChange={(e) => handlePreferenceChange('cta_preferences', e.target.checked)}
                        style={{ margin: 0 }}
                      />
                      Include Call-to-Action
                    </label>
                  </div>
                  
                  {/* Current Context Display */}
                  <div style={{ 
                    borderTop: '1px solid #e9ecef', 
                    paddingTop: '12px',
                    fontSize: '11px'
                  }}>
                    <div style={{ marginBottom: '8px', fontWeight: 600, color: '#333' }}>Current Context:</div>
                    <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                      {userPreferences.tone && (
                        <span style={{
                          background: '#e3f2fd',
                          color: '#1976d2',
                          padding: '2px 6px',
                          borderRadius: 8,
                          fontSize: '10px'
                        }}>
                          {userPreferences.tone}
                        </span>
                      )}
                      {userPreferences.industry && (
                        <span style={{
                          background: '#f3e5f5',
                          color: '#7b1fa2',
                          padding: '2px 6px',
                          borderRadius: 8,
                          fontSize: '10px'
                        }}>
                          {userPreferences.industry}
                        </span>
                      )}
                      {userPreferences.target_audience && (
                        <span style={{
                          background: '#e8f5e8',
                          color: '#388e3c',
                          padding: '2px 6px',
                          borderRadius: 8,
                          fontSize: '10px'
                        }}>
                          {userPreferences.target_audience}
                        </span>
                      )}
                      <span style={{
                        background: '#fff3e0',
                        color: '#f57c00',
                        padding: '2px 6px',
                        borderRadius: 8,
                        fontSize: '10px'
                      }}>
                        {chatHistory.length} messages
                      </span>
                    </div>
                  </div>
                  
                  <style>{`
                    @keyframes slideIn {
                      from { opacity: 0; transform: translateY(-10px); }
                      to { opacity: 1; transform: translateY(0); }
                    }
                  `}</style>
                </div>
              )}
            </div>
            
                         {/* Context & Notes Button */}
             <div 
               style={{ 
                 position: 'relative',
                 cursor: 'pointer'
               }}
               onMouseEnter={() => onContextModalChange(true)}
               onMouseLeave={() => onContextModalChange(false)}
             >
               <div style={{
                 display: 'flex',
                 alignItems: 'center',
                 gap: '8px',
                 padding: '10px 16px',
                 background: 'rgba(255, 255, 255, 0.15)',
                 borderRadius: '24px',
                 border: '1px solid rgba(255, 255, 255, 0.2)',
                 transition: 'all 0.2s ease',
                 backdropFilter: 'blur(10px)'
               }}>
                 <span style={{ fontSize: '14px', opacity: 0.9 }}>📝</span>
                 <span style={{ fontSize: '13px', fontWeight: 600 }}>Context & Notes</span>
                 <span style={{ fontSize: '10px', opacity: 0.7 }}>▼</span>
               </div>
              
              {/* Context & Notes Modal */}
              {showContextModal && (
                <div style={{
                  position: 'absolute',
                  top: '100%',
                  left: '0',
                  width: '400px',
                  background: 'white',
                  borderRadius: '12px',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
                  border: '1px solid #e9ecef',
                  padding: '20px',
                  zIndex: 1000,
                  marginTop: '8px',
                  animation: 'slideIn 0.2s ease-out'
                }}>
                  <div style={{ marginBottom: '16px' }}>
                    <h4 style={{ margin: '0 0 12px 0', color: '#333', fontSize: '16px', fontWeight: 600 }}>
                      Context & Notes
                    </h4>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '16px' }}>
                      Add context, notes, or specific requirements for your LinkedIn content
                    </div>
                  </div>
                  
                  <textarea
                    value={context}
                    onChange={(e) => onContextChange(e.target.value)}
                    placeholder="Add context, notes, or specific requirements for your LinkedIn content..."
                    style={{
                      width: '100%',
                      minHeight: '120px',
                      padding: '12px',
                      border: '1px solid #ddd',
                      borderRadius: '8px',
                      fontSize: '14px',
                      fontFamily: 'inherit',
                      resize: 'vertical',
                      background: '#f8f9fa'
                    }}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div style={{ display: 'flex', gap: 12 }}>
          <button
            onClick={onCopy}
            disabled={!draft.trim()}
            style={{
              padding: '8px 16px',
              background: 'rgba(255, 255, 255, 0.1)',
              color: 'white',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: 6,
              cursor: draft.trim() ? 'pointer' : 'not-allowed',
              fontSize: 14,
              fontWeight: 500
            }}
          >
            Copy
          </button>
          <button
            onClick={onClear}
            disabled={!draft.trim()}
            style={{
              padding: '8px 16px',
              background: 'rgba(255, 255, 255, 0.1)',
              color: 'white',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: 6,
              cursor: draft.trim() ? 'pointer' : 'not-allowed',
              fontSize: 14,
              fontWeight: 500
            }}
          >
            Clear
          </button>
          <button
            onClick={onClearHistory}
            style={{
              padding: '8px 16px',
              background: 'rgba(255, 255, 255, 0.1)',
              color: 'white',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: 6,
              cursor: 'pointer',
              fontSize: 14,
              fontWeight: 500
            }}
            title={`Clear chat memory (${getHistoryLength()} messages)`}
          >
            Clear Memory ({getHistoryLength()})
          </button>
        </div>
      </div>
    </div>
  );
};
