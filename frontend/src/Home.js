import React from 'react';
import ReleaseCardsAlbum from './ReleaseCardsAlbum';
import Navbar from './Navbar';

const Home = ({ isAuth, setIsAuth }) => {
  return (
    <>
      <Navbar isAuth={isAuth} setIsAuth={setIsAuth}/>
      <ReleaseCardsAlbum url={"/songs/"} infiniteScroll={true}/>
    </>
  );
};

export default Home;
