import { useCallback, useEffect, useState } from 'react';
import { createTask, getTasks, removeTask, updateTask } from '../lib/taskService.js';
import { isCanceled, requestError } from '../lib/apiClient.js';

export function useTasks() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    let active = true;
    async function loadTasks() {
      setLoading(true);
      setError('');
      try {
        const data = await getTasks(controller.signal);
        if (active) setTasks(data);
      } catch (failure) {
        if (active && !isCanceled(failure)) setError(requestError(failure));
      } finally {
        if (active) setLoading(false);
      }
    }
    loadTasks();
    return () => { active = false; controller.abort(); };
  }, [attempt]);

  const addTask = useCallback(async (title) => {
    try {
      const created = await createTask(title);
      setTasks((current) => [created, ...current]);
    } catch (failure) {
      throw new Error(requestError(failure));
    }
  }, []);

  const toggleTask = useCallback(async (id, isComplete) => {
    try {
      const updated = await updateTask(id, { is_complete: isComplete });
      setTasks((current) => current.map((task) => task.id === id ? updated : task));
    } catch (failure) {
      throw new Error(requestError(failure));
    }
  }, []);

  const deleteTask = useCallback(async (id) => {
    try {
      await removeTask(id);
      setTasks((current) => current.filter((task) => task.id !== id));
    } catch (failure) {
      throw new Error(requestError(failure));
    }
  }, []);

  const retry = useCallback(() => setAttempt((value) => value + 1), []);
  return { tasks, loading, error, addTask, toggleTask, deleteTask, retry };
}
