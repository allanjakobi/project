import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const ProfileForm = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    country: 'Estonia',
    province: '',
    municipality: '',
    settlement: '',
    street: '',
    house: '',
    apartment: '',
    phone: '+372',
    language: 'Eesti',
  });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  // Fetch user data from backend
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/profile/', {
          credentials: 'include',
        });
        const data = await response.json();
        setFormData(data);
      } catch (error) {
        console.error('Error fetching profile data', error);
      }
    };
    fetchProfileData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/profile/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
        credentials: 'include',
      });

      if (response.ok) {
        navigate('/dashboard');  // Redirect to dashboard after successful update
      } else {
        const errorData = await response.json();
        setErrors(errorData);
      }
    } catch (error) {
      console.error('Error updating profile', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Input fields for profile data */}
      <button type="submit">Save Profile</button>
      {errors && <p>{errors}</p>}
    </form>
  );
};

export default ProfileForm;
