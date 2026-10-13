import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getHealth } from '../lib/taskService.js';
import { apiBaseUrl, isCanceled, requestError } from '../lib/apiClient.js';
import { canReadTasks } from '../lib/lesson.js';

export default function HomePage() {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    let active = true;
    async function loadHealth() {
      setLoading(true);
      setError('');
      try {
        const data = await getHealth(controller.signal);
        if (active) setHealth(data);
      } catch (failure) {
        if (active && !isCanceled(failure)) setError(requestError(failure));
      } finally {
        if (active) setLoading(false);
      }
    }
    loadHealth();
    return () => { active = false; controller.abort(); };
  }, [attempt]);

  return (
    <section className="home-page">
      <p className="eyebrow">A focused space for your work</p>
      <h1 className="home-page__title">Make room for what matters.</h1>
      <p className="home-page__description">
        Capture your next task, track your progress, and follow each request from React to your Flask backend.
      </p>
      <div className="connection-card" aria-live="polite">
        <p className="eyebrow">Backend connection</p>
        {loading ? <p role="status">Connecting to Flask…</p> : error ? (
          <>
            <p className="error-text" role="alert">{error}</p>
            <button type="button" className="task-edit-form__cancel" onClick={() => setAttempt((value) => value + 1)}>Retry connection</button>
          </>
        ) : (
          <>
            <p className="connection-card__message">{health?.message}</p>
            <p>Status: <strong>{health?.status}</strong></p>
          </>
        )}
        <code>GET {apiBaseUrl}/health</code>
      </div>
      {canReadTasks ? <Link className="home-page__action" to="/tasks">View my tasks</Link> : (
        <p className="lesson-notice">Today we connect React to Flask. Task routes begin on Day 2.</p>
      )}
    </section>
  );
}
