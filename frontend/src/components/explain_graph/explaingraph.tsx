import React, { useState } from "react";
import "./explaingraph.css";
import SparklesIcon from "@mui/icons-material/AutoAwesome";
import { Box, Modal } from "@mui/material";
import { color } from "framer-motion";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
    transform: 'translate(-50%, -50%)',
  width: 400,
  height: 300,
  bgcolor: "#1E1E1E",
  border: "2px solid black",
  boxShadow: 24,
  p: 4,
  display: "flex",
  flexDirection: "column",
  // justifyContent: "space-between",
  fontFamily: "Montserrat",
  //   color:"white"
  borderRadius: "10px",
  overflowY: 'auto',  // Enable vertical scrolling
  overflowX: 'hidden',  // Hide horizontal overflow
  // overflow: 'auto', // Hide text overflow
  // textOverflow: 'ellipsis',  // Show ellipsis when the text overflows
  // whiteSpace: 'nowrap',  // Prevent the text from wrapping
  color:"white"
};

interface ExplainGraphProps {
  title:string
  description:string
}

const ExplainGraphButton: React.FC<ExplainGraphProps> = ({title, description}) => {
  var [isExplainExpanded, setExplainExpanded] = useState(false);
  const handleExplainOpen = () => setExplainExpanded(true);
  const handleExplainClose = () => setExplainExpanded(false);

  <button className="ask-ai-button">
    <span className="icon">
      <SparklesIcon />
    </span>
    <span className="text-xs">Explain Graph</span>
  </button>;

  return (
    <div>
      <button className="ask-ai-button" onClick={handleExplainOpen}>
        <span className="icon">
          <SparklesIcon />
        </span>
        <span className="text-xs">Explain Graph</span>
      </button>
      <Modal
        open={isExplainExpanded}
        onClose={handleExplainClose}
      >
        <Box sx={style}>
          <h3>{title}</h3>
          {description}
          {/* Lorem Ipsum Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum */}
        </Box>
      </Modal>
    </div>
  );
};

export default ExplainGraphButton;
