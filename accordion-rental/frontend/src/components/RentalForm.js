import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  Text,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Button,
  VStack,
  Divider,
  Spinner,
  useToast,
} from '@chakra-ui/react';

const RentalForm = ({ userId }) => {
  const location = useLocation();
  const instrument = location.state?.instrument; // Access instrument data passed from previous component
  const [rentalPeriod, setRentalPeriod] = useState(12);
  const [additionalInfo, setAdditionalInfo] = useState('');
  const [rate, setRate] = useState(null);
  const [finalRate, setFinalRate] = useState(null); // To hold the final rental rate
  const navigate = useNavigate();
  const toast = useToast();

  // Fetch rate based on price_level when the component mounts
  useEffect(() => {
    if (instrument?.price_level) {
      fetch(`/api/rates/${instrument.price_level}`)
        .then(response => response.json())
        .then(data => {
          setRate(data.rate);
          setFinalRate(data.rate); // Set the final rate initially to fetched rate
        })
        .catch(error => {
          console.error('Error fetching rate:', error);
          toast({
            title: "Error loading rate",
            description: "Unable to retrieve rental rate information.",
            status: "error",
            duration: 4000,
            isClosable: true,
          });
        });
    }
  }, [instrument, toast]);

  // Update final rate based on rental period
  useEffect(() => {
    if (rate) {
      let updatedRate;
      if (rentalPeriod >= 0 && rentalPeriod < 4) {
        updatedRate = Math.round(rate * 2.1); // 0-3 months
      } else if (rentalPeriod >= 4 && rentalPeriod < 12) {
        updatedRate = Math.round(rate * 1.4); // 4-11 months
      } else {
        updatedRate = rate; // 12 months or greater
      }
      setFinalRate(updatedRate);
    }
  }, [rentalPeriod, rate]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const agreementData = {
      userId: userId,
      instrumentId: instrument?.id,
      startDate: new Date().toISOString(),
      months: rentalPeriod,
      rate: finalRate, // Use the calculated rental rate
      info: additionalInfo,
      status: 'created',
    };

    try {
      const response = await fetch('/api/agreements', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(agreementData),
      });

      if (response.ok) {
        toast({
          title: "Agreement created",
          description: "Your rental agreement has been successfully submitted.",
          status: "success",
          duration: 4000,
          isClosable: true,
        });
        navigate('/profile'); // Redirect after successful submission
      } else {
        toast({
          title: "Error",
          description: "There was an issue submitting your agreement.",
          status: "error",
          duration: 4000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error('Error creating rental agreement:', error);
      toast({
        title: "Submission failed",
        description: "Network error during agreement submission.",
        status: "error",
        duration: 4000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={8} bg="gray.100" minH="100vh" display="flex" justifyContent="center" alignItems="center">
      <Box
        p={6}
        maxW="600px"
        w="full"
        boxShadow="lg"
        rounded="lg"
        bg="white"
      >
        <VStack spacing={4} align="stretch">
          <Text fontSize="2xl" fontWeight="bold" color="teal.600" mb={4}>
            Rental Agreement for {instrument?.modelId.brand} {instrument?.modelId.model}
          </Text>
          <Divider />

          <Box>
            <Text fontSize="lg" color="gray.600">Price Level: {instrument?.price_level}</Text>
            <Text fontSize="lg" color="gray.600">
              Rental Rate: {rate ? `$${rate}` : <Spinner size="xs" color="teal.500" />}
            </Text>
          </Box>

          <FormControl id="rentalPeriod" isRequired>
            <FormLabel>Rental Period (months)</FormLabel>
            <Input
              type="number"
              value={rentalPeriod}
              onChange={(e) => setRentalPeriod(e.target.value)}
              min="1"
              bg="gray.50"
              placeholder="Enter rental duration in months"
            />
          </FormControl>

          <FormControl id="additionalInfo">
            <FormLabel>Additional Information</FormLabel>
            <Textarea
              value={additionalInfo}
              onChange={(e) => setAdditionalInfo(e.target.value)}
              placeholder="Add any relevant notes"
              bg="gray.50"
              resize="vertical"
            />
          </FormControl>

          <Divider />

          <Text fontSize="lg" fontWeight="bold">Summary:</Text>
          <Text fontSize="md">Brand: {instrument?.modelId.brand}</Text>
          <Text fontSize="md">Model: {instrument?.modelId.model}</Text>
          <Text fontSize="md">Price Level: {instrument?.price_level}</Text>
          <Text fontSize="md">Rental Period: {rentalPeriod} months</Text>
          <Text fontSize="md">Rate: {finalRate !== null ? `$${finalRate} per month` : 'Loading...'}</Text>

          <Button
            mt={4}
            colorScheme="teal"
            size="lg"
            type="submit"
            onClick={handleSubmit}
          >
            Submit Rental Agreement
          </Button>
        </VStack>
      </Box>
    </Box>
  );
};

export default RentalForm;
