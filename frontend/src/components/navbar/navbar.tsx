import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

const Navbar: React.FC = () => {
  return (
    <div className="navbar">
      <ul className="navlist">
        <li className="nav-item">
          <img className="dream-logo" src="/logo.png"></img>
        </li>
        <li className="nav-item">
          <Link to="/" className="nav-link">Home</Link>
        </li>
        <li className="navItem">
          <Link to="/team" className="nav-link">Team</Link>
        </li>
        <li className="navItem">
          <Link to="/" className="nav-link">FAQs</Link>
        </li>
        <li className="navItem">
          <Link to="/" className="nav-link">Help</Link>
        </li>
        
      </ul>
    </div>
  );
};

export default Navbar;