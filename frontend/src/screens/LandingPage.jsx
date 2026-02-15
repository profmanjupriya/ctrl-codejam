import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header.jsx';

export default function LandingPage() {
  return (
    <>
      <Header />
      <main>
        {/* Hero */}
        <section id="home" className="tech-section min-h-[80vh] flex items-center">
          <div className="tech-container text-center">
            <h1 className="tech-heading mb-4">Code Blitz</h1>
            <p className="text-gray-300 text-lg md:text-xl mb-2">
              Hosted by <span className="text-tech-purple font-semibold">CTRL</span>{' '}
              <span className="text-tech-blue font-semibold">SDSU</span>
            </p>
            <p className="text-gray-400 max-w-2xl mx-auto mb-10">
              A high-speed coding competition where teams of up to 3 compete for $450 in prizes.
            </p>
            <Link to="/registration" className="tech-button inline-block">
              Register / Login
            </Link>
            <button
              type="button"
              onClick={() => document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' })}
              className="tech-button-outline ml-4 inline-block"
            >
              Learn More
            </button>
          </div>
        </section>

        {/* About */}
        <section id="about" className="tech-section bg-tech-darker/50">
          <div className="tech-container">
            <h2 className="tech-subheading mb-8">About Code Blitz</h2>
            <p className="text-gray-300 text-lg max-w-3xl">
              Join us for a high-speed coding competition where groups of up to 3 will band together
              to fight for the chance to win $450! The fastest, most accurate competitors will win
              it all. Brought to you by the Coalition of Tech Representatives and Leadership (CTRL)
              at San Diego State University.
            </p>
          </div>
        </section>

        {/* Info - Time & Location */}
        <section id="info" className="tech-section">
          <div className="tech-container">
            <h2 className="tech-subheading mb-8">Time & Location</h2>
            <div className="tech-grid">
              <div className="tech-card">
                <div className="text-3xl mb-3">📍</div>
                <h3 className="font-semibold text-tech-blue mb-2">Venue</h3>
                <p className="text-gray-300">Templo Mayor</p>
              </div>
              <div className="tech-card">
                <div className="text-3xl mb-3">📅</div>
                <h3 className="font-semibold text-tech-blue mb-2">Date</h3>
                <p className="text-gray-300">March 21st</p>
              </div>
              <div className="tech-card">
                <div className="text-3xl mb-3">🕐</div>
                <h3 className="font-semibold text-tech-blue mb-2">Time</h3>
                <p className="text-gray-300">9am – 1pm</p>
              </div>
            </div>
          </div>
        </section>

        {/* Committee */}
        <section id="committee" className="tech-section">
          <div className="tech-container">
            <h2 className="tech-subheading mb-8">Committee</h2>
            <p className="text-gray-400 max-w-2xl mb-10">
              Code Blitz is organized by CTRL — Coalition of Tech Representatives and Leadership at
              San Diego State University. Dedicated to fostering innovation and leadership in the
              tech community.
            </p>
            <div className="tech-grid">
              <div className="tech-card text-center">
                <div className="text-3xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Committee Chair</h3>
                <p className="text-gray-300">Isabella King</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-3xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Committee Vice Chair</h3>
                <p className="text-gray-300">Ella Lamie</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-3xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Faculty Advisor</h3>
                <p className="text-gray-300">Manju Muralidharan</p>
              </div>
            </div>
          </div>
        </section>

        {/* Footer CTA */}
        <section className="tech-section border-t border-tech-blue/20">
          <div className="tech-container text-center">
            <p className="text-gray-400 mb-6">Ready to compete?</p>
            <Link to="/registration" className="tech-button inline-block">
              Go to Registration
            </Link>
          </div>
        </section>
      </main>
    </>
  );
}
