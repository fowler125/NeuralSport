import React from 'react';

function Footer() {
  return (
    <footer>
      <h3>NeuralSport</h3>
      <div className="right">
        <div className="links">
          <a href="#">Privacy Policy</a>
          <a href="#">Cooperation</a>
          <a href="#">Sponsorship</a>
          <a href="#">Contact Us</a>
        </div>
        <div className="social">
          <i className='bx bxl-instagram'></i>
          <i className='bx bxl-facebook-square'></i>
          <i className='bx bxl-github'></i>
        </div>
        <p>Copyright © 2024 NeuralSport, All Rights Reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;