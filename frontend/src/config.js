// Base URL for backend API.
// - In local dev, leave VITE_API_BASE_URL unset so Vite proxy uses /api -> localhost:5000.
// - In production (e.g. Vercel), set VITE_API_BASE_URL to your judge backend URL
//   (e.g. http://64.23.188.213:5000 or https://api.yourdomain.com).
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
