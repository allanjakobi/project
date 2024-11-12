import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Input, VStack, HStack, Select, Text, SimpleGrid } from "@chakra-ui/react";

const ProfileForm = () => {
  
  
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    country: 'Estonia',
    province: '',
    municipality: '',
    settlement: '',
    street: '',
    house: '',
    apartment: '',
    phone: '+372',
    language: 'Eesti',
  });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();
  const getAccessToken = () => {
    const name = 'access_token=';
    const decodedCookie = decodeURIComponent(document.cookie); // Decode the cookie
    const cookieArr = decodedCookie.split(';'); // Split by ';' to get individual cookies
    
    // Loop through cookies to find the access_token
    for (let i = 0; i < cookieArr.length; i++) {
        let cookie = cookieArr[i].trim(); // Trim whitespace
        // Check if this cookie starts with access_token=
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length); // Return the token value
        }
    }
    return null; // Return null if token not found
  };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Get the CSRF token
      const csrfToken = await getCSRFToken();
      console.log("CSRF Token:", csrfToken);
  
      // Get the access token
      const accessToken = document.cookie.split('; ').find(row => row.startsWith('access_token=')).split('=')[1];
  
      // Check if accessToken is available
      if (!accessToken) {
        console.error("Access token not found.");
        return;
      }
      console.log("Access token : ", accessToken);
  
      const response = await fetch('http://localhost:8000/api/profile/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`, // Include the access token here
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(formData),
        credentials: 'include',
      });
      console.log("Profile update response:", response);
  
      if (response.ok) {
        console.log("Profile updated successfully.");
        navigate('/'); // Redirect to the main page on success
      } else {
        console.error("Profile update failed with status:", response.status);
        const errorData = await response.json();
        console.log("Error data:", errorData);
        setErrors(errorData); // Set validation errors
      }
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  const getCSRFToken = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/csrf/', { credentials: 'include' });
      console.log("CSRF token response:", response);
      
      const data = await response.json();
      console.log("CSRF token data:", data);
      return data.csrfToken; // assuming backend returns {'csrfToken': '<token>'}
    } catch (error) {
      console.error('Error fetching CSRF token:', error);
      return null;
    }
  };

  // Fetch user data from backend
  useEffect(() => {
    const testAuth = async () => {
      const csrfToken = await getCSRFToken(); // Define or import getCSRFToken function if needed
      const accessToken = localStorage.getItem('access_token'); // Adjust based on where you're storing the token

      try {
        const response = await fetch('http://localhost:8000/api/test-auth/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
        });

        if (response.ok) {
          console.log("Authenticated successfully.");
        } else {
          console.error("Failed AUUuthentication:", response.status);
        }
      } catch (error) {
        console.error('Error during authentication check:', error);
      }
    };

    testAuth();
    const fetchProfileData = async () => {
      const access_token = getAccessToken();
      if (!access_token) {
        console.error("No access token found");
        return;
      }
      const csrfToken = getCSRFToken()
    
      try {
        const response = await fetch('http://localhost:8000/api/profile/', {
          method: 'GET',
          headers: {
            'X-CSRFToken': csrfToken,
            //'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`,
          },
          credentials: 'include',
        });
    
        if (response.ok) {
          const data = await response.json();
          setFormData((prevState) => ({
            ...prevState,
            firstName: data.firstName || '',
            lastName: data.lastName || '',
            email: data.email || data.email2,
            country: data.country || 'Estonia',
            province: data.province || '',
            municipality: data.municipality || '',
            settlement: data.settlement || '',
            street: data.street || '',
            house: data.house || '',
            apartment: data.apartment || '',
            phone: data.phone || '+372',
            language: data.language || 'Eesti',
          }));
        } else {
          console.error("Failed to fetch profile data:", response.status);
        }
      } catch (error) {
        console.error('Error fetching profile data:', error);
      }
    };

    fetchProfileData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    console.log(`Changing ${name} to ${value}`);
    setFormData({ ...formData, [name]: value });
  };

  return (
    <Box
      maxW="600px"
      mx="auto"
      p={8}
      borderWidth={1}
      borderRadius="lg"
      boxShadow="xl"
      bg="gray.50"
    >
      <Text fontSize="2xl" fontWeight="bold" mb={6} textAlign="center" color="teal.500">
        Update Profile
      </Text>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <SimpleGrid columns={2} spacing={4} w="full">
            <Input
              placeholder="First Name"
              name="firstName"
              value={formData.firstName}
              onChange={handleInputChange}
              bg="white"
              _placeholder={{ color: "gray.500" }}
            />
            <Input
              placeholder="Last Name"
              name="lastName"
              value={formData.lastName}
              onChange={handleInputChange}
              bg="white"
              _placeholder={{ color: "gray.500" }}
            />
          </SimpleGrid>

          <SimpleGrid columns={2} spacing={4} w="full">
            <Input
              placeholder="Country"
              name="country"
              value={formData.country}
              onChange={handleInputChange}
              bg="white"
              _placeholder={{ color: "gray.500" }}
            />
            <Input
              placeholder="Province"
              name="province"
              value={formData.province}
              onChange={handleInputChange}
              bg="white"
              _placeholder={{ color: "gray.500" }}
            />
          </SimpleGrid>

          <Input
            placeholder="Municipality"
            name="municipality"
            value={formData.municipality}
            onChange={handleInputChange}
            bg="white"
            _placeholder={{ color: "gray.500" }}
          />
          <Input
            placeholder="Settlement"
            name="settlement"
            value={formData.settlement}
            onChange={handleInputChange}
            bg="white"
            _placeholder={{ color: "gray.500" }}
          />
          <Input
            placeholder="Street"
            name="street"
            value={formData.street}
            onChange={handleInputChange}
            bg="white"
            _placeholder={{ color: "gray.500" }}
          />
          
          <SimpleGrid columns={3} spacing={4} w="full">
            <Input
              placeholder="House"
              name="house"
              value={formData.house}
              onChange={handleInputChange}
              bg="white"
              _placeholder={{ color: "gray.500" }}
            />
            <Input
              placeholder="Apartment"
              name="apartment"
              value={formData.apartment}
              onChange={handleInputChange}
              bg="white"
              _placeholder={{ color: "gray.500" }}
            />
            <Input
              placeholder="Phone"
              name="phone"
              value={formData.phone}
              onChange={handleInputChange}
              bg="white"
              _placeholder={{ color: "gray.500" }}
            />
          </SimpleGrid>

          <Input
              placeholder="Email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              bg="white"
              _placeholder={{ color: "gray.500" }}
              
            />

          <Select placeholder="Language" name="language" value={formData.language} onChange={handleInputChange} bg="white" isRequired>
            <option value="Eesti">Eesti</option>
            <option value="English">English</option>
          </Select>

          <Button colorScheme="teal" w="full" size="lg" type="submit">
            Save Profile
          </Button>

          {errors &&
            Object.keys(errors).map((key) => (
              <Text key={key} color="red.500">
                {errors[key]}
              </Text>
            ))}
        </VStack>
      </form>
    </Box>
  );
};

export default ProfileForm;
