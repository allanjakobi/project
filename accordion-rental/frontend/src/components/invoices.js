import React, { useEffect, useState } from 'react';
import { Box, Text, VStack, Button } from '@chakra-ui/react';

function Invoices() {
  const [agreements, setAgreements] = useState([]);
  const handleDownload = (invoiceId) => {
    const downloadUrl = `http://localhost:8000/api/invoices/download/${invoiceId}/`;
    window.location.href = downloadUrl; // Initiates file download
  };

  useEffect(() => {
    async function fetchAgreements() {
        const response = await fetch('http://localhost:8000/api/invoices/', {
            credentials: 'include',
          });
      if (response.ok) {
        const data = await response.json();
        setAgreements(data);
      } else {
        console.error('Failed to fetch agreements and invoices');
      }
    }

    fetchAgreements();
  }, []);

  return (
    <VStack spacing={4} align="start">
      {agreements.map((agreement) => (
        <Box key={agreement.agreement.agreementId} p={4} borderWidth={1} borderRadius="md">
          <Text fontWeight="bold">
            Agreement #{agreement.agreement.agreementId}: Ref nr {agreement.agreement.referenceNr}
          </Text>
          {/* <Text>Instrument ID: {agreement.agreement.instrumentID}</Text>
          <Text>Start Date: {agreement.agreement.startDate}</Text>
          <Text>Months: {agreement.agreement.months}</Text>
          <Text>Status: {agreement.agreement.status}</Text> */}
          <Text fontWeight="bold" mt={2}>Invoices:</Text>
          {agreement.invoices.length > 0 ? (
            agreement.invoices.map((invoice) => (
                <Box key={invoice.id} mb={2}>
                <Text>
                  Invoice {invoice.id} issued at {invoice.date} : ${invoice.price}, Status: {invoice.status}
                </Text>
                <Button
                  colorScheme="teal"
                  size="sm"
                  onClick={() => handleDownload(invoice.id)}
                >
                  Download
                </Button>
              </Box>
              
            ))
          ) : (
            <Text>No invoices available.</Text>
          )}
        </Box>
      ))}
    </VStack>
  );
}

export default Invoices;
