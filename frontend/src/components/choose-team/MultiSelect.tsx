import React, { useState } from "react";
import Select, { MultiValue } from "react-select";

interface CustomSelectProps {
  label: string;
  data: any[];
  isMulti: boolean;
  placeholder: string;
  widthString?: string;
  onInputChange?: (inputValue: string) => void;
  onChange?: (inputValue: any) => void;
}

const CustomSelect: React.FC<CustomSelectProps> = ({
  label,
  data,
  isMulti,
  placeholder,
  widthString,
  onInputChange,
  onChange,
}) => {
  const [selectedOptions, setSelectedOptions] = useState<any[]>([]);
  const maxSelections = 22; // Maximum number of selections allowed

  const handleChange = (selected: MultiValue<any>) => {
    if (isMulti) {
      // Enforce the selection limit
      if (selected.length > maxSelections) return;
      setSelectedOptions(selected as any[]);
    } else {
      setSelectedOptions(selected ? [selected] : []);
    }
    onChange?.(selected);
  };

  const customStyles = {
    control: (styles: any) => ({
      ...styles,
      backgroundColor: "rgba(0, 0, 0, 0.25)",
      border: "2px solid rgba(255, 255, 255, 0.7)",
      color: "white",
      display: "flex",
      overflowY: isMulti ? "auto" : "visible", // Allow horizontal scrolling for multi-select
      maxHeight: isMulti && "100px",
    }),
    menu: (styles: any) => ({
      ...styles,
      backgroundColor: "rgba(0, 0, 0, 0.9)",
      color: "white",
    }),
    singleValue: (styles: any) => ({
      ...styles,
      color: "white",
    }),
    placeholder: (styles: any) => ({
      ...styles,
      color: "rgba(255, 255, 255, 0.7)",
    }),
    multiValue: (styles: any) => ({
      ...styles,
      backgroundColor: "rgba(255, 255, 255, 0.2)",
    }),
    multiValueLabel: (styles: any) => ({
      ...styles,
      color: "white",
    }),
    multiValueRemove: (styles: any) => ({
      ...styles,
      color: "white",
      ":hover": {
        backgroundColor: "rgba(255, 255, 255, 0.3)",
        color: "black",
      },
    }),
    input: (styles: any) => ({
      ...styles,
      color: "white",
    }),
  };

  return (
    <div className="custom-select-container">
      <label className="custom-select-label">
        {label} {isMulti && `(${selectedOptions.length}/${maxSelections})`}
      </label>
      <Select
        options={data}
        isMulti={isMulti}
        styles={customStyles}
        placeholder={placeholder}
        classNamePrefix="custom-select"
        className={widthString}
        onInputChange={onInputChange}
        onChange={handleChange}
      />
    </div>
  );
};

export default CustomSelect;
