import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles/main.scss";
import App from "./App.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";

// Get the root element from the HTML.
const rootElement = document.getElementById("root");

// Render the application with authentication available.
createRoot(rootElement).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
);
// the authentication provider wraps my entire application, making the
// current session available to my pages components.
// previously i had the BrowserRouter wrap around my entire application.
