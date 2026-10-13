import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function TaskItem({ task, canChange, onToggleComplete, onDelete }) {
  const [working, setWorking] = useState(false);
  async function handleToggle() {
    setWorking(true);
    try { await onToggleComplete(task.id, !task.is_complete); }
    finally { setWorking(false); }
  }
  async function handleDelete() {
    setWorking(true);
    try { await onDelete(task.id); }
    finally { setWorking(false); }
  }
  const explanation = !canChange ? 'Available on Day 3' : undefined;
  return (
    <li className="task-item" aria-busy={working}>
      <div className="task-item__content">
        <input type="checkbox" checked={task.is_complete} onChange={handleToggle} disabled={working || !canChange}
          title={explanation} aria-label={`Mark ${task.title} as ${task.is_complete ? 'active' : 'complete'}`} />
        <Link className="task-item__link" to={`/tasks/${task.id}`}>
          <span className={`task-item__title${task.is_complete ? ' task-item__title--done' : ''}`}>{task.title}</span>
        </Link>
      </div>
      <button type="button" className="task-item__delete" onClick={handleDelete} disabled={working || !canChange}
        title={explanation} aria-label={`Delete ${task.title}`}>✕</button>
    </li>
  );
}
