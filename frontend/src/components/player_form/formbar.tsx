import React from "react";
import "./formbar.css";

interface FormBarProps {
  hotness: number;
}

const FormBar: React.FC<FormBarProps> = ({ hotness }) => {
  return (
    <div className="form-bar-container">
      <div className="form-bar">
        <div
          className="form-indicator"
          style={{ left: `${hotness}%` }}
        />
      </div>
    </div>
  );
};

export default FormBar;
