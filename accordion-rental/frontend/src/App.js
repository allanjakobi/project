// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AccordionList from './components/AccordionList';
import RegisterForm from './components/RegisterForm';
import Profile from './components/ProfileForm';
import AdminDashboard from './components/AdminDashboard';
import LoginForm from './components/LoginForm';

function App() {
  return (
    <Router>
      <Routes>
        {/* Use 'element' instead of 'component', and pass the components as JSX elements */}
        <Route path="/" element={<AccordionList />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/profile" element={<Profile />} /> {/* Define the profile route */}
        <Route path="/login" element={<LoginForm />} />
        
      </Routes>
    </Router>
  );
}

export default App;
