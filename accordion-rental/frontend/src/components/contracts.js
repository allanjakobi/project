import React, { useEffect, useState } from 'react';
import { Box, Text, Table, Thead, Tbody, Tr, Th, Td, Image } from '@chakra-ui/react';

const Contracts = () => {
  const [contracts, setContracts] = useState([]);

  useEffect(() => {
    const fetchContracts = async () => {
      const response = await fetch('http://localhost:8000/api/contracts/', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        console.log("LEPINGUD: ", data)
        setContracts(data);
      }
    };
    fetchContracts();
  }, []);

  return (
    <Box padding="4">
      <Text fontSize="xl" mb={4} fontWeight="bold">CONTRACTS</Text>

      {contracts.map((contract, index) => (
        <Box key={index} borderWidth="1px" borderRadius="lg" p="6" mb="4">
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th fontSize="l">Agreement nr: {contract.agreement.agreementId}</Th>
                <Th>Model Details</Th>
                <Th>Instrument Details</Th>
              </Tr>
            </Thead>
            <Tbody>
              <Tr>
                <Td>
                  {/* Display Agreement details */}
                  
                  <p>Contract : {contract.agreement.status}</p>
                  <p>Refernce nr: {contract.agreement.referenceNr}</p>
                  <p>Rate: ${contract.agreement.rate} per month</p>
                  <p>Start Date: {contract.agreement.startDate}</p>
                  <p>Instrument returned before: {contract.agreement.endDate}</p>|
                </Td>
                <Td>
                  {/* Display Model details */}
                  <p>Brand: {contract.model.brand}</p>
                  <p>Model: {contract.model.model}</p>
                  <p>{contract.model.keys} keys</p>
                  <p>{contract.model.sb} basses</p>
                </Td>
                <Td>
                  {/* Display Indstrument details */}
                  <p>Serial: {contract.instrument.serial}</p>
                  <p>instrumentId: {contract.instrument.instrumentId}</p>
                  <p>Status: {contract.instrument.status}</p>
                  <p>Color: {contract.instrument.color}</p>
                </Td>
              </Tr>
              <Tr>
                <Td colSpan="3" textAlign="center">
                  <Image
                    src={`http://localhost:8000${contract.imageLink}`}
                    alt="Instrument Image"
                    boxSize="200px"
                  />
                </Td>
              </Tr>
            </Tbody>
          </Table>
        </Box>
      ))}
    </Box>
  );
};

export default Contracts;
