import React, { useState } from 'react';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';
import MoreIcon from '@mui/icons-material/MoreVert';
import NotificationsMenu from './NotificationsMenu';
import AccountMenu from './AccountMenu';
import Box from '@mui/material/Box';


export default function MobileMenu({ setIsAuth }) {
  const [mobileMoreAnchorEl, setMobileMoreAnchorEl] = useState(null);
  const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);

  const handleMobileMenuOpen = (event) => {
    setMobileMoreAnchorEl(event.currentTarget);
  };

  const handleMobileMenuClose = () => {
    setMobileMoreAnchorEl(null);
  };

  const mobileMenuId = 'primary-search-account-menu-mobile';

  return (
    <>
      {/* For medium to large screens display Notifications and Account menus */}
      <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
        <NotificationsMenu/>
        <AccountMenu setIsAuth={setIsAuth}/>
      </Box>
      {/* For small screens, display a menu with more icon that contains Notifications and Account */}
      <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
        <IconButton
          size="large"
          aria-label="show more"
          aria-controls={mobileMenuId}
          aria-haspopup="true"
          onClick={handleMobileMenuOpen}
          color="inherit"
        >
          <MoreIcon />
        </IconButton>

        <Menu
          anchorEl={mobileMoreAnchorEl}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          id={mobileMenuId}
          keepMounted
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          open={isMobileMenuOpen}
          onClose={handleMobileMenuClose}
        >
          <MenuItem>
            <NotificationsMenu/>
            <p>Notifications</p>
          </MenuItem>
          <MenuItem>
            <AccountMenu setIsAuth={setIsAuth}/>
            <p>Account</p>
          </MenuItem>
        </Menu>
      </Box>
    </>
  );
}
