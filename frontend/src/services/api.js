import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('cyberguard_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Optional auto-logout on unauthorized
      if (window.location.pathname !== '/login') {
        localStorage.removeItem('cyberguard_token');
        localStorage.removeItem('cyberguard_user');
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
};

export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
};

export const eventsAPI = {
  list: (params) => api.get('/events', { params }),
  ingest: (data) => api.post('/events', data),
};

export const alertsAPI = {
  list: (params) => api.get('/alerts', { params }),
  get: (id) => api.get(`/alerts/${id}`),
};

export const incidentsAPI = {
  list: (params) => api.get('/incidents', { params }),
  get: (id) => api.get(`/incidents/${id}`),
};

export const investigationAPI = {
  investigate: (incidentId, data = {}) => api.post(`/investigate/${incidentId}`, data),
};

export const ragAPI = {
  search: (query, top_k = 5) => api.post('/rag/search', { query, top_k }),
};

export const responseAPI = {
  validate: (data) => api.post('/response/validate', data),
  simulate: (data) => api.post('/response/simulate', data),
};

export const auditAPI = {
  list: () => api.get('/audit'),
};

export const reportsAPI = {
  get: (incidentId) => api.get(`/reports/${incidentId}`),
};

export default api;
