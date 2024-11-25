import React, { useState } from "react";
import TextField from "@mui/material/TextField";
import { IconButton, InputAdornment, List, ListItem, ListItemButton, ListItemText } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import geminiicon from "../../assets/icons/gemini.png";

interface SearchBarProps {
  suggestions: string[]; // Array of suggestions for auto-complete
  onSearch: (query: string) => void; // Callback for handling search
}

const SearchBar: React.FC<SearchBarProps> = ({ suggestions, onSearch }) => {
  const [query, setQuery] = useState<string>("");
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;
    setQuery(inputValue);

    // Filter suggestions based on input
    if (inputValue) {
      const matches = suggestions.filter((sug) =>
        sug.toLowerCase().startsWith(inputValue.toLowerCase())
      );
      setFilteredSuggestions(matches);
    } else {
      setFilteredSuggestions([]);
    }
  };

  const handleSearch = () => {
    onSearch(query);
    setQuery("");
    setFilteredSuggestions([]);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    onSearch(suggestion);
    setFilteredSuggestions([]);
  };


  return (
    <div style={{ width: "70%", minHeight: "50px", backgroundColor: "white", borderRadius: "25px", marginTop: "20px", justifyItems: "center" }}>
      <div style={{ width: "100%", minHeight: "50px", backgroundColor: "white", borderRadius: "25px", marginTop: "20px", justifyItems: "center"}}>
      <TextField
      fullWidth
        // variant="outlined"
        value={query}
        onChange={handleInputChange}
        placeholder="Recent form of virat kohli"
        style={{
            height: "20px",
            textAlign: "center",
            fontSize: "2px",
            width: "100%",
            border: "none",
            borderRadius: "25px",
            fontFamily: "Montserrat"
        }}
        InputProps={{
            startAdornment:(
                <InputAdornment position="start">
                    <IconButton onClick={handleSearch}>
                        <SearchIcon />
                    </IconButton>
                </InputAdornment>
            ),
          endAdornment: (
            <InputAdornment position="end">
              <IconButton onClick={handleSearch}>
                <SearchIcon />
              </IconButton>
            </InputAdornment>
          ),
        }}
        sx={{
            "& .MuiOutlinedInput-root": {
              "& fieldset": {
                border: "none", // Remove outer border
              },
              "&:hover fieldset": {
                border: "none", // No border on hover
              },
              "&.Mui-focused fieldset": {
                border: "none", // Remove focus border
              },
            },
        }}
      />
      </div>

      <div>
      {filteredSuggestions.length > 0 && (
        <List style={{ width: "100%", borderRadius: "4px", marginTop: "8px", fontFamily: "Montserrat" }}>
          {filteredSuggestions.map((suggestion, index) => (
            <ListItem key={index} disablePadding>
              <ListItemButton onClick={() => handleSuggestionClick(suggestion)}>
                <ListItemText primary={suggestion} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      )}
      </div>
      

      
    </div>
  );
};

export default SearchBar;
