import React, { useState } from 'react';
import { Menu, MenuItem, IconButton } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import './filterButton.css';

type FilterOptions = 'All' | 'ODI' | 'Test' | 'T20';
type TypeOptions = 'All' | 'Domestic' | 'International';

const FilterButton: React.FC = () => {
  // State for filter values
  const [selectedFilter, setSelectedFilter] = useState<FilterOptions>('All');
  const [selectedType, setSelectedType] = useState<TypeOptions>('All');
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleFilterChange = (filter: FilterOptions) => {
    setSelectedFilter(filter);
    setAnchorEl(null);
  };

  const handleTypeChange = (type: TypeOptions) => {
    setSelectedType(type);
    setAnchorEl(null);
  };

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div className="filterbutton">
      <IconButton onClick={handleClick} className="hamburger-icon">
        <MenuIcon />
      </IconButton>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
        
      >
        <div className="dropdown-menu" style={{display:"flex", flexDirection:"row", backgroundColor:"black", color:"white"}}>
          <div className="filter-section" style={{justifyItems:"center", justifyContent:"center"}}>
            <h4>Filter Type</h4>
            {['All', 'ODI', 'Test', 'T20'].map((filter) => (
              <MenuItem
                key={filter}
                onClick={() => handleFilterChange(filter as FilterOptions)}
                sx={{
                  backgroundColor: selectedFilter === filter ? '#FA2433' : 'transparent',
                  color: selectedFilter === filter ? 'white' : 'inherit',
                  '&:hover': {
                    backgroundColor: '#3e8e41', // Optional: Change hover color
                  },
                }}
              >
                {filter}
              </MenuItem>
            ))}
          </div>

          <div className="type-section" style={{justifyItems:"center", justifyContent:"center"}}>
            <h4>Type</h4>
            {['All', 'Domestic', 'International'].map((type) => (
              <MenuItem
                key={type}
                onClick={() => handleTypeChange(type as TypeOptions)}
                sx={{
                  backgroundColor: selectedType === type ? '#FA2433' : 'transparent',
                  color: selectedType === type ? 'white' : 'inherit',
                  '&:hover': {
                    backgroundColor: '#3e8e41', // Optional: Change hover color
                  },
                }}
              >
                {type}
              </MenuItem>
            ))}
          </div>
        </div>
      </Menu>
    </div>
  );
};

export default FilterButton;