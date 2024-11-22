//registerForm.js
//import Cookies from 'js-cookie';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';  // For redirecting to login page
import { Box, FormControl, FormLabel, Input, Button, VStack, Text } from "@chakra-ui/react";


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
        console.log(data)
        
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
    <Box bg="gray.100" p={8} borderRadius="md" boxShadow="lg" maxW="md" mx="auto" mt={10}>
      <form onSubmit={handleSubmit}>
        <VStack spacing={5}>
          <FormControl isInvalid={errors.username}>
            <FormLabel htmlFor="username">Username</FormLabel>
            <Input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Enter your username"
            />
            {errors.username && <Text color="red.500">{errors.username}</Text>}
          </FormControl>

          <FormControl isInvalid={errors.email}>
            <FormLabel htmlFor="email">Email</FormLabel>
            <Input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Enter your email"
            />
            {errors.email && <Text color="red.500">{errors.email}</Text>}
          </FormControl>

          <FormControl isInvalid={errors.password}>
            <FormLabel htmlFor="password">Password</FormLabel>
            <Input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Enter your password"
            />
            {errors.password && <Text color="red.500">{errors.password}</Text>}
          </FormControl>

          <FormControl isInvalid={passwordError}>
            <FormLabel htmlFor="confirmPassword">Confirm Password</FormLabel>
            <Input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              placeholder="Confirm your password"
            />
            {passwordError && <Text color="red.500">{passwordError}</Text>}
          </FormControl>

          <Button type="submit" colorScheme="teal" size="lg" w="full">
            Register
          </Button>

          {successMessage && <Text color="green.500">{successMessage}</Text>}
        </VStack>
      </form>
    </Box>
  );
};

export default RegisterForm;