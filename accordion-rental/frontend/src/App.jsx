import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Button } from '@chakra-ui/react'; // Importing Chakra Button
import AccordionList from './components/AccordionList';
import AdminDashboard from './components/AdminDashboard';
import LoginForm from './components/LoginForm';
import Logout from './components/Logout';
import Navbar from './components/Navbar';
import RegisterForm from './components/RegisterForm';
import Profile from './components/ProfileForm';

function App() {
  const [loggedInUser, setLoggedInUser] = useState(null);

  useEffect(() => {
    const username = localStorage.getItem('username');
    if (username) {
      setLoggedInUser(username);
    }
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setLoggedInUser(null);
  };

  return (
    <Router>
      {/* Use your Chakra Button component */}
      <Button colorScheme="teal" onClick={handleLogout}>
        Logout
      </Button>
      <Routes>
        <Route path="/" element={<AccordionList />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </Router>
  );
}

export default App;
