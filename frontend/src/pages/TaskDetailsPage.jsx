import { Link, useLocation, useParams } from 'react-router-dom';
import { useTask } from '../hooks/useTask.js';
import { canChangeTasks } from '../lib/lesson.js';

export default function TaskDetailsPage() {
  const { taskId } = useParams();
  const location = useLocation();
  const { task, loading, error, retry } = useTask(taskId);
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
    <article className="task-details">
      {location.state?.taskUpdated && <p className="task-edit-notice" role="status">Task updated successfully.</p>}
      <p className="eyebrow">Task details · #{task.id}</p>
      <h1 className="task-details__title">{task.title}</h1>
      <p className="task-details__status">{task.is_complete ? 'Completed' : 'Active'}</p>
      <p className="task-details__date">Created {new Date(task.created_at).toLocaleString()}</p>
      <div className="task-details-actions">
        {canChangeTasks ? <Link className="task-edit-link" to={`/tasks/${task.id}/edit`}>Edit task</Link> : (
          <button type="button" className="task-edit-form__save" disabled title="Editing starts on Day 3">Edit task · Day 3</button>
        )}
        <Link className="task-details__back" to="/tasks">← Return to tasks</Link>
      </div>
    </article>
  );
}
