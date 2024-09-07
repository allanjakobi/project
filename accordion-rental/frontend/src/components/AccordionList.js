// AccordionList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AccordionList = () => {
  const [instruments, setInstruments] = useState([]);
  const [loading, setLoading] = useState(true); // For showing a loading state
  const [error, setError] = useState(null);

  // Fetch data from the API
  useEffect(() => {
    const fetchInstruments = async () => {
      try {
        const response = await axios.get('/api/available-instruments/');
        setInstruments(response.data);
      } catch (err) {
        setError(err);
        console.error("Error fetching available instruments", err);
      }
    };
  
    fetchInstruments();
  }, []);

  if (error) {
    return <div>Error fetching available instruments: {error.message}</div>;
  }

  

  return (
    <div>
      <h1>Available Instruments</h1>
      <ul>
        {instruments.map(instrument => (
          <li key={instrument.instrumentId}>
          <img src={instrument.thumbnail_image} alt={`${instrument.modelId.brand} ${instrument.modelId.model}`} />

          {/* Access model data from modelId */}
          <h2>{instrument.modelId.brand} {instrument.modelId.model}</h2>
          <p>Color: {instrument.color}</p>
          <p>Serial: {instrument.serial}</p>
          <p>Status: {instrument.status}</p>
          <p>Price Level: {instrument.price_level}</p>
          <h3>Model Details:</h3>
          <p>Keys: {instrument.modelId.keys}</p>
          <p>Weight: {instrument.modelId.weight} kg</p>
          <p>Dimensions: {instrument.modelId.height}cm x {instrument.modelId.width}cm</p>
          <p>Reeds (Right/Left): {instrument.modelId.reedsR}/{instrument.modelId.reedsL}</p>
          <p>New Price: ${instrument.modelId.newPrice}</p>
          <p>Used Price: ${instrument.modelId.usedPrice}</p>
          <h3>Additional Info:</h3>
          <p>{instrument.info_est}</p>
          <p>{instrument.info_eng}</p>
        </li>
        ))}
      </ul>
    </div>
  );
};

export default AccordionList;
