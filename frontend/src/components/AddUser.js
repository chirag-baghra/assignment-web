import React, { useState } from 'react';
import { TextField, Button, FormControl, InputLabel, Select, MenuItem, Box, Typography } from '@mui/material';
import axios from 'axios';

const baseURL = process.env.REACT_APP_BASE_URL;
const AddUser = () => {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [sex, setSex] = useState('Male');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !age || !sex) return;

    try {
      await axios.post(`${baseURL}/api/add-user`, {
        name,
        age: parseInt(age),
        sex,
      });
      setName('');
      setAge('');
      setSex('Male');  // Reset form fields after successful submission
    } catch (error) {
      console.error('Error adding user:', error);
    }
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>Add New User</Typography>
      <Box
        component="form"
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
          maxWidth: '400px',
          margin: '20px auto',
          padding: 2,
          boxShadow: 3,
        }}
        onSubmit={handleSubmit}
      >
        <TextField
          label="Name"
          variant="outlined"
          value={name}
          onChange={(e) => setName(e.target.value)}
          fullWidth
          required
        />
        <TextField
          label="Age"
          type="number"
          variant="outlined"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          fullWidth
          required
        />
        <FormControl fullWidth>
          <InputLabel>Sex</InputLabel>
          <Select
            value={sex}
            onChange={(e) => setSex(e.target.value)}
            label="Sex"
          >
            <MenuItem value="Male">Male</MenuItem>
            <MenuItem value="Female">Female</MenuItem>
            <MenuItem value="Other">Other</MenuItem>
          </Select>
        </FormControl>
        <Button type="submit" variant="contained" color="primary" fullWidth>
          Add User
        </Button>
      </Box>
    </Box>
  );
};

export default AddUser;
