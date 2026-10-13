import axios from 'axios';

export const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5001/api';

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000,
  headers: { Accept: 'application/json' },
});

export function requestError(error) {
  if (error.response?.data?.error) return error.response.data.error;
  if (error.code === 'ECONNABORTED') return 'The API took too long to respond. Try again.';
  return 'Could not reach the Flask API. Check that the backend is running and its allowed origin matches this page.';
}

export function isCanceled(error) {
  return axios.isCancel(error) || error.code === 'ERR_CANCELED';
}
