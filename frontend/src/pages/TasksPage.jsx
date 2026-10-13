import TaskList from '../components/tasks/TaskList.jsx';

export default function TasksPage() {
  return (
    <section className="page">
      <header className="page__header">
        <p className="eyebrow">Your workspace</p>
        <h1 className="page__title">My Tasks</h1>
        <p className="page__description">Add a task, track its progress, or open it for more details.</p>
      </header>
      <TaskList />
    </section>
  );
}
