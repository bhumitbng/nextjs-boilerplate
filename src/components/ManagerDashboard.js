import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, CircularProgress, makeStyles } from '@material-ui/core';
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

const ManagerDashboard = () => {
  const classes = useStyles();
  const [teamPerformance, setTeamPerformance] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/team/performance')
      .then(response => response.json())
      .then(data => {
        setTeamPerformance(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching team performance:', error);
        setLoading(false);
      });
  }, []);

  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <Typography variant="h5" gutterBottom>Team Performance Overview</Typography>
            {loading ? (
              <CircularProgress />
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={teamPerformance}>
                  <XAxis dataKey="date" />
                  <YAxis />
                  <CartesianGrid strokeDasharray="3 3" />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="performance" stroke="#8884d8" activeDot={{ r: 8 }} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper className={classes.paper}>
            <Typography variant="h6" gutterBottom>Key Metrics</Typography>
            {/* Add key metrics here */}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper className={classes.paper}>
            <Typography variant="h6" gutterBottom>Recent Activities</Typography>
            {/* Add recent activities here */}
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
};

export default ManagerDashboard;