import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosInstance from './axiosInstance';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Link from '@mui/material/Link';

const defaultTheme = createTheme();

export default function PlaySong() {
  const { id } = useParams();
  const [songDetails, setSongDetails] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSongDetails = async () => {
      setError(null);

      try {
        const response = await axiosInstance.get(`/songs/${id}/`);
        setSongDetails(response.data);
      } catch (error) {
        setError(error);
      }
    };

    fetchSongDetails();
  }, [id]);

  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      <main>
        <Container sx={{ py: 8 }} maxWidth="xl">
          {error && <p>Error loading song details. Error: {error.message}.</p>}
          {Object.keys(songDetails).length > 0 && (
            <div>
              <img src={songDetails.cover_image} alt="Song Cover" style={{ maxWidth: '50%' }} />
              <Typography variant="h6" color="text.primary" paragraph>
                {songDetails.title}
                {songDetails.release_date}
                {songDetails.genre}
                {songDetails.album}
              </Typography>
              {Object.entries(songDetails.artists_usernames).map(([artistId, username], index, array) => (
                <React.Fragment key={artistId}>
                  <Link href={`/users/${artistId}/`} variant="body2">
                    {username}
                  </Link>
                  {index < array.length - 1 && ', '}
                </React.Fragment>
              ))}
              <audio controls>
                <source src={songDetails.audio_file} type="audio/mp3" />
                Your browser does not support the audio tag.
              </audio>
            </div>
          )}
        </Container>
      </main>
    </ThemeProvider>
  );
};