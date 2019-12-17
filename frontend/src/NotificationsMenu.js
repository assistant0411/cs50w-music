import React, { useState } from 'react';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';
import Badge from '@mui/material/Badge';
import NotificationsIcon from '@mui/icons-material/Notifications';


export default function NotificationsMenu({showText=false}) {
  const notificationsMenuId = 'primary-search-notifications-menu';

  const [notificationsAnchorEl, setNotificationsAnchorEl] = useState(null);
  const isNotificationsMenuOpen = Boolean(notificationsAnchorEl);

  const handleNotificationsMenuOpen = (event) => {
    setNotificationsAnchorEl(event.currentTarget);
  };

  const handleNotificationsMenuClose = () => {
    setNotificationsAnchorEl(null);
  };

  return (
    <>
      <IconButton
        size="large"
        aria-label="show 2 new notifications"
        color="inherit"
        onClick={handleNotificationsMenuOpen}
      >
      <Badge badgeContent={2} color="error">
        <NotificationsIcon />
      </Badge>
      </IconButton>

      <Menu
        anchorEl={notificationsAnchorEl}
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        id={notificationsMenuId}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={isNotificationsMenuOpen}
        onClose={handleNotificationsMenuClose}
      >
        <MenuItem onClick={handleNotificationsMenuClose}>Notification 1</MenuItem>
        <MenuItem onClick={handleNotificationsMenuClose}>Notification 2</MenuItem>
      </Menu>
    </>
  );
}
