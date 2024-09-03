import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const ManagerDashboard = () => {
  const [teamPerformance, setTeamPerformance] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/team/performance')
      .then(response => response.json())
      .then(data => setTeamPerformance(data))
      .catch(error => console.error('Error fetching team performance:', error));
  }, []);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper>
          <Typography variant="h5">Team Performance</Typography>
          <LineChart width={600} height={300} data={teamPerformance}>
            <XAxis dataKey="date" />
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="performance" stroke="#8884d8" />
          </LineChart>
        </Paper>
      </Grid>
      {/* Add more dashboard components here */}
    </Grid>
  );
};

export default ManagerDashboard;