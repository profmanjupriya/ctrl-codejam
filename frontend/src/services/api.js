import { API_BASE_URL } from '../config.js';

const AUTH_TOKEN_KEY = 'codeblitz_token';

export function getAuthToken() {
  return sessionStorage.getItem(AUTH_TOKEN_KEY);
}

export function setAuthToken(token) {
  if (token) sessionStorage.setItem(AUTH_TOKEN_KEY, token);
  else sessionStorage.removeItem(AUTH_TOKEN_KEY);
}

export function clearAuthToken() {
  sessionStorage.removeItem(AUTH_TOKEN_KEY);
}

const base = (path, options = {}) => {
  const url = `${API_BASE_URL}${path}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  const token = getAuthToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const opts = {
    ...options,
    headers,
    credentials: 'include',
  };
  return fetch(url, opts).then(async (res) => {
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw { status: res.status, ...data };
    return data;
  });
};

export const api = {
  auth: {
    login: (username, password) =>
      base('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      }),
    logout: () => base('/api/auth/logout', { method: 'POST' }),
    me: () => base('/api/auth/me'),
  },
  timer: {
    status: () => base('/api/timer/status'),
  },
  admin: {
    startExam: () => base('/api/admin/start-exam', { method: 'POST' }),
    pauseExam: () => base('/api/admin/pause-exam', { method: 'POST' }),
    resetExam: () => base('/api/admin/reset-exam', { method: 'POST' }),
    users: () => base('/api/admin/users'),
    createUser: (username, password) =>
      base('/api/admin/users', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      }),
    deleteUser: (userId) =>
      base(`/api/admin/users/${userId}`, { method: 'DELETE' }),
    updateUserPassword: (userId, password) =>
      base(`/api/admin/users/${userId}`, {
        method: 'PUT',
        body: JSON.stringify({ password }),
      }),
    clearUsers: () => base('/api/admin/users/clear', { method: 'POST' }),
    timerStatus: () => base('/api/admin/timer-status'),
    leaderboard: () => base('/api/admin/leaderboard'),
  },
  questions: {
    list: () => base('/api/questions/'),
    run: (code, questionIndex, language = 'python', options = {}) =>
      base('/api/questions/run', {
        method: 'POST',
        body: JSON.stringify({
          code,
          question_index: questionIndex,
          language,
          preview: options.preview === true,
        }),
      }),
  },
};

export function formatTime(seconds) {
  if (seconds == null) return '--:--';
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}
