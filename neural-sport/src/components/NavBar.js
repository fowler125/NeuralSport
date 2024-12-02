import React from 'react';
import { Link } from 'react-router-dom';

function NavBar() {
  return (
    <nav>
      <a href="#" className="logo">Neural Sport</a>
      <div className="links">
        <Link to="/">Home</Link>
        <a href="#">Features</a>
        <a href="#">Sports</a>
        <a href="#">About Us</a>
      </div>
      <div className="login">
        <button className="signup">Get Started</button>
        <button>Login</button>
      </div>
    </nav>
  );
}

export default NavBar;