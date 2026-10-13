import { NavLink, Outlet } from 'react-router-dom';
import { canReadTasks, lessonDay } from '../lib/lesson.js';

export default function AppLayout() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header__identity">
          <NavLink to="/" className="app-header__brand">Todo App</NavLink>
          <span className="app-header__user">Week 1 · Day {lessonDay}</span>
        </div>
        <nav className="main-nav" aria-label="Main navigation">
          <NavLink to="/" end className="main-nav__link">Home</NavLink>
          {canReadTasks ? (
            <NavLink to="/tasks" className="main-nav__link">My Tasks</NavLink>
          ) : (
            <button className="main-nav__button" disabled title="Task routes start on Day 2">My Tasks · Day 2</button>
          )}
        </nav>
      </header>
      <main className="app-main"><Outlet /></main>
      <footer className="app-footer"><p>Level 4 · React + Flask · In-memory tasks</p></footer>
    </div>
  );
}
