import React, { createContext, useContext, useEffect, useState } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase/index"; // Import the Firebase auth instance

// Create the AuthContext
const AuthContext = createContext();

// AuthProvider to wrap your app and provide the user state
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });

    // Cleanup subscription on unmount
    return () => unsubscribe();
  }, []);

  return <AuthContext.Provider value={user}>{children}</AuthContext.Provider>;
};

// Hook to use the AuthContext
export const useAuth = () => {
  return useContext(AuthContext);
};
