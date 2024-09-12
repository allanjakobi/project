import React from 'react';
import RegisterForm from '../components/RegisterForm';

<meta name="csrf-token" content="{{ csrf_token }}"></meta>

const RegisterPage = () => {
    return (
        <div>
            <h1>Register</h1>
            <RegisterForm />
        </div>
    );
};

export default RegisterPage;
