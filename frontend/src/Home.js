import React from 'react';
import Songlist from './SongList';
import Navbar from './Navbar';

const Home = ({ isAuth, setIsAuth }) => {
  return (
    <>
      <Navbar isAuth={isAuth} setIsAuth={setIsAuth}/>
      <Songlist />
    </>
  );
};

export default Home;
