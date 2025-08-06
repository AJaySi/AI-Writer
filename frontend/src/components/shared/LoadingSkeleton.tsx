import React from 'react';
import { Box, Container, Skeleton, Grid } from '@mui/material';
import { DashboardContainer } from './styled';
import { LoadingSkeletonProps } from './types';

const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ 
  itemCount = 8, 
  itemHeight = 200, 
  headerHeight = 80 
}) => {
  return (
    <DashboardContainer>
      <Container maxWidth="xl">
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Skeleton variant="rectangular" height={headerHeight} sx={{ borderRadius: 2 }} />
          <Grid container spacing={3}>
            {Array.from({ length: itemCount }).map((_, index) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                <Skeleton variant="rectangular" height={itemHeight} sx={{ borderRadius: 2 }} />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </DashboardContainer>
  );
};

export default LoadingSkeleton; 