export const lessonDay = Number(import.meta.env.VITE_LESSON_DAY || 5);
export const canReadTasks = lessonDay >= 2;
export const canChangeTasks = lessonDay >= 3;
