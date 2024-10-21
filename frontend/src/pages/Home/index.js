import React from 'react';
import './styles.css'; // Add some styles as needed
import { useAuth } from "../../stores/firebase"; // Make sure this path is correct

const Home = () => {
  const user = useAuth(); // This will give you the current Firebase user

  return (
    <div className="home">
      <div className="home-container">
        <h1 className="home-title">Welcome to VandyTime</h1>
        {user && <p className="user-greeting">Welcome, {user.email}!</p>}

        {/* Introduction section */}
        <div className="intro-section">
          <p className="intro-text">This platform allows you to:</p>
          <ul className="features-list">
            <li>Input your grades and keep track of them.</li>
            <li>View the grade distributions for various courses.</li>
            <li>Compare your performance with peers.</li>
          </ul>
        </div>

        {/* Buttons to get started */}
        <div className="button-section">
          <a href="/grades" className="get-started-btn">Get Started</a>
        </div>
      </div>
    </div>
  );
};

export default Home;
