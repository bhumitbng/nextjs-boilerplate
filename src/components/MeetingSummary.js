import React, { useState } from 'react';
import { TextField, Button, Typography, Paper, List, ListItem, ListItemText, CircularProgress, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  paper: {
    padding: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    '& > *': {
      marginBottom: theme.spacing(2),
    },
  },
}));

const MeetingSummary = () => {
  const classes = useStyles();
  const [meetingText, setMeetingText] = useState('');
  const [summary, setSummary] = useState('');
  const [keyPoints, setKeyPoints] = useState([]);
  const [actionItems, setActionItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSummarize = () => {
    setLoading(true);
    fetch('http://localhost:5000/api/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: meetingText }),
    })
      .then(response => response.json())
      .then(data => {
        setSummary(data.summary);
        setKeyPoints(data.key_points);
        setActionItems(data.action_items);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error summarizing meeting:', error);
        setLoading(false);
      });
  };

  return (
    <div className={classes.root}>
      <Paper className={classes.paper}>
        <form className={classes.form} onSubmit={(e) => e.preventDefault()}>
          <TextField
            multiline
            rows={4}
            variant="outlined"
            fullWidth
            value={meetingText}
            onChange={(e) => setMeetingText(e.target.value)}
            placeholder="Enter meeting text here"
          />
          <Button onClick={handleSummarize} variant="contained" color="primary" disabled={loading}>
            {loading ? <CircularProgress size={24} /> : 'Summarize'}
          </Button>
        </form>
      </Paper>
      {summary && (
        <Paper className={classes.paper}>
          <Typography variant="h6" gutterBottom>Summary</Typography>
          <Typography>{summary}</Typography>
        </Paper>
      )}
      {keyPoints.length > 0 && (
        <Paper className={classes.paper}>
          <Typography variant="h6" gutterBottom>Key Points</Typography>
          <List>
            {keyPoints.map((point, index) => (
              <ListItem key={index}>
                <ListItemText primary={point} />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
      {actionItems.length > 0 && (
        <Paper className={classes.paper}>
          <Typography variant="h6" gutterBottom>Action Items</Typography>
          <List>
            {actionItems.map((item, index) => (
              <ListItem key={index}>
                <ListItemText primary={item} />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </div>
  );
};

export default MeetingSummary;