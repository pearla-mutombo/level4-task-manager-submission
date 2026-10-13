import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import NewTaskForm from './NewTaskForm.jsx';

it('counts Unicode code points like Python when validating titles', async () => {
  const onAddTask = vi.fn().mockResolvedValue(undefined);
  render(<NewTaskForm onAddTask={onAddTask} />);
  const input = screen.getByRole('textbox', { name: 'Task title' });
  fireEvent.change(input, { target: { value: '😀'.repeat(80) } });
  fireEvent.submit(input.closest('form'));
  await waitFor(() => expect(onAddTask).toHaveBeenCalledWith('😀'.repeat(80)));
  await waitFor(() => expect(input).toHaveValue(''));
  fireEvent.change(input, { target: { value: '😀'.repeat(81) } });
  fireEvent.submit(input.closest('form'));
  expect(screen.getByRole('alert')).toHaveTextContent('cannot exceed 80 characters');
  expect(onAddTask).toHaveBeenCalledTimes(1);
});
