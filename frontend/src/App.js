
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignIn from './SignIn';
import SignUp from './SignUp';
import Home from './Home';
import PlaySong from './PlaySong'


const App = () => {
  const [isAuth, setIsAuth] = useState(!!localStorage.getItem('token'));

  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home isAuth={isAuth} setIsAuth={setIsAuth}/>}/>
        <Route path='/login' element={<SignIn setIsAuth={setIsAuth}/>}/>
        <Route path='/register' element={<SignUp setIsAuth={setIsAuth}/>}/>
        <Route path='/songs/:id' element={<PlaySong />} />
      </Routes>
    </Router>
  );
};

export default App;