import { useEffect, useState } from 'react';
import { getTask } from '../lib/taskService.js';
import { isCanceled, requestError } from '../lib/apiClient.js';

export function useTask(taskId) {
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    let active = true;
    async function loadTask() {
      setLoading(true);
      setError('');
      setTask(null);
      try {
        if (!/^[1-9]\d*$/.test(taskId ?? '')) throw new Error('invalid-id');
        const data = await getTask(taskId, controller.signal);
        if (active) setTask(data);
      } catch (failure) {
        if (active && !isCanceled(failure)) {
          setError(failure.message === 'invalid-id' ? 'Task not found.' : requestError(failure));
        }
      } finally {
        if (active) setLoading(false);
      }
    }
    loadTask();
    return () => { active = false; controller.abort(); };
  }, [taskId, attempt]);

  return { task, loading, error, retry: () => setAttempt((value) => value + 1) };
}
