import React, { useEffect, useState, useRef } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axiosInstance from './axiosInstance';
import Link from '@mui/material/Link';
import InfiniteScroll from 'react-infinite-scroll-component';

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
            <Typography
              component="h1"
              variant="h2"
              align="center"
              color="text.primary"
              gutterBottom
            >
              Album layout
            </Typography>
            <Typography variant="h5" align="center" color="text.secondary" paragraph>
              Something short and leading about the collection below—its contents,
              the creator, etc.
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
                  <Link href={`/songs/${song.id}`} underline="none">
                    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                      <CardMedia
                        component="div"
                        sx={{
                          // 16:9
                          pt: '56.25%',
                        }}
                        image={song.cover_image || 'https://wallpapers.com/images/featured/music-notes-zpmz2slc377qu3wd.jpg'}
                      />
                      <CardContent sx={{ flexGrow: 1 }}>
                        <Typography gutterBottom variant="h5" component="h2">
                          {song.title}
                        </Typography>
                        <Typography>
                          {Object.entries(song.artists_usernames).map(([artistId, username], index, array) => (
                            <React.Fragment key={artistId}>
                              <Link href={`/users/${artistId}/`} variant="body2">
                                {username}
                              </Link>
                              {index < array.length - 1 && ', '}
                            </React.Fragment>
                          ))}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Link>
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
