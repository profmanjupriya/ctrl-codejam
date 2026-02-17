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
            <p className="text-white-400 max-w-2xl mx-auto mb-3">
              A high-speed coding competition where teams of up to 3 compete for $450 in prizes.
            </p>
            <p className="text-white-400 max-w-2xl mx-auto mb-10">
              Sign Up from February 23rd - March 16th to compete!!
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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Committee Chair</h3>
                <p className="text-gray-300">Isabella King</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Committee Vice Chair</h3>
                <p className="text-gray-300">Ella Lamie</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">CTRL President</h3>
                <p className="text-gray-300">Justin Pelak</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">CTRL Vice President</h3>
                <p className="text-gray-300">Everett Richards</p>
              </div>
            </div>
            <br>
            </br>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Committee Chair</h3>
                <p className="text-gray-300">Mathew Hernandez</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Committee Vice Chair</h3>
                <p className="text-gray-300">Shamikh Quazi</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Faculty Advisor</h3>
                <p className="text-gray-300">Aadi Bery</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Faculty Advisor</h3>
                <p className="text-gray-300">Matthew Long</p>
              </div>
            </div>
            <br>
            </br>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Website/Competition Layout</h3>
                <p className="text-gray-300">Bricen Humphrey-Schaefer</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Website/Competition Layout</h3>
                <p className="text-gray-300">Kurt Lara-Rosales</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Website/Competition Layout</h3>
                <p className="text-gray-300">Robert Fuller</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Faculty Advisor</h3>
                <p className="text-gray-300">Patricia Alfonso</p>
              </div>
            </div>
            <br>
            </br>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Committee Chair</h3>
                <p className="text-gray-300">Shelvy Millado</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Committee Vice Chair</h3>
                <p className="text-gray-300">Dhruv Ramgiri</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Faculty Advisor</h3>
                <p className="text-gray-300">Nitin Chatlani</p>
              </div>
              <div className="tech-card text-center">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="font-semibold text-tech-blue mb-1">Faculty Advisor</h3>
                <p className="text-gray-300"></p>
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
                  <p className="font-semibold text-center">No usage of AI is allowed in any form.</p>
                </div>
            </div>
          </div>
        </section>

        {/* Contact Us */}
        <section id="contact" className="tech-section bg-tech-darker/50 border-t border-tech-blue/20">
          <div className="tech-container text-center">
            <h2 className="tech-subheading mb-8">Contact Us</h2>
            <div className="flex justify-center gap-8">
              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 text-tech-blue hover:text-tech-purple transition-colors duration-200"
              >
                <div className="text-4xl">📷</div>
                <span className="text-sm font-semibold">Instagram</span>
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 text-tech-blue hover:text-tech-purple transition-colors duration-200"
              >
                <div className="text-4xl">💼</div>
                <span className="text-sm font-semibold">LinkedIn</span>
              </a>
              <a
                href="mailto:contact@codeblitz.com"
                className="flex flex-col items-center gap-2 text-tech-blue hover:text-tech-purple transition-colors duration-200"
              >
                <div className="text-4xl">✉️</div>
                <span className="text-sm font-semibold">Email</span>
              </a>
            </div>
          </div>
        </section>
        </main>
      </div>
    </>
  );
}
