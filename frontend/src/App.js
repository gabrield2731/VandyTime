import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./stores/firebase"; // AuthProvider to wrap the app

import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import Home from "./pages/Home";
import Grades from "./pages/Grades";
import Navbar from "./pages/NavBar";
import Courses from "./pages/Courses";
import Input from "./pages/Input";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/grades" element={<Grades />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/input" element={<Input />} />
          <Route path="/login" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
