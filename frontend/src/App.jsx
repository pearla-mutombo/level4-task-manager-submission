import { Route, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import HomePage from "./pages/HomePage.jsx";
import TasksPage from "./pages/TasksPage.jsx";
import TaskDetailsPage from "./pages/TaskDetailsPage.jsx";
import EditTaskPage from "./pages/EditTaskPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import NotFoundPage from "./pages/NotFoundPage.jsx";
import { canReadTasks, canChangeTasks } from "./lib/lesson.js";

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<HomePage />} />

        {/* Public authentication pages */}
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />

        {/* Pages that require authentication */}
        <Route element={<ProtectedRoute />}>
          {canReadTasks && <Route path="tasks" element={<TasksPage />} />}

          {canReadTasks && (
            <Route path="tasks/:taskId" element={<TaskDetailsPage />} />
          )}

          {canChangeTasks && (
            <Route path="tasks/:taskId/edit" element={<EditTaskPage />} />
          )}
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

export default App;
// What Changed? I've place my existig task routes inside ProtectedRoute.
// Now, when someone visits /taks without being signed in, React will redirect
// them to /login.
// Once they succefffully authenticate, they'll be able to access the Task Manager.
// Flask will independently verify their access token and enforce owndership restrictions.
