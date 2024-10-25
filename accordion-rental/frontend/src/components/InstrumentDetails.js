import React from 'react';
import { Box, Image, Text, Button, VStack, useBreakpointValue } from "@chakra-ui/react";

const InstrumentDetails = ({ instrument, onBack }) => {
  // Select appropriate image based on device size
  const imageUrl = useBreakpointValue({
    base: instrument.mobile_image,    // for mobile devices
    md: instrument.desktop_image,     // for medium and larger devices
  });

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
          <Button colorScheme="teal" size="lg" mt={4}>
            Reserve
          </Button>
        )}
      </VStack>
    </Box>
  );
};

export default InstrumentDetails;
