import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AccordionList = () => {
  const [instruments, setInstruments] = useState([]);
  const [error, setError] = useState(null);

  // Fetch available instruments when component mounts
  useEffect(() => {
    const fetchInstruments = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/available-instruments/', {
          headers: {
            'Accept': 'application/json',
            // Add CSRF token if needed
            // 'X-CSRFToken': csrfToken,
          },
        });
        setInstruments(response.data);
      } catch (error) {
        console.error('Error fetching available instruments', error);
        setError(error);
      }
    };

    fetchInstruments();
  }, []);

  return (
    <div>
      <h1>Available Instruments</h1>
      {error ? (
        <p>Error fetching instruments: {error.message}</p>
      ) : (
        <ul>
          {instruments.map((instrument, index) => (
            <li key={index}>{instrument.instrumentId} - {instrument.status}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AccordionList;
