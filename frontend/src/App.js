import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignIn from './SignIn';
import Home from './Home';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/login' element={<SignIn/>}/>
      </Routes>
    </Router>
  );
};

export default App;