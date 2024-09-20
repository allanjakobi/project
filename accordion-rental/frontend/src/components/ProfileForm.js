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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/profile/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
        credentials: 'include',  // Include session cookie
      });

      if (response.ok) {
        navigate('/dashboard');  // Redirect to dashboard on success
      } else {
        const errorData = await response.json();
        setErrors(errorData);  // Set validation errors
      }
    } catch (error) {
      console.error('Error updating profile', error);
    }
  };

  // Fetch user data from backend
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/profile/', {
          credentials: 'include',
        });
        const data = await response.json();

        if (data && typeof data === 'object') {
          setFormData((prevState) => ({
            ...prevState,
            firstName: data.firstName || '',
            lastName: data.lastName || '',
            country: data.country || 'Estonia',
            province: data.province || '',
            municipality: data.municipality || '',
            settlement: data.settlement || '',
            street: data.street || '',
            house: data.house || '',
            apartment: data.apartment || '',
            phone: data.phone || '+372',
            language: data.language || 'Eesti',
          }));
        }
      } catch (error) {
        console.error('Error fetching profile data', error);
      }
    };

    fetchProfileData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="firstName"
        value={formData.firstName}
        onChange={handleInputChange}
        placeholder="First Name"
      />
      <input
        type="text"
        name="lastName"
        value={formData.lastName}
        onChange={handleInputChange}
        placeholder="Last Name"
      />
      <input
        type="text"
        name="country"
        value={formData.country}
        onChange={handleInputChange}
        placeholder="Country"
      />
      <input
        type="text"
        name="province"
        value={formData.province}
        onChange={handleInputChange}
        placeholder="Province"
      />
      <input
        type="text"
        name="municipality"
        value={formData.municipality}
        onChange={handleInputChange}
        placeholder="Municipality"
      />
      <input
        type="text"
        name="settlement"
        value={formData.settlement}
        onChange={handleInputChange}
        placeholder="Settlement"
      />
      <input
        type="text"
        name="street"
        value={formData.street}
        onChange={handleInputChange}
        placeholder="Street"
      />
      <input
        type="text"
        name="house"
        value={formData.house}
        onChange={handleInputChange}
        placeholder="House"
      />
      <input
        type="text"
        name="apartment"
        value={formData.apartment}
        onChange={handleInputChange}
        placeholder="Apartment"
      />
      <input
        type="text"
        name="phone"
        value={formData.phone}
        onChange={handleInputChange}
        placeholder="Phone"
      />
      <input
        type="text"
        name="language"
        value={formData.language}
        onChange={handleInputChange}
        placeholder="Language"
      />
      <button type="submit">Save Profile</button>
      {errors && Object.keys(errors).map((key) => (
        <p key={key}>{errors[key]}</p>
      ))}
    </form>
  );
};

export default ProfileForm;
