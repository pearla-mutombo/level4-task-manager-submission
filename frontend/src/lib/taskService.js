import { apiClient } from './apiClient.js';

// All business-data requests pass through Flask; no direct database client.
export async function getHealth(signal) {
  const response = await apiClient.get('/health', { signal });
  return response.data;
}

export async function getTasks(signal) {
  const response = await apiClient.get('/tasks', { signal });
  return response.data;
}

export async function getTask(id, signal) {
  const response = await apiClient.get(`/tasks/${id}`, { signal });
  return response.data;
}

export async function createTask(title) {
  const response = await apiClient.post('/tasks', { title });
  return response.data;
}

export async function updateTask(id, changes) {
  const response = await apiClient.patch(`/tasks/${id}`, changes);
  return response.data;
}

export async function removeTask(id) {
  await apiClient.delete(`/tasks/${id}`);
}
