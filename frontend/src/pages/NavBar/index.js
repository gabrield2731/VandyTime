import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { useAuth } from "../../stores/firebase";
import { auth } from "../../firebase/index";
import { signOut } from "firebase/auth";
import logo from "../../assets/logo.png";
import "./index.css";

const Navbar = () => {
  const user = useAuth();
  const location = useLocation();
  const navBarRoutes = ["/login", "/signup"];
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = async () => {
    try {
      console.log("logging out");
      await signOut(auth);
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <>
      {!navBarRoutes.includes(location.pathname) && (
        <nav className="navbar">
          <div className="navbar-container">
            <div className="navbar-logo">
              <a href="/">
                <img src={logo} alt="VandyLogo" className="logo-image" />
              </a>
            </div>

            <button className="hamburger-menu" onClick={toggleMenu}>
              <span></span>
              <span></span>
              <span></span>
            </button>

            <ul className={`nav-links ${isMenuOpen ? "show-menu" : ""}`}>
              <li>
                <a href="/">Home</a>
              </li>
              <li>
                <a href="/grades">Grades</a>
              </li>
              <li>
                <a href="/courses">Courses</a>
              </li>
              <li>
                <a href="/input">Input</a>
              </li>
              <li>
                <a href="/dashboard">Dashboard</a>
              </li>
              {user && (
                <li>
                  <a onClick={handleLogout} className="login-btn">
                    Log Out
                  </a>
                </li>
              )}
              {!user && (
                <li>
                  <a href="/login" className="login-btn">
                    Log In
                  </a>
                </li>
              )}
            </ul>
          </div>
        </nav>
      )}
    </>
  );
};

export default Navbar;
