import Cookies from 'js-cookie';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';  // For redirecting to login page

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',  // Add confirmPassword state
  });
  const [errors, setErrors] = useState({});
  const [passwordError, setPasswordError] = useState('');  // State for password mismatch
  const [successMessage, setSuccessMessage] = useState('');
  const [csrfToken, setCsrfToken] = useState('');
  const navigate = useNavigate();  // React Router's navigate function

  // Fetch CSRF token from Django backend explicitly
  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/csrf/', {
          credentials: 'include',  // Ensures cookies (CSRF token) are included
        });
        const data = await response.json();
        setCsrfToken(data.csrfToken);  // Store token in state
      } catch (error) {
        console.error('Failed to fetch CSRF token', error);
      }
    };

    fetchCsrfToken();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if passwords match before submitting
    if (formData.password !== formData.confirmPassword) {
      setPasswordError('Passwords do not match');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,  // Include CSRF token
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
        }),
        credentials: 'include',  // Include cookies (for CSRF)
      });
  
      if (response.ok) {
        const data = await response.json();
        setSuccessMessage('User added successfully!');
        
        // Redirect to login after successful registration
        setTimeout(() => {
          navigate('/login');  // Redirect to login page
        }, 1500);  // Delay the redirect to show success message

      } else {
        const errorData = await response.json();
        setErrors(errorData);
      }
    } catch (error) {
      console.error('Error registering user', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Username:</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleInputChange}
        />
        {errors.username && <span>{errors.username}</span>}
      </div>

      <div>
        <label>Email:</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
        />
        {errors.email && <span>{errors.email}</span>}
      </div>

      <div>
        <label>Password:</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleInputChange}
        />
        {errors.password && <span>{errors.password}</span>}
      </div>

      <div>
        <label>Confirm Password:</label>
        <input
          type="password"
          name="confirmPassword"  // Handle confirm password
          value={formData.confirmPassword}
          onChange={handleInputChange}
        />
        {passwordError && <span>{passwordError}</span>}  {/* Display password mismatch error */}
      </div>

      <button type="submit">Register</button>

      {successMessage && <p>{successMessage}</p>}
    </form>
  );
};

export default RegisterForm;
