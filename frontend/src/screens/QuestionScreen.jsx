import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { api, formatTime } from '../services/api.js';

const RUN_COOLDOWN_MS = 3000;

function getStarterForLanguage(q, lang) {
  if (lang === 'java' && q.starter_java) return q.starter_java;
  if (lang === 'cpp' && q.starter_cpp) return q.starter_cpp;
  return q.starter || '';
}

export default function QuestionScreen() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [questions, setQuestions] = useState([]);
  const [qIndex, setQIndex] = useState(0);
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [score, setScore] = useState(0);
  const [remaining, setRemaining] = useState(null);
  const [timerSuspended, setTimerSuspended] = useState(false);
  const [runDisabled, setRunDisabled] = useState(true);
  const [runCooldown, setRunCooldown] = useState(false);
  const [finalScore, setFinalScore] = useState(null);
  const [completed, setCompleted] = useState(false);
  const runCooldownRef = useRef(null);

  const loadQuestions = async () => {
    try {
      const res = await api.questions.list();
      if (res.ok && res.questions?.length) {
        setQuestions(res.questions);
        const q0 = res.questions[0];
        const starter = getStarterForLanguage(q0, language);
        setCode(starter || '');
        setQIndex(0);
      }
    } catch {
      setQuestions([]);
    }
  };

  //hi how are you

  const pollTimer = async () => {
    try {
      const res = await api.timer.status();
      if (res.ok) {
        setRemaining(res.remaining);
        setTimerSuspended(res.suspended === true);
        if (res.started && !completed) setRunDisabled(false);
      }
    } catch {
      setRemaining(null);
      setTimerSuspended(false);
    }
  };

  useEffect(() => {
    if (!user) {
      navigate('/registration', { replace: true });
      return;
    }
    loadQuestions();
  }, [user, navigate]);

  useEffect(() => {
    const id = setInterval(pollTimer, 1000);
    return () => clearInterval(id);
  }, [runDisabled]);

  useEffect(() => {
    if (questions.length && qIndex < questions.length) {
      setCode(getStarterForLanguage(questions[qIndex], language));
    }
  }, [qIndex, questions, language]);

  const runCode = async () => {
    if (runCooldown || runDisabled || completed) return;
    setRunCooldown(true);
    setOutput('Running...\n');
    const maxRetries = 2;
    let lastError;
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const res = await api.questions.run(code, qIndex, language);
        setOutput(res.output || '');
        if (res.correct && res.points) {
          const newScore = score + res.points;
          setScore(newScore);
          setOutput((o) => o + `\n✅ Correct! +${res.points} points\n`);
          if (runCooldownRef.current) clearTimeout(runCooldownRef.current);
          runCooldownRef.current = setTimeout(() => {
            setQIndex((i) => {
              const next = i + 1;
              if (next >= questions.length) {
                setFinalScore(newScore);
                setOutput((o) => o + `\n🎉 Quiz Complete!\nFinal Score: ${newScore}\n`);
                setRunDisabled(true);
                setCompleted(true);
                return questions.length; // move index past last question
              }
              return next;
            });
            setRunCooldown(false);
          }, 1500);
          return;
        }
        break;
      } catch (e) {
        lastError = e;
        if (e.status === 429 && attempt < maxRetries) {
          setOutput(`Server busy, retrying in 2s... (${attempt + 1}/${maxRetries})\n`);
          await new Promise((r) => setTimeout(r, 2000));
        } else {
          break;
        }
      }
    }
    setOutput(lastError?.error || 'Request failed');
    runCooldownRef.current = setTimeout(() => setRunCooldown(false), RUN_COOLDOWN_MS);
  };

  const currentQ = questions[qIndex];
  const isComplete = completed || (qIndex >= questions.length && questions.length > 0);

  const handleLogout = () => {
    logout();
    navigate('/', { replace: true });
  };

  return (
    <div className="question-page">
      <div className="question-top-bar">
        <span className="question-top-text">Score: {score}</span>
        <span className="question-top-text">
          {timerSuspended ? '⏱ Timer suspended' : remaining != null ? `⏱ ${formatTime(remaining)}` : '⏱ Waiting for admin…'}
        </span>
      </div>

      {currentQ && !isComplete && (
        <p className="question-prompt">{currentQ.prompt}</p>
      )}
      {isComplete && (
        <p className="question-prompt">🎉 Quiz Complete!</p>
      )}

      <div className="question-lang-select">
        <label htmlFor="lang">Language: </label>
        <select
          id="lang"
          value={language}
          onChange={(e) => {
            const lang = e.target.value;
            setLanguage(lang);
            if (currentQ) setCode(getStarterForLanguage(currentQ, lang));
          }}
          disabled={runDisabled}
        >
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>
      </div>

      <button
        type="button"
        className={`question-run-btn ${(runCooldown || runDisabled) ? 'run-disabled' : ''}`}
        onClick={runCode}
        disabled={runCooldown || runDisabled}
      >
        ▶ Run
      </button>

      <div className="question-main">
        <textarea
          className="question-editor"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          disabled={runDisabled}
          placeholder="Code"
          spellCheck={false}
        />
        <div className="question-output-wrap">
          <pre className="question-output">{output || ' '}</pre>
        </div>
      </div>

      <button type="button" className="question-logout" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}
