import React from 'react';
import {
  Box,
  Button,
  Alert
} from '@mui/material';
import {
  Check as CheckIcon,
  CalendarToday as CalendarIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { StrategyData } from '../types/strategy.types';

interface StrategyActionsProps {
  strategyData: StrategyData | null;
  strategyConfirmed: boolean;
  onConfirmStrategy: () => void;
  onGenerateContentCalendar: () => void;
  onRefreshData: () => void;
}

const StrategyActions: React.FC<StrategyActionsProps> = ({
  strategyData,
  strategyConfirmed,
  onConfirmStrategy,
  onGenerateContentCalendar,
  onRefreshData
}) => {
  return (
    <Box sx={{ mt: 4 }}>
      {/* Strategy Confirmation Status */}
      {strategyConfirmed && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Alert 
            severity="success" 
            sx={{ 
              mb: 3,
              borderRadius: 2,
              boxShadow: '0 4px 12px rgba(76, 175, 80, 0.2)',
              border: '1px solid rgba(76, 175, 80, 0.3)'
            }}
            action={
              <Button 
                color="inherit" 
                size="small" 
                onClick={onGenerateContentCalendar}
                startIcon={<CalendarIcon />}
                sx={{
                  fontWeight: 600,
                  '&:hover': {
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    transform: 'translateY(-1px)'
                  },
                  transition: 'all 0.3s ease'
                }}
              >
                Generate Content Calendar
              </Button>
            }
          >
            Strategy confirmed! You can now generate a content calendar based on this strategy.
          </Alert>
        </motion.div>
      )}

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
        {!strategyConfirmed ? (
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button
              variant="contained"
              size="large"
              onClick={onConfirmStrategy}
              startIcon={<CheckIcon />}
              sx={{ 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: 3,
                px: 4,
                py: 1.5,
                fontWeight: 600,
                boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                  boxShadow: '0 12px 40px rgba(102, 126, 234, 0.4)',
                  transform: 'translateY(-2px)'
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
              }}
            >
              Confirm Strategy
            </Button>
          </motion.div>
        ) : (
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button
              variant="contained"
              size="large"
              onClick={onGenerateContentCalendar}
              startIcon={<CalendarIcon />}
              color="success"
              sx={{ 
                borderRadius: 3,
                px: 4,
                py: 1.5,
                fontWeight: 600,
                boxShadow: '0 8px 32px rgba(76, 175, 80, 0.3)',
                '&:hover': {
                  boxShadow: '0 12px 40px rgba(76, 175, 80, 0.4)',
                  transform: 'translateY(-2px)'
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
              }}
            >
              Generate Content Calendar
            </Button>
          </motion.div>
        )}
        
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Button
            variant="outlined"
            size="large"
            onClick={onRefreshData}
            startIcon={<RefreshIcon />}
            sx={{ 
              borderRadius: 3,
              px: 4,
              py: 1.5,
              fontWeight: 600,
              borderColor: 'rgba(102, 126, 234, 0.3)',
              color: '#667eea',
              '&:hover': {
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.05)',
                transform: 'translateY(-2px)'
              },
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
            }}
          >
            Refresh Data
          </Button>
        </motion.div>
      </Box>
    </Box>
  );
};

export default StrategyActions; 