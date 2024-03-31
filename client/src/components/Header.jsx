import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getAuth, onAuthStateChanged, signOut } from "firebase/auth";
import './Header.scss';

function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const auth = getAuth();
    // Check if the user is logged in
    onAuthStateChanged(auth, (user) => {
      setIsLoggedIn(!!user); // Simplified isLoggedIn state update
    });
  }, []);

  const handleLogout = () => {
    const auth = getAuth();
    signOut(auth)
      .then(() => {
        setIsLoggedIn(false);
        // Redirect or show success message
      })
      .catch((error) => {
        console.error('Logout error:', error);
      });
  };

  return (
    <header className="header">
      <div className="container">
        <Link to="/" className="logo">Sifu</Link> {/* Link to main page */}
        <nav className="nav">
          <ul className="nav-list">
            {isLoggedIn ? (
              <>
                <li className="nav-item">
                  <Link to="/upload" className="nav-link">Upload</Link> {/* Changed link text to "Upload" */}
                </li>
                <li className="nav-item">
                  <Link to="/portfolio" className="nav-link">Portfolio</Link> {/* Link to Portfolio */}
                </li>
                <li className="nav-item">
                  <button onClick={handleLogout} className="nav-link">Logout</button>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item">
                  <Link to="/login" className="nav-link">Login</Link>
                </li>
                <li className="nav-item">
                  <Link to="/register" className="nav-link">Register</Link>
                </li>
              </>
            )}
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;
