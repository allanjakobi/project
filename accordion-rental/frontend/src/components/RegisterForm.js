import Cookies from 'js-cookie';
import { useState, useEffect } from 'react';

const RegisterForm = () => {

  // Define state to hold form data and other states
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [csrfToken, setCsrfToken] = useState('');

  // Fetch CSRF token from Django
  useEffect(() => {
    const token = Cookies.get('csrftoken'); // Fetch CSRF token from cookie
    setCsrfToken(token);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://127.0.0.1:8000/admin/auth/user/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // Include CSRF token in the request headers
      },
      body: JSON.stringify({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        // Other form fields...
      }),
      credentials: 'include',
    });

    if (response.ok) {
      console.log('User registered successfully');
    } else {
      console.log('Error registering user');
    }
  };

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,  // Update the specific field
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

      <button type="submit">Register</button>

      {successMessage && <p>{successMessage}</p>}
    </form>
  );
};

export default RegisterForm;
