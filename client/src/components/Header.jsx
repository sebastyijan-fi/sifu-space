import React from 'react';
import { Link } from 'react-router-dom';
import './Header.scss';

function Header() {
  return (
    <header className="header">
      <div className="container">
        <Link to="/" className="logo">Sifu</Link> {/* Link to main page */}
        <nav className="nav">
          <ul className="nav-list">
            <li className="nav-item">
              <Link to="/login" className="nav-link">Login</Link>
            </li>
            <li className="nav-item">
              <Link to="/register" className="nav-link">Register</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;
