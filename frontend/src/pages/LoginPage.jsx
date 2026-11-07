import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

export default function LoginPage() {
  const { user, loading, signIn } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const { error: signInError } = await signIn(email.trim(), password);

      if (signInError) {
        setError(signInError.message);
        return;
      }

      navigate("/tasks", { replace: true });
    } catch {
      setError("Unable to sign in right now. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <p className="container py-4">Checking your session...</p>;
  }

  if (user) {
    return <Navigate to="/tasks" replace />;
  }

  return (
    <main className="container py-5" style={{ maxWidth: "480px" }}>
      <h1 className="mb-3">Log In</h1>
      <p className="text-muted">
        Sign in to access your personal Task Manager.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="login-email" className="form-label">
            Email Address
          </label>
          <input
            id="login-email"
            type="email"
            className="form-control"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            autoComplete="email"
            required
          />
        </div>

        <div className="mb-3">
          <label htmlFor="login-password" className="form-label">
            Password
          </label>
          <input
            id="login-password"
            type="password"
            className="form-control"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            required
          />
        </div>

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        <button
          type="submit"
          className="btn btn-primary w-100"
          disabled={submitting}>
          {submitting ? "Signing In..." : "Log In"}
        </button>
      </form>

      <p className="mt-4 text-center">
        Don't have an account? <Link to="/register">Register here</Link>
      </p>
    </main>
  );
}
// What this Login page does:

// Allows users to enter their email address and password.
// Calls Supabase Authentication through my useAuth hook.
// Displays an error if authentication fails.
// Disables the submit button while the login request is processing.
// Redirects successfullly authenticated users to /tasks.
// Provides a registration link for new users.
