import React from 'react';
import { Box, Image, Text, Button, VStack, useBreakpointValue } from "@chakra-ui/react";
import { useNavigate } from 'react-router-dom';

const InstrumentDetails = ({ instrument, onBack, isLoggedIn }) => {
  const navigate = useNavigate();
  const accessToken = localStorage.getItem('access_token'); // Replace with your storage method if needed

  
  const imageUrl = useBreakpointValue({
    base: instrument.mobile_image,
    md: instrument.desktop_image,
  });

  const handleReserve = async () => {
    if (isLoggedIn) {
      try {
        // Assuming you have an API endpoint to reserve the instrument
        
        const response = await fetch(`/api/instruments/${instrument.instrumentId}/reserve`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`, // If you are using JWT for auth
          },
          body: JSON.stringify({ status: 'Reserved' }),
        });
  
        if (response.ok) {
          // Navigate to rent page with instrument details
          navigate('/rent', { state: { instrument: { ...instrument, status: 'Reserved' } } });
        } else {
          console.error('Failed to reserve the instrument.');
        }
      } catch (error) {
        console.error('Error updating instrument status:', error);
      }
    } else {
      // Navigate to login page if not logged in
      navigate('/login');
    }
  };

  return (
    <Box p={5} maxW="800px" mx="auto" boxShadow="md" borderRadius="lg" bg="white">
      <Button onClick={onBack} colorScheme="teal" mb={4}>
        Back to List
      </Button>

      <Image 
        src={imageUrl} 
        alt={`${instrument.modelId.brand} ${instrument.modelId.model}`} 
        borderRadius="lg"
        mb={5}
      />

      <VStack align="start" spacing={4}>
        <Text fontSize="2xl" fontWeight="bold">{instrument.modelId.brand} {instrument.modelId.model}</Text>
        <Text fontSize="lg">Color: {instrument.color}</Text>
        <Text fontSize="lg">Serial: {instrument.serial}</Text>
        <Text fontSize="lg">Status: {instrument.status}</Text>
        <Text fontSize="lg">Price Level: {instrument.price_level}</Text>

        <Text fontSize="2xl" fontWeight="bold">Model Details:</Text>
        <Text>Keys: {instrument.modelId.keys}</Text>
        <Text>Weight: {instrument.modelId.weight} kg</Text>
        <Text>Dimensions: {instrument.modelId.height} cm x {instrument.modelId.width} cm</Text>
        <Text>Reeds (Right/Left): {instrument.modelId.reedsR} / {instrument.modelId.reedsL}</Text>
        <Text>New Price: ${instrument.modelId.newPrice}</Text>
        <Text>Used Price: ${instrument.modelId.usedPrice}</Text>

        <Text fontSize="2xl" fontWeight="bold">Additional Info:</Text>
        <Text>{instrument.info_est}</Text>
        <Text>{instrument.info_eng}</Text>

        {instrument.status === 'Available' && (
          <Button colorScheme="teal" size="lg" mt={4} onClick={handleReserve}>
            Reserve
          </Button>
        )}
      </VStack>
    </Box>
  );
};

export default InstrumentDetails;
