// src/components/SubmitValues.js
import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Typography } from '@mui/material';

const SubmitValues = () => {
  const [value1, setValue1] = useState('');
  const [value2, setValue2] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/submit', {
        value1,
        value2,
      });
      setResponseMessage(response.data.message);
    } catch (error) {
      console.error(error);
      setResponseMessage('Error submitting values');
    }
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Submit Values
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Value 1"
          value={value1}
          onChange={(e) => setValue1(e.target.value)}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Value 2"
          value={value2}
          onChange={(e) => setValue2(e.target.value)}
          required
          fullWidth
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary">
          Submit
        </Button>
      </form>
      {responseMessage && (
        <Typography variant="body1" style={{ marginTop: '10px' }}>
          {responseMessage}
        </Typography>
      )}
    </div>
  );
};

export default SubmitValues;
