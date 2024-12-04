import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

const Navbar: React.FC = () => {
  return (
    <div className="navbar">
      <ul className="navlist">
        <li className="nav-item">
          <Link to="/" className="nav-link">Home</Link>
        </li>
        <li className="navItem">
          <Link to="/about" className="nav-link">About</Link>
        </li>
        <li className="navItem">
          <Link to="/services" className="nav-link">Services</Link>
        </li>
        <li className="navItem">
          <Link to="/projects" className="nav-link">Projects</Link>
        </li>
        <li className="navItem">
          <Link to="/contact" className="nav-link">Contact</Link>
        </li>
      </ul>
    </div>
  );
};

export default Navbar;