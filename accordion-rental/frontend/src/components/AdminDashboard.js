import React, { useState, useEffect } from "react";
import { Box, Button, Input, Table, Tbody, Td, Th, Thead, Tr, Textarea } from "@chakra-ui/react";
import axios from "axios";

const AdminDashboard = () => {
  const [agreements, setAgreements] = useState([]);
  const [sortedAgreements, setSortedAgreements] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });
  const [emailMessages, setEmailMessages] = useState({});
  const [file, setFile] = useState(null);

  useEffect(() => {
    fetchAgreements();
  }, []);

  useEffect(() => {
    sortAgreements();
  }, [sortConfig, agreements]);

  const fetchAgreements = async () => {
    try {
      const response = await axios.get("/api/admin/agreements/");
      setAgreements(response.data.agreements);
      setSortedAgreements(response.data.agreements); // Initialize sortedAgreements
    } catch (error) {
      console.error("Error fetching agreements", error);
    }
  };

  const sortAgreements = () => {
    const sorted = [...agreements];
    if (sortConfig.key) {
      sorted.sort((a, b) => {
        let aValue, bValue;
  
        if (sortConfig.key === "hasActionButton") {
          // Determine if action buttons are present based on status
          aValue = ["Created", "Active", "Test", "EndingSoon", "Ended"].includes(a.status) ? 1 : 0;
          bValue = ["Created", "Active", "Test", "EndingSoon", "Ended"].includes(b.status) ? 1 : 0;
        } else {
          aValue = a[sortConfig.key] || "";
          bValue = b[sortConfig.key] || "";
        }
  
        if (typeof aValue === "string") aValue = aValue.toLowerCase();
        if (typeof bValue === "string") bValue = bValue.toLowerCase();
  
        if (aValue < bValue) {
          return sortConfig.direction === "asc" ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === "asc" ? 1 : -1;
        }
        return 0;
      });
    }
    setSortedAgreements(sorted);
  };

  const handleSort = (key) => {
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === "asc" ? "desc" : "asc",
    }));
  };

  const handleFileChange = (e) => setFile(e.target.files[0]);
  const handleFileUpload = async () => { /* Upload logic */ };

  const handleEmailChange = (agreementId, value) => {
    setEmailMessages((prev) => ({
      ...prev,
      [agreementId]: value,
    }));
  };

  const handleSendEmail = async (agreementId) => {
    const emailMessage = emailMessages[agreementId];
    if (!emailMessage) {
      alert("Please provide a message to send.");
      return;
    }
    try {
      const response = await axios.post(`/api/admin/send-email/${agreementId}/`, {
        email_message: emailMessage,
      });
      alert("Email sent successfully!");
      handleEmailChange(agreementId, "");
    } catch (error) {
      console.error("Error sending email:", error.response?.data || error);
      alert("Error sending email. Please try again.");
    }
  };

  const handleInfoChange = (agreementId, newInfo) => {
    axios
      .put(`/api/admin/update-info/${agreementId}/`, { info: newInfo })
      .then(() => {
        setAgreements((prev) =>
          prev.map((agreement) =>
            agreement.agreementId === agreementId ? { ...agreement, info: newInfo } : agreement
          )
        );
      })
      .catch((error) => {
        console.error("Error updating info:", error);
      });
  };

  return (
    <Box padding="4">
      <Box marginBottom="8">
        <Input type="file" onChange={handleFileChange} />
        <Button onClick={handleFileUpload}>Upload Payments</Button>
      </Box>

      <Table variant="simple">
        <Thead>
          <Tr>
            <Th cursor="pointer" onClick={() => handleSort("agreementId")} >#Nr#</Th>
            <Th>Name</Th>
            <Th cursor="pointer" onClick={() => handleSort("startDate")}>Start Date</Th>
            <Th cursor="pointer" onClick={() => handleSort("endDate")}>End Date</Th>
            <Th cursor="pointer" onClick={() => handleSort("status")}>Status</Th>
            <Th cursor="pointer" onClick={() => handleSort("paymentsDue")}>Due</Th>
            <Th>Instrument</Th>
            <Th cursor="pointer" onClick={() => handleSort("hasActionButton")}>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {sortedAgreements.map((agreement) => (
            <React.Fragment key={agreement.agreementId}>
              <Tr>
                <Td>{agreement.agreementId}</Td>
                <Td>
                  {agreement.user.firstName} {agreement.user.lastName} {agreement.user.phone}
                </Td>
                <Td>{agreement.startDate}</Td>
                <Td>{agreement.endDate}</Td>
                <Td>{agreement.status}</Td>
                <Td>
                  <span style={{ color: agreement.paymentsDue < 0 ? "red" : "inherit" }}>
                    {agreement.paymentsDue}€
                  </span>
                </Td>
                <Td>
                  {agreement.instrument.brand} {agreement.instrument.model} ({agreement.instrument.color})
                </Td>
                <Td>
                  {agreement.status === "Created" && (
                    <Button mr={5}>Set contract Signed</Button>
                  )}
                  {["Active", "Test", "EndingSoon", "Ended"].includes(agreement.status) && (
                    <Button mr={1} mt={1}>
                      Set instrument Returned
                    </Button>
                  )}
                  <Textarea
                    placeholder="Short email message"
                    value={emailMessages[agreement.agreementId] || ""}
                    onChange={(e) => handleEmailChange(agreement.agreementId, e.target.value)}
                  />
                  <Button
                    mt={2}
                    colorScheme="blue"
                    onClick={() => handleSendEmail(agreement.agreementId)}
                  >
                    Send
                  </Button>
                </Td>
              </Tr>

              <Tr>
                <Td colSpan={8}>
                  <Box padding="2" backgroundColor="#f5f5f5" borderRadius="md">
                    <strong>Info:</strong>
                    <Textarea
                      value={agreement.info || ""}
                      placeholder="Update info..."
                      size="sm"
                      onChange={(e) => {
                        setAgreements((prev) =>
                          prev.map((item) =>
                            item.agreementId === agreement.agreementId
                              ? { ...item, info: e.target.value }
                              : item
                          )
                        );
                      }}
                      onBlur={(e) => handleInfoChange(agreement.agreementId, e.target.value)}
                    />
                  </Box>
                </Td>
              </Tr>
            </React.Fragment>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default AdminDashboard;
