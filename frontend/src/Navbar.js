import React from 'react';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import styles from './Navbar.css';
import CreateMenu from './CreateMenu';
import MobileMenu from './MobileMenu';
import SearchBar from './SearchBar'; 


export default function Navbar({ isAuth, setIsAuth }) {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          {isAuth && <CreateMenu />}
          <Link href="/" underline="none" color="inherit" variant="h6">
            <Typography
              variant="h6"
              noWrap
              component="div"
              sx={{ display: { xs: 'none', sm: 'block' } }}
            >
              CS50wMusic
            </Typography>
          </Link>
          <SearchBar />
          <Box sx={{ flexGrow: 1 }} />
          {isAuth && <MobileMenu setIsAuth={setIsAuth}/>}
          {!isAuth && <Link href="/login" variant="body2" id="custom_link">Sign in</Link>}
        </Toolbar>
      </AppBar>
    </Box>
  );
}
