import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, List, ListItem, ListItemText } from '@material-ui/core';

const EmployeeDashboard = ({ employeeId }) => {
  const [performanceData, setPerformanceData] = useState(null);
  const [goals, setGoals] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5000/api/employee/${employeeId}`)
      .then(response => response.json())
      .then(data => {
        setPerformanceData(data.performanceData);
        setGoals(data.goals);
      })
      .catch(error => console.error('Error fetching employee data:', error));
  }, [employeeId]);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Paper>
          <Typography variant="h6">Performance Overview</Typography>
          {performanceData && (
            <>
              <Typography>Score: {performanceData.score}</Typography>
              <Typography>Tasks Completed: {performanceData.tasksCompleted}</Typography>
            </>
          )}
        </Paper>
      </Grid>
      <Grid item xs={12} md={6}>
        <Paper>
          <Typography variant="h6">Goals</Typography>
          <List>
            {goals.map((goal, index) => (
              <ListItem key={index}>
                <ListItemText primary={goal} />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default EmployeeDashboard;