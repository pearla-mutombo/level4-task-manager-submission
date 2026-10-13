import { Route, Routes } from 'react-router-dom';
import AppLayout from './layouts/AppLayout.jsx';
import HomePage from './pages/HomePage.jsx';
import TasksPage from './pages/TasksPage.jsx';
import TaskDetailsPage from './pages/TaskDetailsPage.jsx';
import EditTaskPage from './pages/EditTaskPage.jsx';
import NotFoundPage from './pages/NotFoundPage.jsx';
import { canReadTasks, canChangeTasks } from './lib/lesson.js';

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<HomePage />} />
        {canReadTasks && <Route path="tasks" element={<TasksPage />} />}
        {canReadTasks && <Route path="tasks/:taskId" element={<TaskDetailsPage />} />}
        {canChangeTasks && <Route path="tasks/:taskId/edit" element={<EditTaskPage />} />}
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

export default App;
