import { useContext } from "react";
import { AuthContext } from "../context/authContext.js";

export function useAuth() {
  const context = useContext(AuthContext);

  if (context === null) {
    throw new Error("useAuth must be used inside an AuthProvider.");
  }

  return context;
}
// the useAuth hook will still work the same way, but the React Context and
// AuthProvider are now separated into their own files.

// this hook, it allows any component inside AuthProvider to access authentication
// information using a simple line: const { user, session, loading, signIn, signUp, signOut } = useAuth();
// user tells us which account is signed in, while signOut() lets us log out.
