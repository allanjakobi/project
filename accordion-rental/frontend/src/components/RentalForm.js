// src/components/RentalForm.js
import React, { useState } from 'react';

const RentalForm = ({ accordionId }) => {
  const [rentalPeriod, setRentalPeriod] = useState(1);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`/api/rent/${accordionId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ months: rentalPeriod }),
    })
      .then(response => response.json())
      .then(data => console.log('Rental agreement created:', data))
      .catch(error => console.error('Error creating rental agreement:', error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Rental Period (months):
        <input type="number" value={rentalPeriod} onChange={(e) => setRentalPeriod(e.target.value)} min="1" />
      </label>
      <button type="submit">Submit Rental Agreement</button>
    </form>
  );
};

export default RentalForm;
