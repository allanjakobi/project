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
import ProtectedRoute from './components/ProtectedRoute'; // Import the ProtectedRoute
import RentalForm from './components/RentalForm';
import Contracts from './components/contracts';



function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      <Routes>
      <Route path="/" element={<AccordionList isLoggedIn={isLoggedIn} />} />
      <Route path="/register" element={<RegisterForm />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route 
          path="/profile" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <Profile />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/rent" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <RentalForm />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/contracts" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <Contracts />
            </ProtectedRoute>
          } 
        />
        <Route path="/login" element={<LoginForm setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/logout" element={<Logout setIsLoggedIn={setIsLoggedIn} />} />
      </Routes>
    </Router>
  );
}

export default App;
