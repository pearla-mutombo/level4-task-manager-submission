import { useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

export default function RegisterPage() {
  const { user, loading, signUp } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (password.length < 6) {
      setError("Password must contain at least 6 characters.");
      return;
    }

    setSubmitting(true);

    try {
      const { data, error: signUpError } = await signUp(email.trim(), password);

      if (signUpError) {
        setError(signUpError.message);
        return;
      }

      if (data.session) {
        setSuccess("Account created successfully! You are now signed in.");
      } else {
        setSuccess(
          "Registration submitted. Please check your email for a confirmation link before signing in.",
        );
      }

      setPassword("");
      setConfirmPassword("");
    } catch {
      setError("Unable to register right now. Please try again.");
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
      <h1 className="mb-3">Create an Account</h1>
      <p className="text-muted">
        Register to manage your own private tasks and categories.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="register-email" className="form-label">
            Email Address
          </label>
          <input
            id="register-email"
            type="email"
            className="form-control"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            autoComplete="email"
            required
          />
        </div>

        <div className="mb-3">
          <label htmlFor="register-password" className="form-label">
            Password
          </label>
          <input
            id="register-password"
            type="password"
            className="form-control"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="new-password"
            minLength={6}
            required
          />
        </div>

        <div className="mb-3">
          <label htmlFor="register-confirm-password" className="form-label">
            Confirm Password
          </label>
          <input
            id="register-confirm-password"
            type="password"
            className="form-control"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
            autoComplete="new-password"
            minLength={6}
            required
          />
        </div>

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success" role="status">
            {success}
          </div>
        )}

        <button
          type="submit"
          className="btn btn-primary w-100"
          disabled={submitting}>
          {submitting ? "Creating Account..." : "Register"}
        </button>
      </form>

      <p className="mt-4 text-center">
        Already have an account? <Link to="/login">Log in here</Link>
      </p>
    </main>
  );
}
// What this registration pages does:

// Allows new users to register with an email address and password.
// Checks that both password match.
// Requires a password containing at least six characters, although Supabase may
// enfore additional password requirements.
// Displayas registration errors and confirmation messages.
// Handles Supabase's optional email verification process.
// Provides a link to the login page.

// * Supabase controls whether email confirmation is required. if confirmation is
// * enabaled, the user must verify their email before logging in. I'll test that
// * behavior when i create my two test accounts.
