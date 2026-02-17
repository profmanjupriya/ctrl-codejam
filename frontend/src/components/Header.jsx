import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const scrollTo = (id) => {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
};

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  const scrollLinks = [
    { id: 'home', label: 'Home' },
    { id: 'about', label: 'About' },
    { id: 'info', label: 'Info' },
    { id: 'committee', label: 'Committee' },
    { id: 'genai', label: 'Gen AI Policy' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-tech-darker/95 backdrop-blur border-b border-tech-blue/20">
      <div className="tech-container">
        <div className="flex items-center justify-between h-16">
          <button
            type="button"
            onClick={() => scrollTo('home')}
            className="flex items-center gap-2 text-white hover:opacity-90"
          >
            <span className="font-bold text-xl bg-gradient-to-r from-tech-blue to-tech-purple bg-clip-text text-transparent">
              Code Blitz
            </span>
            <span className="text-gray-400 text-sm hidden sm:inline">by CTRL SDSU</span>
          </button>

          <nav className="hidden md:flex items-center gap-1">
            {scrollLinks.map(({ id, label }) => (
              <button
                key={id}
                type="button"
                onClick={() => scrollTo(id)}
                className="tech-nav-link"
              >
                {label}
              </button>
            ))}
            <Link to="/registration" className="tech-button ml-2">
              Login
            </Link>
          </nav>

          {/* Mobile menu button */}
          <div className="flex items-center gap-2 md:hidden">
            <Link to="/registration" className="tech-button py-2">
              Login
            </Link>
            <button
              type="button"
              onClick={() => setMenuOpen(!menuOpen)}
              className="tech-nav-link p-2"
              aria-label="Toggle menu"
            >
              {menuOpen ? '✕' : '☰'}
            </button>
          </div>
        </div>

        {/* Mobile dropdown */}
        {menuOpen && (
          <div className="md:hidden py-3 border-t border-tech-blue/20">
            {scrollLinks.map(({ id, label }) => (
              <button
                key={id}
                type="button"
                onClick={() => {
                  scrollTo(id);
                  setMenuOpen(false);
                }}
                className="tech-nav-link block w-full text-left py-2"
              >
                {label}
              </button>
            ))}
          </div>
        )}
      </div>
    </header>
  );
}
