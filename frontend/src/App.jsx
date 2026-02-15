import React from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext.jsx';

import LandingPage from './screens/LandingPage.jsx';
import LoginScreen from './screens/LoginScreen.jsx';
import AdminScreen from './screens/AdminScreen.jsx';
import QuestionScreen from './screens/QuestionScreen.jsx';

function RegistrationLayout({ children }) {
  return (
    <div className="min-h-screen bg-tech-dark">
      <header className="border-b border-tech-blue/20 py-3">
        <div className="max-w-7xl mx-auto px-4 flex justify-between items-center">
          <Link to="/" className="text-tech-blue font-semibold hover:opacity-90">
            ← Code Blitz
          </Link>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}

function AppRoutes() {
  const { loading } = useAuth();
  if (loading) return <div className="min-h-screen flex items-center justify-center bg-tech-dark text-white">Loading…</div>;

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/registration" element={<RegistrationLayout><LoginScreen /></RegistrationLayout>} />
      <Route path="/admin" element={<AdminScreen />} />
      <Route path="/question" element={<QuestionScreen />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
