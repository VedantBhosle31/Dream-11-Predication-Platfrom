import React from "react";
import "./formbar.css";

interface FormBarProps {
  hotness: number; // hotness should be a value between 0 and 100
}

const FormBar: React.FC<FormBarProps> = ({ hotness }) => {
  return (
    <div className="form-bar-container">
      {/* Gradient Bar */}
      <div className="form-bar">
        {/* Floating Triangle */}
        <div
          className="form-indicator"
          style={{ left: `${hotness}%` }} // Position the triangle based on the hotness value
        />
      </div>
    </div>
  );
};

export default FormBar;
