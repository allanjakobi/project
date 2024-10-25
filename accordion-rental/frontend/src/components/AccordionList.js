import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box, Grid, Image, Heading, Text, Badge, Spinner, useBreakpointValue,
} from "@chakra-ui/react";
import InstrumentDetails from './InstrumentDetails'; // Import the detailed component

const AccordionList = () => {
  const [instruments, setInstruments] = useState([]);
  const [loading, setLoading] = useState(true); // For showing a loading state
  const [error, setError] = useState(null);
  const [selectedInstrument, setSelectedInstrument] = useState(null); // State for selected instrument

  // Fetch data from the API
  useEffect(() => {
    const fetchInstruments = async () => {
      try {
        const response = await axios.get('/api/available-instruments/');
        setInstruments(response.data);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
      }
    };
  
    fetchInstruments();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minH="60vh">
        <Spinner size="xl" color="teal.500" />
      </Box>
    );
  }

  if (error) {
    return <Box textAlign="center" color="red.500">Error fetching available instruments: {error.message}</Box>;
  }

  return (
    <Box p={8} bg="gray.100" minH="100vh">
      {selectedInstrument ? (
        <InstrumentDetails 
          instrument={selectedInstrument} 
          onBack={() => setSelectedInstrument(null)} // Pass the onBack function
        />
      ) : (
        <>
          <Heading as="h1" size="2xl" textAlign="center" mb={8} color="teal.600">
            Available Instruments
          </Heading>
          <Grid templateColumns={['repeat(1, 1fr)', 'repeat(2, 1fr)', 'repeat(3, 1fr)']} gap={8}>
            {instruments.map(instrument => (
              <Box
                key={instrument.instrumentId}
                bg="white"
                borderRadius="md"
                boxShadow="lg"
                overflow="hidden"
                _hover={{ transform: 'scale(1.05)', transition: '0.3s ease' }}
                cursor="pointer"
                onClick={() => setSelectedInstrument(instrument)} // On click, show details
              >
                <Image
                  src={instrument.thumbnail_image}
                  alt={`${instrument.modelId.brand} ${instrument.modelId.model}`}
                  objectFit="cover"
                  w="100%"
                  h={["200px", "250px", "300px"]}
                />
                <Box p={6}>
                  <Heading as="h3" size="lg" mb={2} color="teal.600">
                    {instrument.modelId.brand} {instrument.modelId.model}
                  </Heading>
                  <Text fontSize="md" color="gray.600">Color: {instrument.color}</Text>
                  <Text fontSize="md" color="gray.600">Serial: {instrument.serial}</Text>

                  <Badge colorScheme={instrument.status === 'Available' ? 'green' : 'red'} mb={2}>
                    {instrument.status}
                  </Badge>
                  
                  <Text fontSize="md" fontWeight="bold" color="gray.700">
                    Price Level: {instrument.price_level}
                  </Text>

                  <Heading as="h4" size="md" mt={4} mb={2} color="teal.500">
                    Model Details
                  </Heading>
                  <Text fontSize="sm" color="gray.600">Keys: {instrument.modelId.keys}</Text>
                  <Text fontSize="sm" color="gray.600">Weight: {instrument.modelId.weight} kg</Text>
                  <Text fontSize="sm" color="gray.600">
                    Dimensions: {instrument.modelId.height}cm x {instrument.modelId.width}cm
                  </Text>
                  <Text fontSize="sm" color="gray.600">
                    Reeds (Right/Left): {instrument.modelId.reedsR}/{instrument.modelId.reedsL}
                  </Text>
                </Box>
              </Box>
            ))}
          </Grid>
        </>
      )}
    </Box>
  );
};

export default AccordionList;
