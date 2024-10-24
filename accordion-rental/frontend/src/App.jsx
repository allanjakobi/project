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
  return (
    <Router>
      <Navbar /> 
      <Routes>
        {/* Use 'element' instead of 'component', and pass the components as JSX elements */}
        <Route path="/" element={<AccordionList />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/profile" element={<Profile />} /> {/* Define the profile route */}
        <Route path="/login" element={<LoginForm />} />
        <Route path="/logout" element={<Logout />} />
        
      </Routes>
    </Router>
  );
}

export default App;
