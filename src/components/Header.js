import React from 'react';
import { AppBar, Toolbar, Typography, Button, makeStyles } from '@material-ui/core';
import { Link } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  title: {
    flexGrow: 1,
  },
  link: {
    color: 'white',
    textDecoration: 'none',
  },
}));

const Header = () => {
  const classes = useStyles();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" className={classes.title}>
          AI-Driven Manager
        </Typography>
        <Button color="inherit" component={Link} to="/dashboard">Dashboard</Button>
        <Button color="inherit" component={Link} to="/meetings">Meetings</Button>
        <Button color="inherit" component={Link} to="/employees">Employees</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;