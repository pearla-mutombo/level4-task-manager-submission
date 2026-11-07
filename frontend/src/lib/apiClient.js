import axios from "axios";
import { supabase } from "./supabaseClient.js";

export const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5001/api";

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000,
  headers: { Accept: "application/json" },
});

// Attach the current Supabase access token to each request.
apiClient.interceptors.request.use(async (config) => {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession();

  if (error) {
    throw error;
  }

  if (session?.access_token) {
    config.headers.set("Authorization", `Bearer ${session.access_token}`);
  } else {
    config.headers.delete("Authorization");
  }

  return config;
});

export function requestError(error) {
  if (error.response?.data?.error) return error.response.data.error;
  if (error.code === "ECONNABORTED") {
    return "The API took too long to respond. Try again.";
  }
  return "Could not reach the Flask API. Check that the backend is running and its allowed origin matches this page.";
}

export function isCanceled(error) {
  return axios.isCancel(error) || error.code === "ERR_CANCELED";
}
// Previously, Axio sent requests without an authentication token.
// Now, before sending each request, Axio checks for the current Supabase session
// when the user is logged in, requests include: Authorization: Bearer <access_token>
// Flask will verifu that token and use the authenticated user's identity to
// determined which tasks and categories they can access.
// if no session exists, Axio sends no authorization header, and my protected Flask
// endpoints should return 401 Unauthorized.
// * the token is obtained from the Supabase session, not from a user ID
// * entered by the client. We also won't print or store the access token in application logs.
