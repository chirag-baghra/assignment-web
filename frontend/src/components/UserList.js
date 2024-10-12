import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Box } from '@mui/material';

const baseURL = process.env.REACT_APP_BASE_URL;

const UserList= () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch(`${baseURL}/api/users`);
        const data = await response.json();
         const transformedData = data.map(user => ({
                    name: user[0],
                    age: user[1],
                    sex: user[2]
                }));
        setUsers(transformedData);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>User List</Typography>
      <TableContainer component={Paper} sx={{ margin: '20px auto', maxWidth: '800px' }}>
        <Table aria-label="users table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell align="right">Age</TableCell>
              <TableCell align="right">Sex</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user, index) => (
              <TableRow key={index}>
                <TableCell component="th" scope="row">{user.name}</TableCell>
                <TableCell align="right">{user.age}</TableCell>
                <TableCell align="right">{user.sex}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default UserList;
