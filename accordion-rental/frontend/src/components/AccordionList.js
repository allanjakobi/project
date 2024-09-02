// src/components/AccordionList.js
import React, { useEffect, useState } from 'react';

const AccordionList = () => {
  const [accordions, setAccordions] = useState([]);

  useEffect(() => {
    fetch('/api/accordions')
      .then(response => response.json())
      .then(data => setAccordions(data))
      .catch(error => console.error('Error fetching accordions:', error));
  }, []);

  return (
    <div>
      <h2>Available Accordions</h2>
      <ul>
        {accordions.map(accordion => (
          <li key={accordion.id}>
            {accordion.brand} {accordion.model} - {accordion.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AccordionList;
