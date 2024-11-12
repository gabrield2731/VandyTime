import React from "react";
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

  const handleLogout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  return (
    <>
      {!navBarRoutes.includes(location.pathname) && (
        <nav className="navbar">
          <div className="navbar-container">
            <div className="navbar-logo">
            <a href="/"><img src={logo} alt="VandyLogo" className="logo-image" /></a>
            </div>

            <ul className="nav-links">
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
            </ul>

            <div className="nav-login">
              {user ? (
                <button onClick={handleLogout} className="login-btn">
                  Log Out
                </button>
              ) : (
                <a href="/login" className="login-btn">
                  Log In
                </a>
              )}
            </div>
          </div>
        </nav>
      )}
    </>
  );
};

export default Navbar;
