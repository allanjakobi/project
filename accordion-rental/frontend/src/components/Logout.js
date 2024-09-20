import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        // Call the backend API to log out the user
        const response = await fetch('http://127.0.0.1:8000/api/logout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include', // Include cookies (session ID, CSRF token)
        });

        if (response.ok) {
          // Clear all tokens from localStorage or sessionStorage
          localStorage.clear(); // or sessionStorage.clear() if you are using sessionStorage

          // Clear cookies by setting them to expire
          document.cookie = 'csrftoken=; Max-Age=0; path=/;';
          document.cookie = 'sessionid=; Max-Age=0; path=/;';

          // Redirect to the login page
          navigate('/login');
        } else {
          console.error('Failed to log out:', await response.json());
        }
      } catch (error) {
        console.error('Error during logout:', error);
      }
    };

    handleLogout();
  }, [navigate]);

  return <div>Logging out...</div>;
};

export default Logout;
