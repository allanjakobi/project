import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = ({ setIsLoggedIn }) => {
  const [csrfToken, setCsrfToken] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch CSRF token on component mount
    const fetchCsrfToken = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/get_csrf_token/', {
          method: 'GET',
          credentials: 'include', // Include cookies
        });
        const data = await response.json();
        setCsrfToken(data.csrfToken);
      } catch (error) {
        console.error("Failed to fetch CSRF token:", error);
      }
    };

    fetchCsrfToken();
  }, []);

  useEffect(() => {
    const handleLogout = async () => {
      if (!csrfToken) return; // Ensure csrfToken is available before attempting logout

      try {
        const response = await fetch('/api/logout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Include CSRF token here
          },
          credentials: 'include', // Important for sending cookies
        });

        if (response.ok) {
          setIsLoggedIn(false); // Clear login state
          console.log("Logged out successfully");
          navigate("/"); // Redirect to homepage
        } else {
          const data = await response.json();
          console.error("Logout failed:", data);
        }
      } catch (error) {
        console.error("Error during logout:", error);
      }
    };

    handleLogout();
  }, [csrfToken, navigate, setIsLoggedIn]); // Include setIsLoggedIn in dependencies

  return <div>Logging out...</div>;
};

export default Logout;
