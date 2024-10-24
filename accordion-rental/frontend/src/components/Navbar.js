import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in by verifying session token
    const checkLoginStatus = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/check_login/', {
          method: 'GET',
          credentials: 'include', // Send cookies (session ID, CSRF token)
        });

        if (response.ok) {
          setIsLoggedIn(true); // User is logged in
        } else {
          setIsLoggedIn(false); // User is not logged in
        }
      } catch (error) {
        console.error('Error checking login status:', error);
        setIsLoggedIn(false); // Default to not logged in on error
      }
    };

    checkLoginStatus();
  }, []);

  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Available Instruments</Link>
        </li>

        {isLoggedIn ? (
          <>
            <li>
              <Link to="/contracts">Contracts</Link>
            </li>
            <li>
              <Link to="/invoices">Invoices</Link>
            </li>
            <li>
              <Link to="/profile">Profile</Link>
            </li>
            <li>
              <Link to="/logout">Logout</Link>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/register">Register</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;