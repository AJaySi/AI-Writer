// SEO CopilotKit Suggestions Component
// Displays contextual suggestions based on current SEO data and user state

import React, { useMemo, useState } from 'react';
import { useSEOCopilotSuggestions } from '../../stores/seoCopilotStore';
import { CopilotSuggestion } from '../../types/seoCopilotTypes';

interface SEOCopilotSuggestionsProps {
  maxSuggestions?: number;
  showCategories?: boolean;
  onSuggestionClick?: (suggestion: CopilotSuggestion) => void;
}

const SEOCopilotSuggestionsComponent: React.FC<SEOCopilotSuggestionsProps> = ({
  maxSuggestions = 4,
  showCategories = true,
  onSuggestionClick
}) => {
  const suggestions = useSEOCopilotSuggestions();
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);

  // Group suggestions by category (memoized)
  const groupedSuggestions = useMemo(() => {
    return suggestions.reduce((acc, suggestion) => {
      if (!acc[suggestion.category]) {
        acc[suggestion.category] = [];
      }
      acc[suggestion.category].push(suggestion);
      return acc;
    }, {} as Record<string, CopilotSuggestion[]>);
  }, [suggestions]);

  // Get category display info
  const getCategoryInfo = (category: string) => {
    const categoryInfo = {
      analysis: { icon: '🔍', name: 'Analysis', color: '#3B82F6' },
      optimization: { icon: '⚡', name: 'Optimization', color: '#10B981' },
      education: { icon: '🎓', name: 'Education', color: '#F59E0B' },
      monitoring: { icon: '📊', name: 'Monitoring', color: '#8B5CF6' }
    };
    return categoryInfo[category as keyof typeof categoryInfo] || { icon: '💡', name: category, color: '#6B7280' };
  };

  // Get priority badge
  const getPriorityBadge = (priority: string) => {
    const priorityInfo = {
      high: { label: 'High', color: '#EF4444', bgColor: '#FEE2E2' },
      medium: { label: 'Medium', color: '#F59E0B', bgColor: '#FEF3C7' },
      low: { label: 'Low', color: '#10B981', bgColor: '#D1FAE5' }
    };
    return priorityInfo[priority as keyof typeof priorityInfo] || { label: priority, color: '#6B7280', bgColor: '#F3F4F6' };
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion: CopilotSuggestion) => {
    if (onSuggestionClick) {
      onSuggestionClick(suggestion);
    } else {
      // Default behavior - trigger the action
      console.log('Suggestion clicked:', suggestion);
      // Here you would typically trigger the CopilotKit action
    }
  };

  // Render individual suggestion
  const renderSuggestion = (suggestion: CopilotSuggestion) => {
    const priorityBadge = getPriorityBadge(suggestion.priority);
    
    return (
      <div
        key={suggestion.id}
        className="suggestion-item"
        onClick={() => handleSuggestionClick(suggestion)}
      >
        <div className="suggestion-header">
          <div className="suggestion-icon">{suggestion.icon}</div>
          <div className="suggestion-content">
            <h4 className="suggestion-title">{suggestion.title}</h4>
            <p className="suggestion-message">{suggestion.message}</p>
          </div>
          <div 
            className="priority-badge"
            style={{ 
              color: priorityBadge.color, 
              backgroundColor: priorityBadge.bgColor 
            }}
          >
            {priorityBadge.label}
          </div>
        </div>
      </div>
    );
  };

  // Render category section
  const renderCategory = (category: string, categorySuggestions: CopilotSuggestion[]) => {
    const categoryInfo = getCategoryInfo(category);
    const isExpanded = expandedCategory === category;
    const displaySuggestions = isExpanded ? categorySuggestions : categorySuggestions.slice(0, 2);

    return (
      <div key={category} className="suggestion-category">
        <div 
          className="category-header"
          onClick={() => setExpandedCategory(isExpanded ? null : category)}
        >
          <div className="category-info">
            <span className="category-icon">{categoryInfo.icon}</span>
            <span className="category-name">{categoryInfo.name}</span>
            <span className="suggestion-count">({categorySuggestions.length})</span>
          </div>
          <div className="expand-icon">
            {isExpanded ? '−' : '+'}
          </div>
        </div>
        
        <div className={`category-suggestions ${isExpanded ? 'expanded' : ''}`}>
          {displaySuggestions.map(renderSuggestion)}
          {categorySuggestions.length > 2 && !isExpanded && (
            <div className="show-more">
              <button 
                onClick={() => setExpandedCategory(category)}
                className="show-more-btn"
              >
                Show {categorySuggestions.length - 2} more suggestions
              </button>
            </div>
          )}
        </div>
      </div>
    );
  };

  if (suggestions.length === 0) {
    return (
      <div className="seo-copilotkit-suggestions empty">
        <div className="empty-state">
          <div className="empty-icon">💡</div>
          <h3>No suggestions available</h3>
          <p>Start by analyzing your website to get personalized SEO suggestions.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="seo-copilotkit-suggestions">
      <div className="suggestions-header">
        <h3 className="suggestions-title">
          <span className="title-icon">🎯</span>
          SEO Suggestions
        </h3>
        <p className="suggestions-subtitle">
          Personalized recommendations based on your current SEO data
        </p>
      </div>

      <div className="suggestions-content">
        {showCategories ? (
          // Grouped by category
          Object.entries(groupedSuggestions).map(([category, categorySuggestions]) =>
            renderCategory(category, categorySuggestions)
          )
        ) : (
          // Flat list
          <div className="suggestions-list">
            {suggestions.slice(0, maxSuggestions).map(renderSuggestion)}
          </div>
        )}
      </div>

      <style>{`
        .seo-copilotkit-suggestions {
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          overflow: hidden;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .suggestions-header {
          padding: 20px 20px 16px;
          border-bottom: 1px solid #f3f4f6;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .suggestions-title {
          margin: 0 0 4px 0;
          font-size: 18px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .title-icon {
          font-size: 20px;
        }

        .suggestions-subtitle {
          margin: 0;
          font-size: 14px;
          opacity: 0.9;
        }

        .suggestions-content {
          max-height: 500px;
          overflow-y: auto;
        }

        .suggestion-category {
          border-bottom: 1px solid #f3f4f6;
        }

        .suggestion-category:last-child {
          border-bottom: none;
        }

        .category-header {
          padding: 16px 20px;
          background: #f9fafb;
          cursor: pointer;
          display: flex;
          justify-content: space-between;
          align-items: center;
          transition: background-color 0.2s;
        }

        .category-header:hover {
          background: #f3f4f6;
        }

        .category-info {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .category-icon {
          font-size: 16px;
        }

        .category-name {
          font-weight: 600;
          color: #374151;
        }

        .suggestion-count {
          font-size: 12px;
          color: #6b7280;
          background: #e5e7eb;
          padding: 2px 6px;
          border-radius: 10px;
        }

        .expand-icon {
          font-size: 18px;
          font-weight: bold;
          color: #6b7280;
          width: 20px;
          height: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .category-suggestions {
          max-height: 0;
          overflow: hidden;
          transition: max-height 0.3s ease-out;
        }

        .category-suggestions.expanded {
          max-height: 1000px;
        }

        .suggestion-item {
          padding: 16px 20px;
          border-bottom: 1px solid #f3f4f6;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .suggestion-item:hover {
          background: #f9fafb;
        }

        .suggestion-item:last-child {
          border-bottom: none;
        }

        .suggestion-header {
          display: flex;
          align-items: flex-start;
          gap: 12px;
        }

        .suggestion-icon {
          font-size: 20px;
          flex-shrink: 0;
          margin-top: 2px;
        }

        .suggestion-content {
          flex: 1;
          min-width: 0;
        }

        .suggestion-title {
          margin: 0 0 4px 0;
          font-size: 14px;
          font-weight: 600;
          color: #111827;
          line-height: 1.4;
        }

        .suggestion-message {
          margin: 0;
          font-size: 13px;
          color: #6b7280;
          line-height: 1.4;
        }

        .priority-badge {
          font-size: 10px;
          font-weight: 600;
          padding: 2px 6px;
          border-radius: 8px;
          flex-shrink: 0;
          margin-top: 2px;
        }

        .show-more {
          padding: 12px 20px;
          text-align: center;
          border-top: 1px solid #f3f4f6;
        }

        .show-more-btn {
          background: none;
          border: none;
          color: #3b82f6;
          font-size: 13px;
          font-weight: 500;
          cursor: pointer;
          padding: 4px 8px;
          border-radius: 4px;
          transition: background-color 0.2s;
        }

        .show-more-btn:hover {
          background: #eff6ff;
        }

        .suggestions-list {
          padding: 0;
        }

        .empty {
          padding: 40px 20px;
          text-align: center;
        }

        .empty-state {
          color: #6b7280;
        }

        .empty-icon {
          font-size: 48px;
          margin-bottom: 16px;
        }

        .empty-state h3 {
          margin: 0 0 8px 0;
          font-size: 16px;
          font-weight: 600;
          color: #374151;
        }

        .empty-state p {
          margin: 0;
          font-size: 14px;
        }

        /* Scrollbar styling */
        .suggestions-content::-webkit-scrollbar {
          width: 6px;
        }

        .suggestions-content::-webkit-scrollbar-track {
          background: #f1f5f9;
        }

        .suggestions-content::-webkit-scrollbar-thumb {
          background: #cbd5e1;
          border-radius: 3px;
        }

        .suggestions-content::-webkit-scrollbar-thumb:hover {
          background: #94a3b8;
        }
      `}</style>
    </div>
  );
};

const SEOCopilotSuggestions = React.memo(SEOCopilotSuggestionsComponent);
export default SEOCopilotSuggestions;
