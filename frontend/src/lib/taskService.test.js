import { beforeEach, expect, it, vi } from 'vitest';
import { apiClient } from './apiClient.js';
import { createTask, getHealth, getTask, getTasks, removeTask, updateTask } from './taskService.js';

vi.mock('./apiClient.js', () => ({ apiClient: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() } }));
beforeEach(() => {
  vi.resetAllMocks();
  apiClient.get.mockResolvedValue({ data: { status: 'ok' } });
  apiClient.post.mockResolvedValue({ data: { id: 1 } });
  apiClient.patch.mockResolvedValue({ data: { id: 1 } });
  apiClient.delete.mockResolvedValue({ status: 204, data: '' });
});

it('uses the documented paths, payloads, abort signals, and empty-delete response', async () => {
  const signal = new AbortController().signal;
  expect(await getHealth(signal)).toEqual({ status: 'ok' });
  await getTasks(signal);
  await getTask(3, signal);
  expect(apiClient.get.mock.calls).toEqual([['/health', { signal }], ['/tasks', { signal }], ['/tasks/3', { signal }]]);
  expect(await createTask('Read Python')).toEqual({ id: 1 });
  expect(apiClient.post).toHaveBeenCalledWith('/tasks', { title: 'Read Python' });
  await updateTask(3, { is_complete: true });
  expect(apiClient.patch).toHaveBeenCalledWith('/tasks/3', { is_complete: true });
  expect(await removeTask(3)).toBeUndefined();
  expect(apiClient.delete).toHaveBeenCalledWith('/tasks/3');
});
