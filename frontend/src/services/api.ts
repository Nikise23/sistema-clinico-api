/// <reference types="react-scripts" />
import axios from 'axios';
import { AuthResponse, LoginRequest, RegisterRequest, Patient, PatientCreate } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Patients API
export const patientsAPI = {
  getAll: async (params?: { skip?: number; limit?: number; search?: string }) => {
    const response = await api.get('/patients', { params });
    return response.data;
  },

  getById: async (id: string): Promise<Patient> => {
    const response = await api.get(`/patients/${id}`);
    return response.data;
  },

  create: async (data: PatientCreate): Promise<Patient> => {
    const response = await api.post('/patients', data);
    return response.data;
  },

  update: async (id: string, data: Partial<PatientCreate>): Promise<Patient> => {
    const response = await api.put(`/patients/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/patients/${id}`);
  },
  getSummary: async (id: string) => {
    const response = await api.get(`/patients/${id}/summary`);
    return response.data;
  },
};

export default api;