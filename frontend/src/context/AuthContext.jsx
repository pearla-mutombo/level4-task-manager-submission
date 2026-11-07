import { useEffect, useState } from "react";
import { supabase } from "../lib/supabaseClient.js";
import { AuthContext } from "./authContext.js";

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    // Restore the user's session when the app loads.
    supabase.auth
      .getSession()
      .then(({ data, error }) => {
        if (!active) return;

        if (error) {
          console.error("Could not restore the session:", error.message);
        }

        setSession(error ? null : data.session);
        setLoading(false);
      })
      .catch((error) => {
        if (!active) return;
        console.error("Session restoration failed:", error.message);
        setSession(null);
        setLoading(false);
      });

    // Listen for login, logout, and token refresh events.
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      if (active) {
        setSession(nextSession);
        setLoading(false);
      }
    });

    return () => {
      active = false;
      subscription.unsubscribe();
    };
  }, []);

  const value = {
    session,
    user: session?.user ?? null,
    loading,
    signIn: (email, password) =>
      supabase.auth.signInWithPassword({ email, password }),
    signUp: (email, password) => supabase.auth.signUp({ email, password }),
    signOut: () => supabase.auth.signOut(),
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
// This context manages frontend session state. Our Flask backend will still
// independently verify each access token before allowing access to protected
// task data.

// What this codes does:
// getSession() restores a saved login session when the application starts.
// onAuthStateChange() listens for login, logout, and token refresh events.
// user identifies the currently signed-in account.
// loading tells React when the initial session check is still running.
// signIn, signUp, and signOut provide authentication functions for our
// upcoming pages.
