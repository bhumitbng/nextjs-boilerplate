import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { ThemeProvider, createMuiTheme, CssBaseline } from '@material-ui/core';
import Header from './components/Header';
import ManagerDashboard from './components/ManagerDashboard';
import EmployeeDashboard from './components/EmployeeDashboard';
import MeetingSummary from './components/MeetingSummary';

const theme = createMuiTheme({
  palette: {
    type: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Header />
        <Switch>
          <Route exact path="/" component={ManagerDashboard} />
          <Route path="/dashboard" component={ManagerDashboard} />
          <Route path="/employee/:id" component={EmployeeDashboard} />
          <Route path="/meetings" component={MeetingSummary} />
        </Switch>
      </Router>
    </ThemeProvider>
  );
}

export default App;