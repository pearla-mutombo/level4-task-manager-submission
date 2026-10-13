import { useState } from 'react';
import TaskItem from './TaskItem.jsx';
import NewTaskForm from './NewTaskForm.jsx';
import { useTasks } from '../../hooks/useTasks.js';
import { canChangeTasks } from '../../lib/lesson.js';

export default function TaskList() {
  const [filter, setFilter] = useState('all');
  const [actionError, setActionError] = useState('');
  const { tasks, loading, error, addTask, toggleTask, deleteTask, retry } = useTasks();

  async function handleAddTask(title) {
    setActionError('');
    await addTask(title);
  }

  async function handleToggleComplete(id, isComplete) {
    setActionError('');
    try { await toggleTask(id, isComplete); }
    catch (failure) { setActionError(`Could not update the task: ${failure.message}`); }
  }

  async function handleDeleteTask(id) {
    setActionError('');
    try { await deleteTask(id); }
    catch (failure) { setActionError(`Could not delete the task: ${failure.message}`); }
  }

  const completedTasks = tasks.filter((task) => task.is_complete).length;
  const visibleTasks = tasks.filter((task) => {
    if (filter === 'active') return !task.is_complete;
    if (filter === 'completed') return task.is_complete;
    return true;
  });

  return (
    <section className="card task-panel">
      <div className="task-panel__heading">
        <div><p className="eyebrow">Task list</p><h2>Today’s focus</h2></div>
        {!loading && !error && tasks.length > 0 && (
          <p className="task-summary" aria-live="polite"><strong>{completedTasks}</strong> of <strong>{tasks.length}</strong> complete</p>
        )}
      </div>
      {!canChangeTasks && <p className="lesson-notice">Read and create today. Completion, editing, and deletion start on Day 3.</p>}
      <NewTaskForm onAddTask={handleAddTask} disabled={loading || Boolean(error)} />
      <div className="task-filter" aria-label="Filter tasks">
        {['all', 'active', 'completed'].map((filterName) => (
          <button key={filterName} type="button" className={`task-filter__button${filter === filterName ? ' task-filter__button--active' : ''}`}
            onClick={() => setFilter(filterName)} aria-pressed={filter === filterName}>{filterName}</button>
        ))}
      </div>
      {(error || actionError) && <p className="error-text" role="alert">{error || actionError}</p>}
      {error && <button type="button" className="task-edit-form__cancel" onClick={retry}>Retry loading tasks</button>}
      {loading ? (
        <div className="loading-state" role="status">Loading your tasks…</div>
      ) : !error && tasks.length === 0 ? (
        <div className="empty-state"><div><strong>No tasks yet</strong><p>Add your first task above to get started.</p></div></div>
      ) : !error && visibleTasks.length === 0 ? (
        <div className="empty-state"><div><strong>No {filter} tasks</strong><p>Choose All to see your other tasks.</p></div></div>
      ) : !error ? (
        <ul className="task-list">
          {visibleTasks.map((task) => <TaskItem key={task.id} task={task} canChange={canChangeTasks} onToggleComplete={handleToggleComplete} onDelete={handleDeleteTask} />)}
        </ul>
      ) : null}
    </section>
  );
}
