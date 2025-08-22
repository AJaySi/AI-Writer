# Calendar Generation Modal

## Overview

The CalendarGenerationModal is a specialized transparency modal for the 12-step calendar generation process. It provides real-time progress tracking, educational content, and detailed insights for each step of the calendar generation workflow.

## Features

### ✅ Implemented (Phase 1A - Modal Foundation)

1. **Core Modal Structure**
   - Full-screen dialog with proper Material-UI integration
   - Responsive design with proper sizing and layout
   - Close functionality and action buttons

2. **Progress Tracking**
   - Overall progress bar with percentage display
   - Step indicators for Phase 1 (Steps 1-3)
   - Quality score chips with color coding
   - Status indicators (initializing, step1, step2, step3, completed, error)

3. **Tabbed Interface**
   - Live Progress tab
   - Step Results tab
   - Data Sources tab
   - Quality Gates tab
   - Smooth animations with Framer Motion

4. **Educational Panel**
   - Expandable educational content section
   - Step-specific tips and examples
   - User-friendly toggle interface

5. **Polling Integration**
   - Custom hook for real-time progress updates
   - Error handling and retry logic
   - Configurable polling intervals

6. **Mock Data Support**
   - Development-ready mock data for Phase 1
   - Realistic progress simulation
   - Quality scores and educational content

## File Structure

```
CalendarGenerationModal/
├── index.ts                          # Main exports
├── types.ts                          # TypeScript interfaces
├── CalendarGenerationModal.tsx       # Main modal component
├── TestModal.tsx                     # Test component
└── README.md                         # This file
```

## Usage

### Basic Usage

```tsx
import { CalendarGenerationModal } from './CalendarGenerationModal';

const MyComponent = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleComplete = (results) => {
    console.log('Calendar generation completed:', results);
    setIsModalOpen(false);
  };

  const handleError = (error) => {
    console.error('Calendar generation error:', error);
    setIsModalOpen(false);
  };

  return (
    <CalendarGenerationModal
      open={isModalOpen}
      onClose={() => setIsModalOpen(false)}
      sessionId="session-123"
      initialConfig={{
        userId: 'user123',
        strategyId: 'strategy456',
        calendarType: 'monthly',
        platforms: ['LinkedIn', 'Twitter', 'Website'],
        duration: 30,
        postingFrequency: 'daily'
      }}
      onComplete={handleComplete}
      onError={handleError}
    />
  );
};
```

### Testing

Use the TestModal component to verify functionality:

```tsx
import { TestCalendarGenerationModal } from './CalendarGenerationModal';

// Add to your app for testing
<TestCalendarGenerationModal />
```

## Configuration

### CalendarConfig Interface

```typescript
interface CalendarConfig {
  userId: string;
  strategyId: string;
  calendarType: 'monthly' | 'quarterly' | 'yearly';
  platforms: string[];
  duration: number;
  postingFrequency: 'daily' | 'weekly' | 'biweekly';
}
```

### Polling Configuration

The modal uses a polling mechanism with the following defaults:
- Polling interval: 2 seconds
- Retry interval: 5 seconds (on error)
- Endpoint: `/api/calendar-generation/progress/${sessionId}`

## Integration Points

### Backend Integration

The modal expects the following API endpoints:

1. **Progress Endpoint**: `GET /api/calendar-generation/progress/{sessionId}`
   - Returns real-time progress data
   - Includes step results, quality scores, and educational content

2. **Completion Handling**: 
   - Modal automatically handles completion state
   - Calls `onComplete` callback with results
   - Calls `onError` callback on failures

### Frontend Integration

1. **State Management**: Ready for Zustand store integration
2. **Routing**: Can be integrated with React Router
3. **Theming**: Uses Material-UI theme system
4. **Accessibility**: Built with accessibility best practices

## Development Status

### ✅ Completed
- Modal foundation and structure
- Progress tracking UI
- Tabbed interface
- Educational panel
- Polling mechanism
- Mock data for Phase 1
- TypeScript types
- Test component

### 🔄 Next Steps (Phase 1B)
1. **Enhanced Step Results Panel**
   - Detailed step result display
   - Data source attribution
   - Quality gate validation results

2. **Data Source Transparency**
   - Integration with existing DataSourceTransparency component
   - Real data source attribution
   - Confidence scores and timestamps

3. **Quality Gates Panel**
   - Real-time quality gate validation
   - Pass/fail status indicators
   - Recommendations and improvements

4. **Backend Integration**
   - Connect to real Phase 1 backend endpoints
   - Replace mock data with live data
   - Error handling for real API calls

### 📋 Future Enhancements (Phase 2+)
1. **Advanced Animations**
   - Step transition animations
   - Progress bar animations
   - Loading states and spinners

2. **User Preferences**
   - Transparency level settings
   - Educational content preferences
   - Auto-expand options

3. **Export Functionality**
   - Progress reports
   - Quality analysis exports
   - Educational content downloads

## Technical Details

### Dependencies
- React 18+
- Material-UI (MUI) v5
- Framer Motion
- TypeScript

### Performance Considerations
- Lazy loading of tab content
- Optimized re-renders with React.memo
- Efficient polling with useCallback
- Minimal bundle size impact

### Accessibility Features
- ARIA labels and descriptions
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check TypeScript configuration
   - Verify file paths and exports

2. **Polling Issues**
   - Check network connectivity
   - Verify API endpoint availability
   - Review browser console for errors

3. **Styling Issues**
   - Ensure Material-UI theme is properly configured
   - Check for CSS conflicts
   - Verify responsive breakpoints

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
REACT_APP_DEBUG_CALENDAR_MODAL=true
```

## Contributing

When contributing to this component:

1. Follow the existing code structure
2. Add TypeScript types for new features
3. Include test cases for new functionality
4. Update this README for new features
5. Ensure accessibility compliance

## License

This component is part of the ALwrity project and follows the same licensing terms.
