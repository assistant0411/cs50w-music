import React, { useState, useEffect } from 'react';
import axiosInstance from './axiosInstance';

const SongList = () => {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    axiosInstance.get('/songs/')
      .then(response => {
        setSongs(response.data.results);
      })
      .catch(error => {
        console.error('Error fetching songs:', error);
      });
  }, []);

  return (
    <div>
      <h2>Song List</h2>
      <ul>
        {songs.map(song => (
          <li key={song.id}>{song.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default SongList;
