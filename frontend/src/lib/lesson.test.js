import { afterEach, describe, expect, it, vi } from 'vitest';

afterEach(() => { vi.unstubAllEnvs(); vi.resetModules(); });
describe('lesson gates', () => {
  it.each([[1, false, false], [2, true, false], [3, true, true], [4, true, true], [5, true, true]])(
    'enables only the supported operations on day %s', async (day, read, change) => {
      vi.stubEnv('VITE_LESSON_DAY', String(day));
      const lesson = await import('./lesson.js');
      expect(lesson.lessonDay).toBe(day);
      expect(lesson.canReadTasks).toBe(read);
      expect(lesson.canChangeTasks).toBe(change);
    },
  );
});
