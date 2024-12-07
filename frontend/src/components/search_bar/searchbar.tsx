import React, { useState } from "react";
import "./SearchBar.css";
import { IconButton, InputBase, Paper, List, ListItem } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import SparklesIcon from "@mui/icons-material/AutoAwesome";
import usePlayerStore from "../../store/playerStore";

interface SearchBarProps {
  suggestions: string[];
  feature_name: string;
  player_name: string;
  date: string;
  model: string;
  player_opponents: string;
  player_type: string;
}

const SearchBar: React.FC<SearchBarProps> = ({
  suggestions,
  feature_name,
  // user_task,
  player_name,
  date,
  model,
  player_opponents,
  player_type,
}) => {
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setShowSuggestions(event.target.value.length > 0);
  };

  const handleSearch = async () => {
    if (searchTerm.trim() !== "") {
      const updatedUserTask = searchTerm;

      await fetchData(updatedUserTask);
      
      setSearchTerm("");
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setSearchTerm(suggestion);
    setShowSuggestions(false);
    fetchData(suggestion);
  };

  const { playerdescription, setplayerdescription } = usePlayerStore();


  const fetchData = async (user_task: string) => {
    const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/genai/describe-player/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Tell the server it's JSON
      },
      body: JSON.stringify({
        feature_name: "query_answering",
        user_task: user_task,
        player_name: player_name,
        date: date,
        model: model,
        player_opponents: player_opponents,
        player_type: player_type,
      }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const fetcheddata = await response.json();
    console.log("Fetched Data:", fetcheddata["description"]);


    setplayerdescription(fetcheddata["description"]);
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
        onClick={handleSearch}
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
