import React, { useState } from 'react';
import { FormattedMessage } from 'react-intl';
import axios from 'axios';

export const VideoEditing = () => {
  const [file, setFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState(false);
  const [processedVideoUrl, setProcessedVideoUrl] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) return;

    setProcessing(true);
    const formData = new FormData();
    formData.append('video', file);

    try {
      const response = await axios.post('/api/video-editing/process/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setProcessedVideoUrl(response.data.video_url);
    } catch (error) {
      console.error('Error processing video:', error);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div>
      <h1>
        <FormattedMessage defaultMessage="Video Editing" id="videoEditing.title" />
      </h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button type="submit" disabled={!file || processing}>
          <FormattedMessage defaultMessage="Process Video" id="videoEditing.processButton" />
        </button>
      </form>
      {processing && <p>Processing video...</p>}
      {processedVideoUrl && (
        <div>
          <h2>Processed Video</h2>
          <video src={processedVideoUrl} controls width="640" height="360" />
        </div>
      )}
    </div>
  );
};