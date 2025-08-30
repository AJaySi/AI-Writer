import { Box, Card, Chip } from '@mui/material';
import { styled } from '@mui/material/styles';

// Shared styled components for dashboard components
export const DashboardContainer = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  background:
    'radial-gradient(1200px 600px at 10% -10%, rgba(255,255,255,0.08) 0%, transparent 60%),\
     radial-gradient(900px 500px at 110% 10%, rgba(255,255,255,0.06) 0%, transparent 60%),\
     linear-gradient(135deg, #0f1226 0%, #1b1e3b 35%, #2a2f59 70%, #3a3f7a 100%)',
  padding: theme.spacing(5, 4, 6, 4),
  position: 'relative',
  color: 'rgba(255,255,255,0.9)',
  '&::before': {
    content: '""',
    position: 'absolute',
    inset: 0,
    background:
      'url("data:image/svg+xml,%3Csvg width=\'80\' height=\'80\' viewBox=\'0 0 80 80\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.03\'%3E%3Ccircle cx=\'40\' cy=\'40\' r=\'2\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
    pointerEvents: 'none',
  },
  '&::after': {
    content: '""',
    position: 'absolute',
    top: '50%',
    left: '50%',
    width: '900px',
    height: '900px',
    background: 'radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 65%)',
    transform: 'translate(-50%, -50%)',
    filter: 'blur(20px)',
    pointerEvents: 'none',
    zIndex: 0,
  },
}));

export const GlassCard = styled(Card)(({ theme }) => ({
  background: 'linear-gradient(180deg, rgba(255,255,255,0.14) 0%, rgba(255,255,255,0.08) 100%)',
  backdropFilter: 'blur(22px)',
  WebkitBackdropFilter: 'blur(22px)',
  border: '1px solid rgba(255, 255, 255, 0.16)',
  borderRadius: theme.spacing(3.5),
  boxShadow:
    '0 18px 50px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255,255,255,0.25), inset 0 -1px 0 rgba(0,0,0,0.1)',
  transition: 'transform 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.35s',
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: '-120%',
    width: '100%',
    height: '100%',
    background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.10), transparent)',
    transition: 'left 0.6s ease-in-out',
  },
  '&:hover': {
    transform: 'translateY(-10px) scale(1.015)',
    boxShadow: '0 30px 80px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255,255,255,0.3)',
    border: '1px solid rgba(255, 255, 255, 0.22)',
    '&::before': {
      left: '120%',
    },
  },
}));

export const ShimmerHeader = styled(Box)(({ theme }) => ({
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: '-100%',
    width: '100%',
    height: '3px',
    background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent)',
    animation: 'shimmer 3s infinite',
  },
  '@keyframes shimmer': {
    '0%': { left: '-100%' },
    '100%': { left: '100%' },
  },
}));

export const SearchContainer = styled(Box)(({ theme }) => ({
  background: 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(20px)',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  borderRadius: theme.spacing(3),
  padding: theme.spacing(2),
  marginBottom: theme.spacing(4),
  transition: 'all 0.3s ease',
  '&:hover': {
    background: 'rgba(255, 255, 255, 0.15)',
    border: '1px solid rgba(255, 255, 255, 0.3)',
  },
}));

export const CategoryChip = styled(Chip, {
  shouldForwardProp: (prop) => prop !== 'active',
})<{ active?: boolean }>(({ theme, active }) => ({
  background: active ? 'rgba(255, 255, 255, 0.25)' : 'rgba(255, 255, 255, 0.1)',
  color: 'white',
  fontWeight: 600,
  fontSize: '0.9rem',
  padding: theme.spacing(1, 2),
  border: `1px solid ${active ? 'rgba(255, 255, 255, 0.4)' : 'rgba(255, 255, 255, 0.2)'}`,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  '&:hover': {
    background: 'rgba(255, 255, 255, 0.25)',
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
  },
  '& .MuiChip-label': {
    padding: theme.spacing(0.5, 1),
  },
}));

export const EnhancedGlassCard = styled(GlassCard)(({ theme }) => ({
  background: 'rgba(255, 255, 255, 0.12)',
  border: '2px solid rgba(255, 255, 255, 0.2)',
  '&:hover': {
    border: '2px solid rgba(255, 255, 255, 0.3)',
  },
}));

export const AIInsightsPanel = styled(GlassCard)(({ theme }) => ({
  background: 'rgba(255, 255, 255, 0.1)',
  border: '1px solid rgba(255, 255, 255, 0.15)',
  position: 'relative',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '3px',
    background: 'linear-gradient(90deg, #667eea, #764ba2, #f093fb)',
    borderRadius: '3px 3px 0 0',
  },
})); 