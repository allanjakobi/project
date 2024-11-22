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
  useToast,
  Select,
  Checkbox,
  Link,
} from '@chakra-ui/react';

const RentalForm = ({ userId }) => {
  const location = useLocation();
  const instrument = location.state?.instrument; // Access instrument data passed from previous component
  const [rentalPeriod, setRentalPeriod] = useState(12);
  const [additionalInfo, setAdditionalInfo] = useState('');
  const [rate, setRate] = useState(null);
  const [finalRate, setFinalRate] = useState(null); // To hold the final rental rate
  const [invoiceInterval, setInvoiceInterval] = useState(1); // New state for invoice interval
  const [termsAccepted, setTermsAccepted] = useState(false); // New state for checkbox
  const navigate = useNavigate();
  const toast = useToast();

  const getTokenFromCookie = () => {
    const name = 'access_token=';
    const decodedCookie = decodeURIComponent(document.cookie); // Decode the cookie
    const cookieArr = decodedCookie.split(';'); // Split by ';' to get individual cookies
    
    // Loop through cookies to find the access_token
    for (let i = 0; i < cookieArr.length; i++) {
        let cookie = cookieArr[i].trim(); // Trim whitespace
        // Check if this cookie starts with access_token=
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length); // Return the token value
        }
    }
    return null; // Return null if token not found
  };

  const getCSRFToken = () => {
    const name = 'csrftoken'; // Adjust if your CSRF cookie has a different name
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
};

useEffect(() => {
  // Set a timeout to navigate back to the homepage after 180 seconds (3 minutes)
  const timer = setTimeout(() => {
    navigate('/');
  }, 120000); // 180000 milliseconds = 3 minutes

  // Clean up the timer if the component unmounts before the timer finishes
  return () => clearTimeout(timer);
}, [navigate]);
  

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

    // Set default invoice interval based on rental period
    const intervals = getInvoiceIntervals(rentalPeriod);
    setInvoiceInterval(intervals[0]); // Set the first valid interval as default
  }, [rentalPeriod, rate]);

  const getInvoiceIntervals = (period) => {
    const intervals = [];
    for (let i = 1; i <= period; i++) {
      if (period % i === 0) {
        intervals.push(i);
      }
    }
    return intervals;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!termsAccepted) {
        toast({
            title: "Terms not accepted",
            description: "Please confirm that you are familiar with the rental terms.",
            status: "warning",
            duration: 4000,
            isClosable: true,
        });
        return; // Prevent submission if terms are not accepted
    }

    const agreementData = {
        instrumentId: instrument.instrumentId,
        months: rentalPeriod,
        rate: finalRate, // Use the calculated rental rate
        info: additionalInfo,
        invoiceInterval: invoiceInterval, // Include invoice interval in the request
    };


    try {
      const accessToken = getTokenFromCookie();
      const csrfToken = getCSRFToken();  // Get the token from cookies
      //console.log("Access Token Retrieved:", accessToken); // Log the token

      if (!accessToken) {
            throw new Error("No access token found");
        }

        const response = await fetch('/api/agreements/', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`, // Include the token in the Authorization header
                "X-CSRFToken": csrfToken, // Include the CSRF token in the request headers

            },
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
            navigate('/contracts'); // Redirect after successful submission
        } else {
            console.error("Error details:", await response.text()); // Log detailed error message
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

  const handleTermsClick = () => {
    toast({
      title: "Basic Terms",
      description: "\n" + 
                   "1. The rental less than a month is charged as one month.\n" + 
                   "2. Late returns incur additional fees.\n" +
                   "3. The instrument must be maintained in good condition.\n" + 
                   "4. The user is responsible for any damages during the rental period.\n" +
                   "5. Early agreement terminating - 2 months additional fee.\n" +
                   "6. User is responible for tranport - returning has to be finished by the end of agreement.\n\n" + 
                   "7. Other terms apply based on signed agreements.\n\n" + 
                   "Please refer to your rental agreement for detailed terms.",
      status: "info",
      duration: 10000, // Show for 10 seconds
      isClosable: true,
    });
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
            Agreement's inputs for {instrument?.modelId.brand} {instrument?.modelId.model}
          </Text>
          <Divider />

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

          <FormControl id="invoiceInterval" isRequired>
            <FormLabel>Invoice Interval</FormLabel>
            <Select
              value={invoiceInterval}
              onChange={(e) => setInvoiceInterval(e.target.value)}
              bg="gray.50"
            >
              {getInvoiceIntervals(rentalPeriod).map((interval) => (
                <option key={interval} value={interval}>
                  {interval} month(s)
                </option>
              ))}
            </Select>
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

          <FormControl display="flex" alignItems="center">
            <Checkbox 
              isChecked={termsAccepted} 
              onChange={() => setTermsAccepted(!termsAccepted)}
            >
              I am familiar with basic rental terms
            </Checkbox>
            <Link 
              color="teal.500" 
              ml={2} 
              onClick={handleTermsClick}
              fontWeight="bold"
            >
              (View Terms)
            </Link>
          </FormControl>

          <Divider />

          <Text fontSize="lg" fontWeight="bold">Summary:</Text>
          <Text fontSize="md">Brand: {instrument?.modelId.brand}</Text>
          <Text fontSize="md">Model: {instrument?.modelId.model}</Text>
{/*           <Text fontSize="md">Price Level: {instrument?.price_level}</Text>
 */}          <Text fontSize="md">Rental Period: {rentalPeriod} months</Text>
          <Text fontSize="md">Rate: {finalRate !== null ? `${finalRate} € per month` : 'Loading...'}</Text>

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
