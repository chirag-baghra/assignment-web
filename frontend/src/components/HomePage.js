import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <Container maxWidth="md" sx={{ textAlign: 'center', marginTop: '50px' }}>
      <Box sx={{ marginBottom: 4 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to User Management
        </Typography>
        <Typography variant="h5" component="p" color="textSecondary">
          Manage your users effectively. You can add new users and view the list of all users.
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 4 }}>
        <Button
          variant="contained"
          color="primary"
          size="large"
          component={Link}
          to="/add-user"
          sx={{ padding: '10px 20px' }}
        >
          Add User
        </Button>

        <Button
          variant="outlined"
          color="primary"
          size="large"
          component={Link}
          to="/user-list"
          sx={{ padding: '10px 20px' }}
        >
          View Users
        </Button>
      </Box>
    </Container>
  );
};

export default HomePage;
