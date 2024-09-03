import React, { useState } from 'react';
import { TextField, Button, Typography } from '@material-ui/core';

const MeetingSummary = () => {
  const [meetingText, setMeetingText] = useState('');
  const [summary, setSummary] = useState('');

  const handleSummarize = () => {
    fetch('http://localhost:5000/api/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: meetingText }),
    })
      .then(response => response.json())
      .then(data => setSummary(data.summary))
      .catch(error => console.error('Error summarizing meeting:', error));
  };

  return (
    <div>
      <TextField
        multiline
        rows={4}
        variant="outlined"
        fullWidth
        value={meetingText}
        onChange={(e) => setMeetingText(e.target.value)}
        placeholder="Enter meeting text here"
      />
      <Button onClick={handleSummarize} variant="contained" color="primary">
        Summarize
      </Button>
      {summary && (
        <Typography variant="body1">
          <strong>Summary:</strong> {summary}
        </Typography>
      )}
    </div>
  );
};

export default MeetingSummary;