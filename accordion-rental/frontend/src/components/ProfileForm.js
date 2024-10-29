import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Input, VStack, HStack, Text, SimpleGrid } from "@chakra-ui/react";

const ProfileForm = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
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

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      // Get the CSRF token first
      const csrfToken = await getCSRFToken();
  
      const response = await fetch('/api/profile/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // Pass CSRF token in headers
        },
        body: JSON.stringify(formData),
        credentials: 'include',
      });
  
      if (response.ok) {
        navigate('/dashboard'); // Redirect to dashboard on success
      } else {
        const errorData = await response.json();
        setErrors(errorData); // Set validation errors
      }
    } catch (error) {
      console.error('Error updating profile', error);
    }
  };

  const getCSRFToken = async () => {
    const response = await fetch('/api/csrf/', {
      credentials: 'include',
    });
    const data = await response.json();
    return data.csrfToken; // assuming backend returns {'csrfToken': '<token>'}
  };

  // Fetch user data from backend
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/profile/', {
          credentials: 'include',
        });
        const data = await response.json();

        if (data && typeof data === 'object') {
          setFormData((prevState) => ({
            ...prevState,
            firstName: data.firstName || '',
            lastName: data.lastName || '',
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
        }
      } catch (error) {
        console.error('Error fetching profile data', error);
      }
    };

    fetchProfileData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
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
            placeholder="Language"
            name="language"
            value={formData.language}
            onChange={handleInputChange}
            bg="white"
            _placeholder={{ color: "gray.500" }}
          />

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
