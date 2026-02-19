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
                href="https://www.instagram.com/ctrl_sdsu/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 text-tech-blue hover:text-tech-purple transition-colors duration-200"
              >
                <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.057-1.645.069-4.849.069-3.203 0-3.584-.012-4.849-.069-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zM5.838 12a6.162 6.162 0 1 1 12.324 0 6.162 6.162 0 0 1-12.324 0zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm4.965-10.322a1.44 1.44 0 1 1 2.881.001 1.44 1.44 0 0 1-2.881-.001z"/>
                </svg>
                <span className="text-sm font-semibold">Instagram</span>
              </a>
              <a
                href="https://www.linkedin.com/company/ctrl-sdsu-coalition-of-tech-representatives-and-leadership/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 text-tech-blue hover:text-tech-purple transition-colors duration-200"
              >
                <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.225 0z"/>
                </svg>
                <span className="text-sm font-semibold">LinkedIn</span>
              </a>
              <a
                href="https://discord.gg/5Jdt4WuP4K"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 text-tech-blue hover:text-tech-purple transition-colors duration-200"
              >
                <svg width="48" height="48" viewBox="0 0 127.14 96.36" fill="currentColor">
                  <path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0A105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a77.15,77.15,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.18,77,77,0,0,0,6.89,11.1A105.73,105.73,0,0,0,126.6,80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60.55,31,53.88s5-11.81,11.45-11.81S53.9,46.13,53.9,52.79,48.7,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60.55,73.25,53.88s5-11.81,11.45-11.81S95.89,46.13,95.89,52.79,90.7,65.69,84.69,65.69Z"/>
                </svg>
                <span className="text-sm font-semibold">Discord</span>
              </a>
            </div>
          </div>
        </section>
        </main>
      </div>
    </>
  );
}
