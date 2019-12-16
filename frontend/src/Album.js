import React, { useEffect, useState, useRef } from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axiosInstance from './axiosInstance';
import InfiniteScroll from 'react-infinite-scroll-component';
import SongCard from './SongCard';


const defaultTheme = createTheme();

export default function Album() {
  const [songs, setSongs] = useState([]);
  const [error, setError] = useState(null);
  const [url, setUrl] = useState("/songs/");
  const isInitialMount = useRef(true);

  const fetchData = async () => {
    setError(null);

    try {
      const songsResponse = await axiosInstance.get(url);
      setSongs((prevSongs) => [...prevSongs, ...songsResponse.data.results]);
      setUrl(songsResponse.data.next);
    } catch (error) {
      setError(error);
    }
  };

  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
    } else {
      fetchData();
    }
  }, []);

  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      <main>
        <Box
          sx={{
            bgcolor: 'background.paper',
            pt: 8,
            pb: 6,
          }}
        >
          <Container maxWidth="sm">
            <Typography variant="h5" align="center" color="text.primary" paragraph>
              some text idk
            </Typography>
          </Container>
        </Box>
        <Container sx={{ py: 8 }} maxWidth="xl">
            <InfiniteScroll
              dataLength={songs.length}
              next={fetchData}
              hasMore={!!url}
              loader={<p>Loading...</p>}
              endMessage={<p>No more songs to load.</p>}
            >
            <Grid container spacing={4}>
              {songs.map((song) => (
                <Grid item key={song.id} xs={6} sm={4} md={3} lg={2}>
                  <SongCard song={song}/>
                </Grid>
              ))}
            </Grid>
          </InfiniteScroll>
          {error && <p>Error loading songs. Error: {error}.</p>}
        </Container>
      </main>
    </ThemeProvider>
  );
}
