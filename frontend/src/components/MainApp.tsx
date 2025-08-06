import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';

const MainApp: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Paper elevation={3} sx={{ p: 4, maxWidth: 800, margin: 'auto' }}>
        <Typography variant="h4" align="center" gutterBottom>
          Welcome to Alwrity! 🚀
        </Typography>
        <Typography variant="body1" align="center" sx={{ mb: 3 }}>
          Your onboarding is complete. The main application is ready to use.
        </Typography>
        
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Available Features:
          </Typography>
          <Typography variant="body2" component="ul" sx={{ pl: 2 }}>
            <li>AI Content Writers (Blog, Social Media, Email, etc.)</li>
            <li>SEO Tools and Analytics</li>
            <li>Website Analysis</li>
            <li>Content Calendar</li>
            <li>Research Tools</li>
            <li>And much more...</li>
          </Typography>
        </Box>

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="textSecondary">
            This is where the main Alwrity application will be implemented.
            All existing functionality will be migrated here.
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
};

export default MainApp; 