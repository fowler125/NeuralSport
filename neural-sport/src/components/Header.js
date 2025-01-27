import React from 'react';
import { Link } from 'react-router-dom';
import Slideshow from './Slideshow';


function Header() {

  return (
    <header>
      <div className="left">
        <h1>Play Ball! <span>NeuralSport</span></h1>
        <p>The future of sports, made by sportsAI.</p>
        <a href="#">
          <i className='bx bx-baseball'></i>
          <span>Baseball</span>
        </a>
        <Link to="/basketball">
          <i className='bx bx-basketball'></i>
          <span>Basketball</span>
        </Link>
        <Link to="/football">
          <i className='bx bx-ball'></i>
          <span>Football</span>
        </Link>
      </div>
      <Slideshow />
      
    </header>
  );
}

export default Header;