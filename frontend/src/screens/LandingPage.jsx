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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Isabella King</h3>
                <p className="text-gray-300">Committee Chair</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Ella Lamie</h3>
                <p className="text-gray-300">Committee Vice Chair</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Justin Pelak</h3>
                <p className="text-gray-300">CTRL President</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Everett Richards</h3>
                <p className="text-gray-300">CTRL Vice President</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Manju Muralidharan Priya</h3>
                <p className="text-gray-300">Faculty Advisor</p>
                <img src="/Manju.png" alt="Manju Muralidharan Priya" className="mt-3 w-full h-45 object-cover rounded" />
              </div>
            </div>
            <br></br>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Aadi Bery</h3>
                <p className="text-gray-300">Event Logistics, Industry Outreach</p>
                <img src="/ABeryHeadshot.jpg" alt="Aadi Bery" className="mt-3 w-50 h-50 object-cover rounded" />
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Brandon Garate</h3>
                <p className="text-gray-300">Industry Outreach, Marketing</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Bricen Humphrey-Schaefer</h3>
                <p className="text-gray-300">Competition Layout, Website</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Dhruv Ramgiri</h3>
                <p className="text-gray-300">Finances</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Jose Hernandez Sanchez</h3>
                <p className="text-gray-300">Helper</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
            </div>
            <br></br>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Kurt Lara-Rosales</h3>
                <p className="text-gray-300">Competition Layout, Website</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Mathew Hernandez</h3>
                <p className="text-gray-300">Emailer, Secretary</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Matthew Long</h3>
                <p className="text-gray-300">Competition Layout, Finances</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Nitin Chatlani</h3>
                <p className="text-gray-300">Competition Layout, Industry Outreach</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Patricia Alfonso</h3>
                <p className="text-gray-300">Marketing, Merch</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
            </div>
            <br></br>
            <div className="grid grid-center grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              <div></div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Robert Fuller</h3>
                <p className="text-gray-300">Competition Layout, Website Testing</p>
                <div className="text-4xl mt-3">👤</div>
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Shamikh Quazi</h3>
                <p className="text-gray-300">Finances</p>
                <img src="/SQuazi.jpg" alt="Shamikh Quazi" className="mt-3 w-full h-40 object-cover rounded" />
              </div>
              <div className="tech-card text-center">
                <h3 className="font-semibold text-tech-blue mb-1">Shelvy Millado</h3>
                <p className="text-gray-300">Instagram, Reels, LinkedIn</p>
                <div className="text-4xl mt-3">👤</div>
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
