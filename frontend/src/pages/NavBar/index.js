import React from 'react';
import { useLocation } from 'react-router-dom';
import './index.css';

const Navbar = () => {
  const location = useLocation();
  const navBarRoutes = ['/login'];

  return (
    <>
      {!navBarRoutes.includes(location.pathname) && (
        <nav className="navbar">
          <div className="navbar-container">
            <div className="navbar-logo">
              <a href="/">YourLogo</a>
            </div>

            <ul className="nav-links">
              <li><a href="/">Home</a></li>
              <li><a href="/grades">Grades</a></li>
              <li><a href="/courses">Courses</a></li>
              <li><a href="/input">Input</a></li>
            </ul>

            <div className="nav-login">
              <a href="/login" className="login-btn">Log In</a>
            </div>
          </div>
        </nav>
      )}
    </>
  );
};

export default Navbar;
