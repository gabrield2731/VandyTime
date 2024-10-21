// src/components/SignIn.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../firebase/index";
import "./index.css";

const SignIn = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSignIn = async (e) => {
    e.preventDefault(); // Prevent page reload

    try {
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );
      console.log("User signed in:", userCredential.user);
      navigate("/");
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="signin-container">
      <div className="signin-box">
        <h2>VandyTime Login</h2>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleSignIn} className="signin-form">
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="signin-button">
            Login
          </button>
        </form>

        <div className="signup">
          <p>Don't have an account?</p>
          <a href="/signup">Sign up</a>
        </div>
        <div className="signup">
          <p>Don't want an account?</p>
          <a href="/">View Home</a>
        </div>
      </div>
    </div>
  );
};

export default SignIn;
