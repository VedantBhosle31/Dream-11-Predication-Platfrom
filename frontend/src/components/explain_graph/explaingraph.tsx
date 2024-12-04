import React, { useState } from "react";
import "./explaingraph.css";
import SparklesIcon from "@mui/icons-material/AutoAwesome";
import { Box, Modal } from "@mui/material";
import { color } from "framer-motion";
import ReactLoading from "react-loading";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
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
  overflowY: "auto", // Enable vertical scrolling
  overflowX: "hidden", // Hide horizontal overflow
  // overflow: 'auto', // Hide text overflow
  // textOverflow: 'ellipsis',  // Show ellipsis when the text overflows
  // whiteSpace: 'nowrap',  // Prevent the text from wrapping
  color: "white",
};

interface ExplainGraphProps {
  title: string;
  explaindate: string;
  opponents: string;
  typeofplayer: string;
  player_name:string;
  model:string
}

const ExplainGraphButton: React.FC<ExplainGraphProps> = ({ title, explaindate,  opponents, typeofplayer, model, player_name}) => {
  var [isExplainExpanded, setExplainExpanded] = useState(false);
  var [graphdescription, setgraphdescription] = useState();
  const [isLoading, setisLoading] =  useState(false);
  const handleExplainOpen = () => setExplainExpanded(true);
  const handleExplainClose = () => setExplainExpanded(false);

  const fetchExplainData = async () => {
    setisLoading(true);
    // setExplainExpanded(true);

    console.log("here got details", title, explaindate,  opponents, typeofplayer, model, player_name );

    const response = await fetch("http://127.0.0.1:8000/genai/explain-graph/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Tell the server it's JSON
      },
      body: JSON.stringify({
        graph_name: title,
        date: explaindate,
        player_opponents:opponents,
        player_type:typeofplayer,
        player_name:player_name,
        model:model
      }), // Convert the data to a JSON string
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const fetchedexplaindata = await response.json();

    console.log(fetchedexplaindata["explanation"])

    setgraphdescription(fetchedexplaindata["explanation"]);
    setisLoading(false);
    setExplainExpanded(true);

  };

  <button className="ask-ai-button">
    <span className="icon">
      <SparklesIcon />
    </span>
    <span className="text-xs">Explain Graph</span>
  </button>;

  return (
    <div>
      {isLoading === false ? 
      (
      <button className="ask-ai-button" onClick={fetchExplainData}>
        <span className="icon">
          <SparklesIcon />
        </span>
        <span className="text-xs">Explain Graph</span>
      </button>): <ReactLoading type="spin" color="#0000FF"
                height={15} width={15} />
      
      }
      <Modal open={isExplainExpanded} onClose={handleExplainClose}>
        <Box sx={style}>
          <h3>{title}</h3>
          <div style={{width:"90%", height:"60%"}}>
            {graphdescription}
          </div>
          {/* {graphdescription} */}
          {/* Lorem Ipsum Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum */}
        </Box>
      </Modal>
    </div>
  );
};

export default ExplainGraphButton;
