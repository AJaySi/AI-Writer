import React, { useState } from 'react';
import { Button, Box, Typography } from '@mui/material';
import CalendarGenerationModal from './CalendarGenerationModal';

const TestCalendarGenerationModal: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleComplete = (results: any) => {
    console.log('Calendar generation completed:', results);
    setIsModalOpen(false);
  };

  const handleError = (error: string) => {
    console.error('Calendar generation error:', error);
    setIsModalOpen(false);
  };

  const mockConfig = {
    userId: 'user123',
    strategyId: 'strategy456',
    calendarType: 'monthly' as const,
    platforms: ['LinkedIn', 'Twitter', 'Website'],
    duration: 30,
    postingFrequency: 'daily' as const
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Calendar Generation Modal Test
      </Typography>
      
      <Button
        variant="contained"
        onClick={handleOpenModal}
        sx={{ mb: 2 }}
      >
        Open Calendar Generation Modal
      </Button>

      <CalendarGenerationModal
        open={isModalOpen}
        onClose={handleCloseModal}
        sessionId="test-session-123"
        initialConfig={mockConfig}
        onComplete={handleComplete}
        onError={handleError}
      />

      <Typography variant="body1" color="text.secondary">
        This test component allows you to verify the CalendarGenerationModal functionality.
        The modal will display mock data for Phase 1 (Steps 1-3) with a 94% quality score.
      </Typography>
    </Box>
  );
};

export default TestCalendarGenerationModal;
