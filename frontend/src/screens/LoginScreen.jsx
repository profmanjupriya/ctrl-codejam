import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';

export default function LoginScreen() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const doLogin = async (e) => {
    e?.preventDefault();
    if (!username.trim() || !password) {
      setMessage('Enter username and password');
      return;
    }
    setLoading(true);
    setMessage('');
    try {
      const res = await login(username.trim(), password);
      if (res.ok) {
        if (res.is_admin) navigate('/admin', { replace: true });
        else navigate('/question', { replace: true });
      } else {
        setMessage(res.error || 'Invalid login');
      }
    } catch (e) {
      setMessage(e.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-box">
        <h1 className="login-title">Welcome</h1>
        <form onSubmit={doLogin}>
          <label className="login-label">Username</label>
          <input
            type="text"
            className="login-input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />
          <label className="login-label">Password</label>
          <input
            type="password"
            className="login-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />
          <div className="login-btn-row">
            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? '…' : 'Login'}
            </button>
          </div>
        </form>
        {message ? <p className="login-msg">{message}</p> : null}
      </div>
    </div>
  );
}
