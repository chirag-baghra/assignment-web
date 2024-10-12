import React, { useState } from 'react';
import axios from 'axios';
import { AppBar, Toolbar, Button, Container, Typography, TextField, Box, Snackbar } from '@mui/material';
import MuiAlert from '@mui/material/Alert';

const Alert = React.forwardRef((props, ref) => <MuiAlert elevation={6} ref={ref} {...props} />);

function App() {
  const [value1, setValue1] = useState('');
  const [value2, setValue2] = useState('');
  const [response, setResponse] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post('http://localhost:5000/submit', {
        value1,
        value2,
      });

      setResponse(res.data.message);
      setOpenSnackbar(true);
    } catch (err) {
      console.error(err);
      setResponse('Error submitting values');
      setOpenSnackbar(true);
    }
  };

  const handleCloseSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSnackbar(false);
  };

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Submit Values
          </Typography>
        </Toolbar>
      </AppBar>
      <Container sx={{ marginTop: 4 }}>
        <Box 
          component="form" 
          onSubmit={handleSubmit} 
          sx={{
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            backgroundColor: '#f5f5f5',
            padding: 3,
            borderRadius: 2,
            boxShadow: 1
          }}
        >
          <TextField
            label="Value 1"
            variant="outlined"
            value={value1}
            onChange={(e) => setValue1(e.target.value)}
            required
          />
          <TextField
            label="Value 2"
            variant="outlined"
            value={value2}
            onChange={(e) => setValue2(e.target.value)}
            required
          />
          <Button variant="contained" color="primary" type="submit">
            Submit
          </Button>
        </Box>

        <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
          <Alert onClose={handleCloseSnackbar} severity={typeof response === 'string' && response.includes('Error') ? 'error' : 'success'}>
            {response}
          </Alert>
        </Snackbar>
      </Container>
    </div>
  );
}

export default App;
