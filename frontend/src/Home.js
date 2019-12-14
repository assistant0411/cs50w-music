import React from 'react';
import Album from './Album';
import Navbar from './Navbar';

const Home = ({ isAuth, setIsAuth }) => {
  return (
    <>
      <Navbar isAuth={isAuth} setIsAuth={setIsAuth}/>
      <Album />
    </>
  );
};

export default Home;
