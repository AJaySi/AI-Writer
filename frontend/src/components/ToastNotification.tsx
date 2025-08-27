import React, { useState, useEffect } from 'react';
import { Snackbar, Alert, AlertColor } from '@mui/material';
import { Psychology as MindIcon } from '@mui/icons-material';

interface ToastNotificationProps {
  open: boolean;
  message: string;
  severity?: AlertColor;
  autoHideDuration?: number;
  onClose: () => void;
}

interface MemoryToastProps {
  open: boolean;
  domainName: string;
  onClose: () => void;
}

export const ToastNotification: React.FC<ToastNotificationProps> = ({
  open,
  message,
  severity = 'success',
  autoHideDuration = 4000,
  onClose
}) => {
  return (
    <Snackbar
      open={open}
      autoHideDuration={autoHideDuration}
      onClose={onClose}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
    >
      <Alert 
        onClose={onClose} 
        severity={severity} 
        sx={{ width: '100%' }}
        variant="filled"
      >
        {message}
      </Alert>
    </Snackbar>
  );
};

export const MemoryToast: React.FC<MemoryToastProps> = ({
  open,
  domainName,
  onClose
}) => {
  return (
    <Snackbar
      open={open}
      autoHideDuration={4000}
      onClose={onClose}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
    >
      <Alert 
        onClose={onClose} 
        severity="success" 
        sx={{ 
          width: '100%',
          '& .MuiAlert-icon': {
            color: '#4caf50'
          }
        }}
        variant="filled"
        icon={<MindIcon />}
      >
        {domainName} memory updated
      </Alert>
    </Snackbar>
  );
};

// Hook for managing toast notifications
export const useToast = () => {
  const [toast, setToast] = useState<{
    open: boolean;
    message: string;
    severity: AlertColor;
  }>({
    open: false,
    message: '',
    severity: 'success'
  });

  const [memoryToast, setMemoryToast] = useState<{
    open: boolean;
    domainName: string;
  }>({
    open: false,
    domainName: 'ALwrity'
  });

  const showToast = (message: string, severity: AlertColor = 'success') => {
    setToast({
      open: true,
      message,
      severity
    });
  };

  const showMemoryToast = (domainName: string = 'ALwrity') => {
    setMemoryToast({
      open: true,
      domainName
    });
  };

  const hideToast = () => {
    setToast(prev => ({ ...prev, open: false }));
  };

  const hideMemoryToast = () => {
    setMemoryToast(prev => ({ ...prev, open: false }));
  };

  const ToastComponent = () => (
    <>
      <ToastNotification
        open={toast.open}
        message={toast.message}
        severity={toast.severity}
        onClose={hideToast}
      />
      <MemoryToast
        open={memoryToast.open}
        domainName={memoryToast.domainName}
        onClose={hideMemoryToast}
      />
    </>
  );

  return {
    showToast,
    showMemoryToast,
    ToastComponent
  };
};