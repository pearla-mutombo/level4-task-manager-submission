import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App.jsx';
import * as service from './lib/taskService.js';

vi.mock('./lib/taskService.js', () => ({
  getHealth: vi.fn(), getTasks: vi.fn(), getTask: vi.fn(), createTask: vi.fn(), updateTask: vi.fn(), removeTask: vi.fn(),
}));

const task = { id: 7, title: 'Learn Flask', is_complete: false, created_at: '2026-10-12T12:00:00+00:00' };
function showApp(route = '/tasks') {
  return render(<MemoryRouter initialEntries={[route]}><App /></MemoryRouter>);
}

beforeEach(() => {
  vi.resetAllMocks();
  service.getHealth.mockResolvedValue({ status: 'ok', message: 'Hello from Flask' });
  service.getTasks.mockResolvedValue([task]);
  service.getTask.mockResolvedValue(task);
});

describe('prepared application workflows', () => {
  it('displays the Flask health response on the home page', async () => {
    showApp('/');
    expect(await screen.findByText('Hello from Flask')).toBeInTheDocument();
    expect(screen.getByText('ok')).toBeInTheDocument();
  });

  it('creates, filters, completes, and deletes using returned API data', async () => {
    const user = userEvent.setup();
    const created = { ...task, id: 8, title: 'API normalized title' };
    service.createTask.mockResolvedValue(created);
    service.updateTask.mockResolvedValue({ ...created, is_complete: true });
    service.removeTask.mockResolvedValue(undefined);
    showApp();
    await screen.findByRole('link', { name: 'Learn Flask' });
    await user.type(screen.getByRole('textbox', { name: 'Task title' }), '  New task  ');
    await user.click(screen.getByRole('button', { name: 'Add task' }));
    expect(service.createTask).toHaveBeenCalledWith('New task');
    const row = await screen.findByRole('link', { name: 'API normalized title' });
    expect(row).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: 'Task title' })).toHaveValue('');
    await user.click(screen.getByRole('button', { name: 'completed' }));
    expect(screen.getByText('No completed tasks')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'all', exact: true }));
    await user.click(screen.getByRole('checkbox', { name: 'Mark API normalized title as complete' }));
    expect(service.updateTask).toHaveBeenCalledWith(8, { is_complete: true });
    await waitFor(() => expect(screen.getByRole('checkbox', { name: 'Mark API normalized title as active' })).toBeChecked());
    await user.click(screen.getByRole('button', { name: 'Delete API normalized title' }));
    await waitFor(() => expect(screen.queryByRole('link', { name: 'API normalized title' })).not.toBeInTheDocument());
    expect(service.removeTask).toHaveBeenCalledWith(8);
  });

  it('retains a task and releases its controls after a failed mutation', async () => {
    const user = userEvent.setup();
    service.updateTask.mockRejectedValueOnce({ response: { data: { error: 'Practice failure' } } });
    service.updateTask.mockResolvedValueOnce({ ...task, is_complete: true });
    showApp();
    const checkbox = await screen.findByRole('checkbox', { name: 'Mark Learn Flask as complete' });
    await user.click(checkbox);
    expect(await screen.findByRole('alert')).toHaveTextContent('Practice failure');
    expect(checkbox).not.toBeChecked();
    expect(checkbox).not.toBeDisabled();
    await user.click(checkbox);
    await waitFor(() => expect(screen.getByRole('checkbox', { name: 'Mark Learn Flask as active' })).toBeChecked());
  });

  it('shows empty state, then a backend error with a working retry', async () => {
    service.getTasks.mockResolvedValue([]);
    const empty = showApp();
    expect(await screen.findByText('No tasks yet')).toBeInTheDocument();
    empty.unmount();
    service.getTasks.mockRejectedValueOnce(new Error('offline'));
    service.getTasks.mockResolvedValueOnce([task]);
    showApp();
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not reach the Flask API');
    expect(screen.getByRole('button', { name: 'Add task' })).toBeDisabled();
    await userEvent.click(screen.getByRole('button', { name: 'Retry loading tasks' }));
    expect(await screen.findByRole('link', { name: 'Learn Flask' })).toBeInTheDocument();
  });

  it('displays loading and prevents creation until the first list request completes', async () => {
    let finish;
    service.getTasks.mockReturnValue(new Promise((resolve) => { finish = resolve; }));
    showApp();
    expect(screen.getByRole('status')).toHaveTextContent('Loading your tasks');
    expect(screen.getByRole('textbox', { name: 'Task title' })).toBeDisabled();
    await act(async () => { finish([task]); });
    expect(await screen.findByRole('link', { name: 'Learn Flask' })).toBeInTheDocument();
  });

  it('reads details, edits a task, and reloads the saved result', async () => {
    const user = userEvent.setup();
    const saved = { ...task, title: 'Explain Flask', is_complete: true };
    service.updateTask.mockResolvedValue(saved);
    service.getTask.mockResolvedValueOnce(task).mockResolvedValueOnce(task).mockResolvedValueOnce(saved);
    showApp();
    await user.click(await screen.findByRole('link', { name: 'Learn Flask' }));
    expect(await screen.findByRole('heading', { name: 'Learn Flask' })).toBeInTheDocument();
    await user.click(screen.getByRole('link', { name: 'Edit task' }));
    const title = await screen.findByRole('textbox', { name: 'Task title' });
    await user.clear(title);
    await user.type(title, '  Explain Flask  ');
    await user.click(screen.getByRole('checkbox', { name: 'Mark this task as completed' }));
    await user.click(screen.getByRole('button', { name: 'Save changes' }));
    expect(service.updateTask).toHaveBeenCalledWith(7, { title: 'Explain Flask', is_complete: true });
    expect(await screen.findByRole('heading', { name: 'Explain Flask' })).toBeInTheDocument();
    expect(screen.getByRole('status')).toHaveTextContent('Task updated successfully');
    await user.click(screen.getByRole('link', { name: /Return to tasks/ }));
    expect(await screen.findByRole('heading', { name: 'My Tasks' })).toBeInTheDocument();
  });

  it('preserves failed form input for correction and retry', async () => {
    const user = userEvent.setup();
    service.createTask.mockRejectedValue({ response: { data: { error: 'Title rejected' } } });
    showApp();
    await screen.findByRole('link', { name: 'Learn Flask' });
    const input = screen.getByRole('textbox', { name: 'Task title' });
    await user.type(input, 'Try again');
    await user.click(screen.getByRole('button', { name: 'Add task' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Title rejected');
    expect(input).toHaveValue('Try again');
    expect(input).not.toBeDisabled();
  });

  it('handles a missing direct-route task as a recoverable error', async () => {
    service.getTask.mockRejectedValue({ response: { data: { error: 'Task not found.' } } });
    showApp('/tasks/999');
    expect(await screen.findByRole('heading', { name: 'Task unavailable' })).toBeInTheDocument();
    expect(screen.getByRole('alert')).toHaveTextContent('Task not found.');
    expect(screen.getByRole('link', { name: /Return to tasks/ })).toHaveAttribute('href', '/tasks');
  });

  it('rejects whitespace-only edits without sending an API update', async () => {
    showApp('/tasks/7/edit');
    const input = await screen.findByRole('textbox', { name: 'Task title' });
    fireEvent.change(input, { target: { value: '   ' } });
    fireEvent.submit(input.closest('form'));
    expect(screen.getByRole('alert')).toHaveTextContent('Task title cannot be empty');
    expect(service.updateTask).not.toHaveBeenCalled();
  });
});
