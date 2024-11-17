import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute'; // Import the ProtectedRoute
import AccordionList from './components/AccordionList';
import AdminDashboard from './components/AdminDashboard'; // Admin functionality
import LoginForm from './components/LoginForm';
import Logout from './components/Logout';
import RegisterForm from './components/RegisterForm';
import Profile from './components/ProfileForm';
import RentalForm from './components/RentalForm';
import Contracts from './components/contracts';
import Invoices from './components/invoices';
import NotFoundPage from './components/NotFoundPage'; // Optional 404 page
import AdminPage from './components/AdminPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      {/* Navbar is displayed across all routes */}
      <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<AccordionList isLoggedIn={isLoggedIn} />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/login" element={<LoginForm setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/logout" element={<Logout setIsLoggedIn={setIsLoggedIn} />} />

        {/* Protected Routes */}
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
        <Route 
          path="/invoices" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <Invoices />
            </ProtectedRoute>
          } 
        />
        
        {/* Admin Route (Protected for staff only) */}
        <Route 
          path="/admin" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} isAdmin={true}>
              <AdminDashboard />
              {/* <AdminPage /> */}
            </ProtectedRoute>
          } 
        />

        {/* Fallback Route for 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;
