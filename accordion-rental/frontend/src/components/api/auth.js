import axios from 'axios';

export const registerUser = (userData) => {
    return axios.post('http://127.0.0.1:8000/admin/auth/user/add/', userData);
};

export const loginUser = (userData) => {
    return axios.post('http://127.0.0.1:8000/api/login/', userData);
};
