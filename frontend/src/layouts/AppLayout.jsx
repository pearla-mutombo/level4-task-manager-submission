import { useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";
import { canReadTasks, lessonDay } from "../lib/lesson.js";

export default function AppLayout() {
  const { user, loading, signOut } = useAuth();
  const navigate = useNavigate();

  const [signingOut, setSigningOut] = useState(false);
  const [logoutError, setLogoutError] = useState("");

  async function handleLogout() {
    setSigningOut(true);
    setLogoutError("");

    try {
      const { error } = await signOut();

      if (error) {
        setLogoutError(error.message);
        return;
      }

      navigate("/login", { replace: true });
    } catch {
      setLogoutError("Unable to log out. Please try again.");
    } finally {
      setSigningOut(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header__identity">
          <NavLink to="/" className="app-header__brand">
            Todo App
          </NavLink>

          <span className="app-header__user">Week 1 · Day {lessonDay}</span>

          {user && (
            <span className="app-header__user">Signed in as: {user.email}</span>
          )}
        </div>

        <nav className="main-nav" aria-label="Main navigation">
          <NavLink to="/" end className="main-nav__link">
            Home
          </NavLink>

          {canReadTasks ? (
            <NavLink to="/tasks" className="main-nav__link">
              My Tasks
            </NavLink>
          ) : (
            <button
              className="main-nav__button"
              disabled
              title="Task routes start on Day 2">
              My Tasks · Day 2
            </button>
          )}

          {!loading && !user && (
            <>
              <NavLink to="/login" className="main-nav__link">
                Log In
              </NavLink>

              <NavLink to="/register" className="main-nav__link">
                Register
              </NavLink>
            </>
          )}

          {!loading && user && (
            <button
              type="button"
              className="main-nav__button"
              onClick={handleLogout}
              disabled={signingOut}>
              {signingOut ? "Logging Out..." : "Log Out"}
            </button>
          )}
        </nav>
      </header>

      {logoutError && (
        <div className="alert alert-danger m-3" role="alert">
          {logoutError}
        </div>
      )}

      <main className="app-main">
        <Outlet />
      </main>

      <footer className="app-footer">
        <p>Level 4 · React + Flask · PostgreSQL Task Manager</p>
      </footer>
    </div>
  );
}
// What i've added:

// User status - Navigation
// Signed out	  Home, My Tasks, Log In, Register
// Signed in	  Home, My Tasks, Log Out
// Logging out	Log Out button temporarily disabled

// When signed in, the header will also display the user's email address.

// The logout button calls Supabase Authentication to sign out and then redirects the user
// to /login.
