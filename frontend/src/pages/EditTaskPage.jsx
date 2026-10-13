import { Link, useNavigate, useParams } from 'react-router-dom';
import EditTaskForm from '../components/tasks/EditTaskForm.jsx';
import { useTask } from '../hooks/useTask.js';
import { updateTask } from '../lib/taskService.js';
import { requestError } from '../lib/apiClient.js';

export default function EditTaskPage() {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const { task, loading, error, retry } = useTask(taskId);
  async function handleSave(values) {
    let updated;
    try {
      updated = await updateTask(task.id, { title: values.title, is_complete: values.is_complete });
    } catch (failure) { throw new Error(requestError(failure)); }
    navigate(`/tasks/${updated.id}`, { replace: true, state: { taskUpdated: true } });
  }
  if (loading) return <div className="loading-state" role="status">Loading task…</div>;
  if (error || !task) return (
    <section className="task-details">
      <h1 className="task-details__title">Task unavailable</h1>
      <p className="error-text" role="alert">{error || 'Task not found.'}</p>
      <div className="task-details-actions">
        <button type="button" className="task-edit-form__cancel" onClick={retry}>Try again</button>
        <Link className="task-details__back" to="/tasks">← Return to tasks</Link>
      </div>
    </section>
  );
  return (
    <section className="page">
      <header className="page__header">
        <p className="eyebrow">Your workspace</p>
        <h1 className="page__title">Edit task</h1>
        <p className="page__description">Update the title or completion status of your task.</p>
      </header>
      <div className="card task-edit-card">
        <EditTaskForm key={task.id} task={task} onSave={handleSave} onCancel={() => navigate(`/tasks/${task.id}`)} />
      </div>
    </section>
  );
}
