import { useState, useEffect } from 'react';
import { useNavigate, Link as RouterLink  } from 'react-router-dom';
import { Box, Button, Input, VStack, Text, Checkbox, Link } from "@chakra-ui/react";


const LoginForm = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [csrfToken, setCsrfToken] = useState(null); // State for CSRF token
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();
  const [rememberMe, setRememberMe] = useState(false);

  // Fetch CSRF token on component mount
  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/get_csrf_token/', {
          method: 'GET',
          credentials: 'include',
        });
        const data = await response.json();
        setCsrfToken(data.csrfToken); // Save CSRF token to state
      } catch (error) {
        console.error('Error fetching CSRF token:', error);
      }
    };

    fetchCsrfToken();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // Include CSRF token if needed
        },
        body: JSON.stringify(formData),
        credentials: 'include', // Important to include cookies
      });
  
      if (response.ok) {
        // You can fetch a new CSRF token or just navigate
        navigate('/profile');
      } else {
        const errorData = await response.json();
        setErrors(errorData);
      }
    } catch (error) {
      console.error('Error logging in:', error);
    }
  };

  return (
    <Box h="60vh" display="flex" justifyContent="center" alignItems="center" bg="gray.100">
      <Box w={['90%', '400px']} p={8} borderRadius="md" boxShadow="lg">
        <VStack spacing={7}>
          <Text fontSize={['3xl', '2xl']} fontWeight="bold" color="black">
            Sign in
          </Text>

          <Input
            placeholder="Username"
            name="username"
            value={formData.username}
            onChange={handleInputChange}
            color="white"
            bg="teal.400"
            _placeholder={{ color: "white" }}
            type="text"
            fontSize={['lg', 'md']}
          />
          {errors.username && <Text color="red.500">{errors.username}</Text>}

          <Input
            placeholder="Password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            color="white"
            bg="teal.400"
            _placeholder={{ color: "white" }}
            type="password"
            fontSize={['lg', 'md']}
          />
          {errors.password && <Text color="red.500">{errors.password}</Text>}

          <Checkbox
            isChecked={rememberMe}
            onChange={() => setRememberMe(!rememberMe)}
            colorScheme="green"
            color="black"
            fontSize={['lg', 'md']}
          >
            Remember me
          </Checkbox>

          <Button size={['lg', 'lg', 'md']} w="full" colorScheme="teal" onClick={handleSubmit}>
            Login
          </Button>

          {errors.error && <Text color="red.500">{errors.error}</Text>}

          <Text fontSize={['md', 'sm']} color="gray.600">
            Don’t have an account yet?{" "}
            <Link as={RouterLink} to="/register" color="teal.500" fontWeight="bold">
              Register here
            </Link>
          </Text>
        </VStack>
      </Box>
    </Box>
  );
};

export default LoginForm;