import React from "react";
import "./formbar.css";

interface FormBarProps {
  hotness: number;
}

const FormBar: React.FC<FormBarProps> = ({ hotness }) => {
  return (
    <div className="form-bar-container">
      {/* Gradient Bar */}
      <div className="form-bar">
        {/* Floating Triangle */}
        <div
          className="form-indicator"
          style={{ left: `${hotness}%` }}
        />
      </div>
    </div>
  );
};

export default FormBar;
