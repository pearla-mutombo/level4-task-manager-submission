import { act, renderHook, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import { useTask } from './useTask.js';
import { getTask } from '../lib/taskService.js';

vi.mock('../lib/taskService.js', () => ({ getTask: vi.fn() }));
beforeEach(() => { vi.resetAllMocks(); });

it('aborts an obsolete task read and ignores its late result', async () => {
  let finishOld;
  getTask.mockReturnValueOnce(new Promise((resolve) => { finishOld = resolve; }));
  getTask.mockResolvedValueOnce({ id: 2, title: 'Current task' });
  const { result, rerender, unmount } = renderHook(({ id }) => useTask(id), { initialProps: { id: '1' } });
  const firstSignal = getTask.mock.calls[0][1];
  rerender({ id: '2' });
  expect(firstSignal.aborted).toBe(true);
  await waitFor(() => expect(result.current.task?.id).toBe(2));
  await act(async () => { finishOld({ id: 1, title: 'Obsolete task' }); });
  expect(result.current.task.id).toBe(2);
  const currentSignal = getTask.mock.calls[1][1];
  unmount();
  expect(currentSignal.aborted).toBe(true);
});
