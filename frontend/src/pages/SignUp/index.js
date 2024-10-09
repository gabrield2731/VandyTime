import React, { useState } from "react";
import {
  createUserWithEmailAndPassword,
  sendEmailVerification,
} from "firebase/auth";
import { auth } from "../../firebase/index";
import "./index.css"; // Assuming you're using the same index.css for styles

const SignUp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSignUp = async (e) => {
    setError("");
    setMessage("");
    e.preventDefault();

    // Basic password confirmation check
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (email.split("@")[1] !== "vanderbilt.edu") {
      setError("Please sign up with your Vanderbilt email");
      return;
    }

    try {
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
      );
      const user = userCredential.user;

      // Send email verification
      await sendEmailVerification(user);
      setError("");
      setMessage("Verification email sent. Please check your inbox.");
    } catch (error) {
      setMessage("");
      setError(error.message);
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <h2>Create Your VandyTime Account</h2>
        {error && <p className="error-message">{error}</p>}
        {message && <p className="success-message">{message}</p>}
        <form onSubmit={handleSignUp} className="signup-form">
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
          <div className="input-group">
            <label>Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="signup-button">
            Sign Up
          </button>
        </form>
        <div className="signup">
          <p>Already have an account?</p>
          <a href="/login">Sign in</a>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
