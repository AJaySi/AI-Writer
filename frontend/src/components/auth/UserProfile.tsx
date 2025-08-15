import React, { useState } from 'react';
import {
  Box,
  Avatar,
  Typography,
  Button,
  Paper,
  Divider,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  AccountCircle,
  Settings,
  Logout,
  Edit,
  Save,
  Cancel,
  Google,
  GitHub,
  Facebook,
  Email
} from '@mui/icons-material';
import { useAuthState } from '../../hooks/useAuthState';

const UserProfile: React.FC = () => {
  const { user, provider, isLoading, error, signOut, refreshUser, clearError } = useAuthState();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || ''
  });
  const [showLogoutDialog, setShowLogoutDialog] = useState(false);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleEditToggle = () => {
    if (isEditing) {
      // Save changes
      handleSaveProfile();
    } else {
      setIsEditing(true);
      setEditForm({
        firstName: user?.firstName || '',
        lastName: user?.lastName || ''
      });
    }
    handleMenuClose();
  };

  const handleSaveProfile = async () => {
    try {
      if (user) {
        await user.update({
          firstName: editForm.firstName,
          lastName: editForm.lastName
        });
        await refreshUser();
        setIsEditing(false);
        clearError();
      }
    } catch (err: any) {
      console.error('Failed to update profile:', err);
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditForm({
      firstName: user?.firstName || '',
      lastName: user?.lastName || ''
    });
  };

  const handleLogout = async () => {
    await signOut();
    setShowLogoutDialog(false);
    handleMenuClose();
  };

  const getProviderIcon = (provider: string) => {
    switch (provider) {
      case 'google':
        return <Google />;
      case 'github':
        return <GitHub />;
      case 'facebook':
        return <Facebook />;
      case 'email':
        return <Email />;
      default:
        return <AccountCircle />;
    }
  };

  const getProviderColor = (provider: string) => {
    switch (provider) {
      case 'google':
        return '#4285f4';
      case 'github':
        return '#24292e';
      case 'facebook':
        return '#1877f2';
      case 'email':
        return '#666';
      default:
        return '#666';
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={2}>
        <CircularProgress size={24} />
      </Box>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <>
      <Paper
        elevation={2}
        sx={{
          p: 3,
          borderRadius: 2,
          maxWidth: 400,
          width: '100%'
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Avatar
            src={user.imageUrl}
            sx={{ width: 64, height: 64, mr: 2 }}
          >
            {user.firstName?.[0] || user.emailAddresses?.[0]?.emailAddress?.[0] || 'U'}
          </Avatar>
          
          <Box sx={{ flex: 1 }}>
            {isEditing ? (
              <Box>
                <TextField
                  size="small"
                  label="First Name"
                  value={editForm.firstName}
                  onChange={(e) => setEditForm(prev => ({ ...prev, firstName: e.target.value }))}
                  sx={{ mb: 1, width: '100%' }}
                />
                <TextField
                  size="small"
                  label="Last Name"
                  value={editForm.lastName}
                  onChange={(e) => setEditForm(prev => ({ ...prev, lastName: e.target.value }))}
                  sx={{ width: '100%' }}
                />
              </Box>
            ) : (
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                {user.firstName && user.lastName 
                  ? `${user.firstName} ${user.lastName}`
                  : user.firstName || user.emailAddresses?.[0]?.emailAddress || 'User'
                }
              </Typography>
            )}
            
            <Typography variant="body2" color="text.secondary">
              {user.emailAddresses?.[0]?.emailAddress}
            </Typography>
          </Box>

          <IconButton onClick={handleMenuOpen}>
            <Settings />
          </IconButton>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {isEditing && (
          <Box sx={{ mb: 2 }}>
            <Button
              size="small"
              startIcon={<Save />}
              onClick={handleSaveProfile}
              sx={{ mr: 1 }}
            >
              Save
            </Button>
            <Button
              size="small"
              startIcon={<Cancel />}
              onClick={handleCancelEdit}
              variant="outlined"
            >
              Cancel
            </Button>
          </Box>
        )}

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
            Authentication Method
          </Typography>
          <Chip
            icon={getProviderIcon(provider || 'email')}
            label={provider ? `${provider.charAt(0).toUpperCase() + provider.slice(1)}` : 'Email'}
            sx={{
              bgcolor: getProviderColor(provider || 'email'),
              color: 'white',
              '& .MuiChip-icon': { color: 'white' }
            }}
          />
        </Box>

        <Box>
          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
            Account Details
          </Typography>
          <Typography variant="body2" sx={{ mb: 0.5 }}>
            <strong>User ID:</strong> {user.id}
          </Typography>
          <Typography variant="body2" sx={{ mb: 0.5 }}>
            <strong>Created:</strong> {new Date(user.createdAt).toLocaleDateString()}
          </Typography>
          <Typography variant="body2">
            <strong>Last Sign In:</strong> {new Date(user.lastSignInAt).toLocaleDateString()}
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Button
          fullWidth
          variant="outlined"
          color="error"
          startIcon={<Logout />}
          onClick={() => setShowLogoutDialog(true)}
        >
          Sign Out
        </Button>
      </Paper>

      {/* User Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        <MenuItem onClick={handleEditToggle}>
          <ListItemIcon>
            <Edit fontSize="small" />
          </ListItemIcon>
          <ListItemText>
            {isEditing ? 'Save Profile' : 'Edit Profile'}
          </ListItemText>
        </MenuItem>
        <MenuItem onClick={() => setShowLogoutDialog(true)}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          <ListItemText>Sign Out</ListItemText>
        </MenuItem>
      </Menu>

      {/* Logout Confirmation Dialog */}
      <Dialog
        open={showLogoutDialog}
        onClose={() => setShowLogoutDialog(false)}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>Confirm Sign Out</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to sign out of your account?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowLogoutDialog(false)}>
            Cancel
          </Button>
          <Button onClick={handleLogout} color="error" variant="contained">
            Sign Out
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default UserProfile;
