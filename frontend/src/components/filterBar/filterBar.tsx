import React from 'react';
import './filterBar.css';

interface FilterProps {
  filters: string[]; // Array of filter options
  selected: string;  // Currently selected filter
  onFilterChange: (filter: string) => void;
}

const FilterBar: React.FC<FilterProps> = ({ filters, selected, onFilterChange }) => {
  return (
    <div className="filter-container">
      <div className="filter-bar">
        {filters.map((filter) => (
          <div
            key={filter}
            className={`filter-option ${selected === filter ? 'selected' : ''}`}
            onClick={() => onFilterChange(filter)}
          >
            {filter}
          </div>
        ))}
        
        <div
          className={`slider ${filters.length === 4 ? 'long-filters' : ''}`}
          style={{
            transform: `translateX(${filters.indexOf(selected) * 100}%)`,
          }}
        />
      </div>
    </div>
  );
};

export default FilterBar;
