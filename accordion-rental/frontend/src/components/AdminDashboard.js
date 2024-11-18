import React, { useState, useEffect } from "react";
import { Box, Button, Input, Table, Tbody, Td, Th, Thead, Tr, Textarea, Heading } from "@chakra-ui/react";
import axios from "axios";

const AdminDashboard = () => {
  const [agreements, setAgreements] = useState([]);
  const [emailMessages, setEmailMessages] = useState({});
  const [file, setFile] = useState(null);

  useEffect(() => {
    fetchAgreements();
  }, []);

  const fetchAgreements = async () => {
    try {
      const response = await axios.get("/api/admin/agreements/");
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
    console.log("DATA!: ", formData)
    formData.append("file", file);

    try {
      await axios.post("/api/admin/upload-payments/", formData);
      alert("Payments uploaded successfully.");
    } catch (error) {
      console.error("Error uploading file", error);
    }
  };

  const handleEmailChange = (agreementId, value) => {
    setEmailMessages((prev) => ({
      ...prev,
      [agreementId]: value, // Update message for the specific agreementId
    }));
  };

  // Function to send email
  const handleSendEmail = (agreementId) => {
    const emailMessage = emailMessages[agreementId];
    console.log(`Sending email for agreement ${agreementId}:`, emailMessage);

    fetch(`/api/send-email/${agreementId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: emailMessage }),
    })
      .then((response) => response.json())
      .then((data) => console.log("Email sent:", data))
      .catch((error) => console.error("Error sending email:", error));
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
              <Td>
                {agreement.status}{' @ '}
                <span style={{ color: agreement.paymentsDue < 0 ? 'red' : 'inherit' }}>
                  {agreement.paymentsDue}€
                </span>
              </Td>
              <Td>
                {agreement.instrument.brand} {agreement.instrument.model} ({agreement.instrument.color})
              </Td>
              <Td>
            <Button>Signed</Button>
            <Button>Returned</Button>
            <Textarea
              placeholder="Short email message"
              value={emailMessages[agreement.agreementId] || ""} // Get value for the specific agreementId
              onChange={(e) => handleEmailChange(agreement.agreementId, e.target.value)} // Update the state
            />
            <Button
              mt={2} // Add some spacing
              colorScheme="blue"
              onClick={() => handleSendEmail(agreement.agreementId)} // Trigger send
            >
              Send
            </Button>
          </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
      
    </Box>
  );
};

export default AdminDashboard;
