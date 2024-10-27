import { useState, useEffect } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { Box, Flex, HStack, Link, Button } from '@chakra-ui/react';

const Navbar = ({ isLoggedIn, setIsLoggedIn }) => {
  const navigate = useNavigate();
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await fetch('/api/check_login/', {
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
        setIsLoggedIn(false);
      }
    };

    checkLoginStatus();
  }, [setIsLoggedIn]);

  return (
    <Box bg="teal.500" px={4}>
      <Flex h={16} alignItems="center" justifyContent="space-between">
        {/* Left side - Available Instruments */}
        <HStack spacing={8} alignItems="center">
          <Link
            as={RouterLink}
            to="/"
            fontWeight="bold"
            color="white"
            _hover={{ textDecoration: 'underline', color: 'teal.100' }}
          >
            Available Instruments
          </Link>
        </HStack>

        {/* Right side - Conditional navigation based on login status */}
        <HStack as="nav" spacing={4}>
          {isLoggedIn ? (
            <>
              <Link as={RouterLink} to="/contracts" color="white" _hover={{ textDecoration: 'underline', color: 'teal.100' }}>Contracts</Link>
              <Link as={RouterLink} to="/invoices" color="white" _hover={{ textDecoration: 'underline', color: 'teal.100' }}>Invoices</Link>
              <Link as={RouterLink} to="/profile" color="white" _hover={{ textDecoration: 'underline', color: 'teal.100' }}>Profile</Link>
              <Button
                as="button"
                onClick={() => navigate("/logout")}
                colorScheme="teal"
                variant="solid"
                size="sm"
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button as={RouterLink} to="/register" colorScheme="teal" variant="outline" size="sm">Register</Button>
              <Button as={RouterLink} to="/login" colorScheme="teal" variant="solid" size="sm">Login</Button>
            </>
          )}
        </HStack>
      </Flex>
    </Box>
  );
};

export default Navbar;
