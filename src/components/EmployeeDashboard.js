import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, List, ListItem, ListItemText, CircularProgress, makeStyles } from '@material-ui/core';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
  chart: {
    height: 300,
  },
}));

const EmployeeDashboard = ({ employeeId }) => {
  const classes = useStyles();
  const [performanceData, setPerformanceData] = useState(null);
  const [goals, setGoals] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`http://localhost:5000/api/employee/${employeeId}`),
      fetch(`http://localhost:5000/api/employee/predict/${employeeId}`)
    ])
      .then(([employeeRes, predictionsRes]) => Promise.all([employeeRes.json(), predictionsRes.json()]))
      .then(([employeeData, predictionsData]) => {
        setPerformanceData(employeeData.performanceData);
        setGoals(employeeData.goals);
        setPredictions(predictionsData.predictions);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching employee data:', error);
        setLoading(false);
      });
  }, [employeeId]);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper className={classes.paper}>
            <Typography variant="h6" gutterBottom>Performance Overview</Typography>
            {performanceData && (
              <>
                <Typography>Score: {performanceData.score}</Typography>
                <Typography>Tasks Completed: {performanceData.tasksCompleted}</Typography>
              </>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper className={classes.paper}>
            <Typography variant="h6" gutterBottom>Goals</Typography>
            <List>
              {goals.map((goal, index) => (
                <ListItem key={index}>
                  <ListItemText primary={goal} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <Typography variant="h6" gutterBottom>Performance Prediction</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={predictions}>
                <XAxis dataKey="date" />
                <YAxis />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="predicted_score" stroke="#82ca9d" activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
};

export default EmployeeDashboard;