import { useState, useEffect } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { Box, Button, Input, VStack, Text, Checkbox, Link } from "@chakra-ui/react";

const LoginForm = ({ setIsLoggedIn }) => {
  console.log("vite meta env API", import.meta.env);
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [csrfToken, setCsrfToken] = useState(null);
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();
  const [rememberMe, setRememberMe] = useState(false);
  //const apiUrl = import.meta.env.VITE_API;
  const apiUrl = "192.168.1.187:8000";

  // Fetch CSRF token on component mount
  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const response = await fetch(`/api/get_csrf_token/`, {
          method: 'GET',
          credentials: 'include',
        });
        const data = await response.json();
        setCsrfToken(data.csrfToken);
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
      const response = await fetch(`/api/login/`, {
        method: 'POST',
        timeout: 5000,
        headers: {
          'Content-Type': 'application/json',
          accept: 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(formData),
        credentials: 'include',
      });
    
      if (!response.ok) {
        console.log("response: ", response)
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      

      // Set the state to logged in, and redirect user based on response
      const data = await response.json();
      console.log("Login successful:", data);
      console.log("Access Token (from cookies):", document.cookie
        .split('; ')
        .find(row => row.startsWith('access_token'))
        ?.split('=')[1]);
      console.log("Refresh Token (from cookies):", document.cookie
        .split('; ')
        .find(row => row.startsWith('refresh_token'))
        ?.split('=')[1]);



      setIsLoggedIn(true);
      console.log('Login successful:', data);
      //navigate(data.redirect);
      
    } catch (error) {
      console.error('Login error:', error);
      setErrors({ error: 'Failed to login. Please check your credentials.' });
    }
  };

  return (
    <Box h="60vh" display="flex" justifyContent="center" alignItems="center" bg="gray.100">
      <Box w={['90%', '400px']} p={8} borderRadius="md" boxShadow="lg">
        <form onSubmit={handleSubmit}> {/* Wrap in form element */}
          <VStack spacing={7}>
            <Text fontSize={['3xl', '2xl']} fontWeight="bold" color="black">
              Sign in
            </Text>

            <Input
              placeholder="Username"
              name="username"
              autoComplete="current-password"
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
              autoComplete="current-password" // Add this line
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

            <Button size={['lg', 'lg', 'md']} w="full" colorScheme="teal" type="submit">
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
        </form> {/* Close form element */}
      </Box>
    </Box>
  );
};

export default LoginForm;
