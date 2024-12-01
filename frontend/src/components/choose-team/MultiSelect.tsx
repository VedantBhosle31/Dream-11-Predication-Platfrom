import React from "react";
import Select from "react-select";

interface CustomSelectProps {
  label: string;
  data: any[];
  isMulti: boolean;
  placeholder: string;
}

const CustomSelect: React.FC<CustomSelectProps> = ({
  label,
  data,
  isMulti,
  placeholder,
}) => {
  const customStyles = {
    control: (styles) => ({
      ...styles,
      backgroundColor: "rgba(0, 0, 0, 0.8)",
      borderColor: "transparent",
      color: "white",
    }),
    menu: (styles) => ({
      ...styles,
      backgroundColor: "rgba(0, 0, 0, 0.9)",
      color: "white",
    }),
    singleValue: (styles) => ({
      ...styles,
      color: "white",
    }),
    placeholder: (styles) => ({
      ...styles,
      color: "rgba(255, 255, 255, 0.7)",
    }),
    multiValue: (styles) => ({
      ...styles,
      backgroundColor: "rgba(255, 255, 255, 0.2)",
    }),
    multiValueLabel: (styles) => ({
      ...styles,
      color: "white",
    }),
    multiValueRemove: (styles) => ({
      ...styles,
      color: "white",
      ":hover": {
        backgroundColor: "rgba(255, 255, 255, 0.3)",
        color: "black",
      },
    }),
  };

  return (
    <div className="custom-select-container">
      <label className="custom-select-label">{label}</label>
      <Select
        options={data}
        isMulti={isMulti}
        styles={customStyles}
        placeholder={placeholder}
        classNamePrefix="custom-select"
      />
    </div>
  );
};

export default CustomSelect;
