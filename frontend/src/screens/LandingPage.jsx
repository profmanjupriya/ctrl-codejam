import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header.jsx';

export default function LandingPage() {
  const images = [
    "WhiteL.png",
    "PinkL.png",
  ];

  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrent((prev) => (prev === 0 ? 1 : 0));
    }, 3000); // change every 6 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <>
      {/* Animated Background */}
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: 0,
          overflow: 'hidden',
        }}
      >
        {images.map((img, index) => (
          <div
            key={index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              backgroundImage: `url(${img})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundAttachment: 'fixed',
              opacity: index === current ? 1 : 0,
              transition: 'opacity 2s ease-in-out',
              zIndex: index === current ? 1 : 0,
            }}
          />
        ))}
        {/* Dark overlay for readability */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.4)',
            zIndex: 1,
          }}
        />
      </div>

      {/* Content wrapper */}
      <div style={{ position: 'relative', zIndex: 10 }}>
        <Header />
        <main>
        {/* Hero */}
        <section id="home" className="tech-section min-h-[80vh] flex items-center">
          <div className="tech-container text-center">
            <h1 className="tech-heading mb-4">Code Blitz</h1>
            <p className="text-white-300 text-lg md:text-xl mb-2">
              Hosted by <span className="text-tech-purple font-semibold">CTRL</span>{' '}
              <span className="text-tech-blue font-semibold">SDSU</span>
            </p>
            <p className="text-white-400 max-w-2xl mx-auto mb-10">
              A high-speed coding competition where teams of up to 3 compete for $450 in prizes.
            </p>
            <a
              href="https://docs.google.com/forms/d/1IBp4rhWKWIqCa-5zKK81LZjxX3E7skSA4rOa-oBn9Eo/edit"
              target="_blank"
              rel="noopener noreferrer"
              className="tech-button inline-block"
            >
              Sign up
            </a>
            <a
              href="https://discord.gg/5Jdt4WuP4K"
              target="_blank"
              rel="noopener noreferrer"
              className="tech-button-outline ml-4 inline-block"
            >
              Discord
            </a>
          </div>
        </section>

        {/* About */}
        <section id="about" className="tech-section bg-tech-darker/50">
          <div className="tech-container text-center">
            <h2 className="tech-subheading mb-8">About Code Blitz</h2>
            <p className="text-white-300 text-lg max-w-3xl ml-auto mr-auto">
              Join us for a high-speed coding competition where groups of up to 3 will band together
              to fight for the chance to win $450! The fastest, most accurate competitors will win
              it all. Brought to you by the Coalition of Tech Representatives and Leadership (CTRL)
              at San Diego State University.
              <br /> Sign-ups are capped at 70 participants. There is a $5
              entry fee that must be paid prior to the event.
            </p>
          </div>
        </section>

        {/* Info - Time & Location */}
        <section id="info" className="tech-section bg-tech-darker/50">
          <div className="tech-container">
            <h2 className="tech-subheading mb-8 text-center">Time & Location</h2>
            <div className="tech-grid">
              <div className="tech-card">
                <div className="text-3xl mb-3 text-center">📍</div>
                <h3 className="font-semibold text-tech-blue mb-2 text-center">Venue</h3>
                <p className="text-gray-300 text-center">Templo Mayor</p>
              </div>
              <div className="tech-card">
                <div className="text-3xl mb-3 text-center">📅</div>
                <h3 className="font-semibold text-tech-blue mb-2 text-center">Date</h3>
                <p className="text-gray-300 text-center">March 21st</p>
              </div>
              <div className="tech-card">
                <div className="text-3xl mb-3 text-center">🕐</div>
                <h3 className="font-semibold text-tech-blue mb-2 text-center">Time</h3>
                <p className="text-gray-300 text-center">9am – 1pm</p>
              </div>
            </div>
          </div>
        </section>

        {/* Committee */}
        <section id="committee" className="tech-section bg-tech-darker/50">
          <div className="tech-container">
            <h2 className="tech-subheading mb-8 text-center">Committee</h2>
            <p className="text-white-400 max-w-2xl mb-10 text-center mx-auto">
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

        {/* Generative AI Policy */}
        <section id="genai" className="tech-section bg-tech-darker/50">
          <div className="tech-container">
            <h2 className="tech-subheading mb-8 text-center">Generative AI Policy</h2>

            <div className="mb-6">
              <div className="rounded-lg p-4 text-white bg-gradient-to-r from-tech-blue/10 to-tech-purple/10 border-2 border-tech-blue/30">
                  <p className="font-semibold text-center">Use GenAI to accelerate your work, not replace it.</p>
                </div>
            </div>

            <div className="tech-grid">
              <div className="tech-card">
                <h3 className="font-semibold text-tech-blue mb-3">What&apos;s Allowed:</h3>
                <ul className="text-gray-300 list-disc pl-5 space-y-1">
                  <li>Coding help (debugging, boilerplate, explanations)</li>
                  <li>Design mockups (logos, UI, visuals)</li>
                  <li>Brainstorming (ideas, starter text)</li>
                  <li>Documentation support (README, slides, pitch)</li>
                </ul>
              </div>

              <div className="tech-card">
                <h3 className="font-semibold text-tech-blue mb-3">What&apos;s NOT Allowed:</h3>
                <ul className="text-gray-300 list-disc pl-5 space-y-1">
                  <li>Submitting end-to-end AI-generated projects</li>
                  <li>Hiding AI usage or claiming AI&apos;s work as your own</li>
                  <li>Feeding real student/private data into AI tools</li>
                  <li>Training large AI models from scratch</li>
                </ul>
              </div>

              <div className="tech-card">
                <h3 className="font-semibold text-tech-blue mb-3">Expectations:</h3>
                <ul className="text-gray-300 list-disc pl-5 space-y-1">
                  <li>Judges will look at your process as much as your demo</li>
                  <li>Be ready to explain what you built vs. what AI generated</li>
                  <li>Bonus points for showing ethical and effective AI use</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Footer CTA */}
        <section className="tech-section border-t border-tech-blue/20">
          <div className="tech-container text-center">
            <p className="text-gray-400 mb-6">Ready to compete?</p>
            <a
              href="https://docs.google.com/forms/d/1IBp4rhWKWIqCa-5zKK81LZjxX3E7skSA4rOa-oBn9Eo/edit"
              target="_blank"
              rel="noopener noreferrer"
              className="tech-button inline-block"
            >
              Sign up
            </a>
          </div>
        </section>
        </main>
      </div>
    </>
  );
}
