import React, { useState, useEffect } from "react";
import {
  Box, Button, Input, Table, Tbody, Td, Th, Thead, Tr, Textarea
} from "@chakra-ui/react";
import axios from "axios";

const AdminPage = () => {
  const [agreements, setAgreements] = useState([]);
  const [file, setFile] = useState(null);

  useEffect(() => {
    fetchAgreements();
  }, []);

  const fetchAgreements = async () => {
    try {
      const response = await axios.get("/admin/agreements/");
      setAgreements(response.data.agreements);
    } catch (error) {
      console.error("Error fetching agreements", error);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("/admin/upload-payments/", formData);
      alert("Payments uploaded successfully.");
    } catch (error) {
      console.error("Error uploading file", error);
    }
  };

  const handleSendEmail = async (agreementId, message) => {
    try {
      await axios.post(`/admin/send-email/${agreementId}/`, { message });
      alert("Email sent successfully.");
    } catch (error) {
      console.error("Error sending email", error);
    }
  };

  return (
    <Box padding="4">
      {/* Upload Section */}
      <Box marginBottom="8">
        <Input type="file" onChange={handleFileChange} />
        <Button onClick={handleFileUpload}>Upload Payments</Button>
      </Box>

      {/* Agreements Table */}
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Agreement ID</Th>
            <Th>Start Date</Th>
            <Th>End Date</Th>
            <Th>Status</Th>
            <Th>Instrument</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {agreements.map((agreement) => (
            
            <Tr key={agreement.agreementId}>
              <Td>{agreement.agreementId}</Td>
              <Td>{agreement.startDate}</Td>
              <Td>{agreement.endDate}</Td>
              <Td>{agreement.status}</Td>
              <Td>
                {agreement.instrument.brand} {agreement.instrument.model} ({agreement.instrument.color})
              </Td>
              <Td>
                <Button>Signed</Button>
                <Button>Returned</Button>
                <Textarea
                  placeholder="Short email message"
                  onBlur={(e) => handleSendEmail(agreement.agreementId, e.target.value)}
                />
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default AdminPage;
