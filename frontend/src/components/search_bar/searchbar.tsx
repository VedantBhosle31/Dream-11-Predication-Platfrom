import React, { useState } from "react";
import "./SearchBar.css";
import { IconButton, InputBase, Paper, List, ListItem } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import SparklesIcon from "@mui/icons-material/AutoAwesome";

interface SearchBarProps {
  suggestions: string[];
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ suggestions, onSearch }) => {
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setShowSuggestions(event.target.value.length > 0);
  };

  const handleSearch = () => {
    if (searchTerm.trim() !== "") {
      onSearch(searchTerm);
      setSearchTerm("");
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setSearchTerm(suggestion);
    setShowSuggestions(false);
    onSearch(suggestion);
  };

  return (
    <Paper
      component="form"
      elevation={3}
      style={{
        display: "flex",
        alignItems: "center",
        borderRadius: "25px",
        backgroundColor: "#333",
        color: "white",
        width: "400px",
      }}
    >
      <SearchIcon style={{ margin: "0 8px", color: "#bbb" }} />

      {/* Search Input */}
      <InputBase
        placeholder="Search for player stats or recent form..."
        style={{ color: "white", flex: 1, fontFamily: "Montserrat" }}
        value={searchTerm}
        onChange={handleInputChange}
        onFocus={() => setShowSuggestions(true)}
      />

      <IconButton
        type="button"
        style={{ marginLeft: "8px", color: "red", fillOpacity: "0.5" }}
        onClick={() => alert("Example: Recent Form of Virat Kohli")}
      >
        <SparklesIcon />
      </IconButton>

      {/* Suggestions Dropdown */}
      {showSuggestions && (
        <List
          style={{
            position: "absolute",
            bottom: "60px",
            left: "0",
            width: "31%",
            backgroundColor: "#444",
            color: "white",
            borderRadius: "10px",
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.2)",
            zIndex: 1000,
            fontFamily: "Montserrat",
          }}
        >
          {suggestions
            .filter((suggestion) =>
              suggestion.toLowerCase().includes(searchTerm.toLowerCase())
            )
            .map((suggestion, index) => (
              <ListItem
                key={index}
                // button
                onClick={() => handleSuggestionClick(suggestion)}
                style={{
                  padding: "10px",
                  borderBottom: "1px solid #555",
                  color: "white",
                  fontFamily: "Montserrat",

                }}
              >
                {suggestion}
              </ListItem>
            ))}
        </List>
      )}
    </Paper>
  );
};

export default SearchBar;