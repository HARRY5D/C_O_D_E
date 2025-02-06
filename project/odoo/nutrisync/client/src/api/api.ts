import axios, { AxiosRequestConfig, AxiosError } from 'axios';
import { toast } from "sonner"

const backendURL = '/api';
const api = axios.create({
  baseURL: backendURL,
  headers: {
    'Content-Type': 'application/json',
  },
  validateStatus: (status) => {
    return status >= 200 && status < 300;
  },
});

let accessToken: string | null = null;

// Axios request interceptor: Attach access token to headers
api.interceptors.request.use(
  (config: AxiosRequestConfig): AxiosRequestConfig => {
    if (!accessToken) {
      accessToken = localStorage.getItem('accessToken');
    }
    if (accessToken && config.headers) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error: AxiosError): Promise<AxiosError> => {
    toast.error("Request failed. Please check your connection.");
    return Promise.reject(error);
  }
);

// Axios response interceptor: Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError): Promise<any> => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const { data } = await axios.post<{ accessToken: string }>(`${backendURL}/auth/refresh`, {
          refreshToken: localStorage.getItem('refreshToken'),
        });
        accessToken = data.accessToken;
        localStorage.setItem('accessToken', accessToken);

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${accessToken}`;
        }
        return api(originalRequest);
      } catch (err) {
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('accessToken');
        accessToken = null;
        window.location.href = '/login';
        toast.error("Session expired. Please login again.");
        return Promise.reject(err);
      }
    }

    // Handle other error cases
    if (error.response?.status === 404) {
      toast.error("Resource not found.");
    } else if (error.response?.status === 500) {
      toast.error("Server error. Please try again later.");
    } else if (!error.response) {
      toast.error("Network error. Please check your connection.");
    }

    return Promise.reject(error);
  }
);

export default api;