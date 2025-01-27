import React from 'react';
import NavBar from './components/NavBar';
import Header from './components/Header';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Basketball from './components/Basketball';
import Football from './components/Football';
import Footer from './components/Footer';
import SportsSummary from './components/SportsSummary';
import PlayerProfile from './components/PlayerProfile';
import Stats from './components/Stats';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <Routes>
          <Route path="/" element={<>
            <Header />
            <SportsSummary />
          </>} />
          <Route path="/basketball" element={<Basketball />} />
          <Route path="/player/:playerName" element={<PlayerProfile />} />
          <Route path="/football" element={<Football />} />
          <Route path="/stats" element={<Stats />} /> 
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
