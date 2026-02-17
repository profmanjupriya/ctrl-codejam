import React, { useEffect, useState } from "react";
import { Link } from 'react-router-dom';

export default function HomeScreen() {

  
  return (
    <div className="home">
      <header className="home-header">
        <h1 className="home-title">Code Blitz</h1>
        <div className="home-subtitle-row">
          <span className="home-subtitle">Hosted by </span>
          <span className="home-subtitle" style={{ color: '#B46CFF' }}>CTRL </span>
          <span className="home-subtitle" style={{ color: '#FF3B3B' }}>SDSU</span>
        </div>
      </header>

      <div className="home-cards">
        <div className="home-card">
          <h2 className="home-card-title">About the Code Blitz</h2>
          <p className="home-card-body">
            Join us for a high speed coding competition where groups of up to 3 will band
            together to fight for the chance to win $450! The fastest, most accurate
            competitors will win it all.
          </p>
          <Link to="/info" className="home-card-btn">Learn More</Link>
        </div>

        <div className="home-card">
          <h2 className="home-card-title">Time and Location</h2>
          <p className="home-card-body">Templo Mayor, March 21st{'\n'}9am to 1pm</p>
          <Link to="/info" className="home-card-btn">Event Info</Link>
        </div>

        <div className="home-card">
          <h2 className="home-card-title">Registration is Open</h2>
          <p className="home-card-body">Registration!</p>
          <Link to="/registration" className="home-card-btn">Discord</Link>
        </div>
      </div>
    </div>
  );
}
