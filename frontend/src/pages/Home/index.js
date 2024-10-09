import React from "react";
import { useAuth } from "../../stores/firebase"; // Make sure this path is correct

const Home = () => {
  const user = useAuth(); // This will give you the current Firebase user

  return (
    <div>
      <h1>Home</h1>
      {user ? <p>Welcome, {user.email}</p> : <p>Please sign in</p>}
    </div>
  );
};

export default Home;
