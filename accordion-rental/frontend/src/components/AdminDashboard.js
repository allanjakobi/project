// src/components/AdminDashboard.js
import React, { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [accordions, setAccordions] = useState([]);

  useEffect(() => {
    fetch('/api/admin/accordions')
      .then(response => response.json())
      .then(data => setAccordions(data))
      .catch(error => console.error('Error fetching accordions:', error));
  }, []);

  return (
    <div>
      <h2>Admin Dashboard</h2>
      <ul>
        {accordions.map(accordion => (
          <li key={accordion.id}>
            {accordion.brand} {accordion.model} - {accordion.status}
          </li>
        ))}
      </ul>
      {/* Add more admin features here */}
    </div>
  );
};

export default AdminDashboard;
