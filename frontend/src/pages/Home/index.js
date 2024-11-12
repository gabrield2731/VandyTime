import React from 'react';
import './styles.css';
import { useAuth } from "../../stores/firebase";

const Home = () => {
  const user = useAuth();

  return (
    <div className="home">
      <div className="home-container">
      <div className="home-header">
        <h1 className="home-title">Welcome to VandyTime!</h1>
        {user && <p className="user-greeting">Hello {user.email}!</p>}
      </div>

      <div className="intro-section">
        <p className="intro-text">This platform allows you to:</p>
        <ul className="features-list">
          <div className="features-text">
            <li>Input your grades and keep track of them.</li>
            <li>View the grade distributions for various courses.</li>
            <li>Compare your performance with peers.</li>
          </div>
        </ul>
      </div>

      <div className="button-section">
        <a href="/grades" className="explore-grades-btn">Explore Grades</a>
      </div>

      <div className="disclaimer-footer">
        <p className="disclaimer-text">
          Disclaimer: By entering your grades, you agree to share your data anonymously with the public. No identifying information will be shown. Developers will have access to this information solely for technical support and maintenance purposes, following strict data handling practices. Please only submit data you’re comfortable sharing under these conditions.
        </p>
      </div>
    </div>
  );
};

export default Home;
