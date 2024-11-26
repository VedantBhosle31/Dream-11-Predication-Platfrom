import React, { useState } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import DropZone from "../../components/dropzone/DropZone";
import DragZone from "../../components/dragzone/DragZone";
import "./teamPage.css";
import { useNavigate } from "react-router-dom";

export interface CardData {
  id: string;
  name: string;
  type: string;
  team: string;
  points: string;
  cost: string;
  score: string;
}

const TeamPage: React.FC = () => {
  const navigate = useNavigate();
  const initialDropZoneCards: CardData[] = [
    {
      id: "1",
      name: "FAF DU PLESSIS",
      type: "BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "2",
      name: "VIRAT KOHLI",
      type: "BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "3",
      name: "GLENN MAXWELL",
      type: "ALL-ROUNDER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "4",
      name: "DINESH KARTHIK",
      type: "WICKETKEEPER-BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "5",
      name: "MOHAMMED SIRAJ",
      type: "BOWLER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "6",
      name: "WILL JACKS",
      type: "ALL-ROUNDER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "7",
      name: "MAHIPAL LOMROR",
      type: "ALL-ROUNDER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "8",
      name: "REECE TOPLEY",
      type: "BOWLER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "9",
      name: "RAJAT PATIDAR",
      type: "BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "10",
      name: "ANUJ RAWAT",
      type: "WICKETKEEPER-BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "11",
      name: "ALZARRI JOSEPH",
      type: "BOWLER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
    },
  ];

  const initialDragZoneCards: CardData[] = [
    {
      id: "12",
      name: "ROHIT SHARMA",
      type: "BATSMAN",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "13",
      name: "SURYAKUMAR YADAV",
      type: "BATSMAN",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "14",
      name: "HARDIK PANDYA",
      type: "ALL-ROUNDER",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "15",
      name: "TIM DAVID",
      type: "BATSMAN",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "16",
      name: "ISHAN KISHAN",
      type: "WICKETKEEPER-BATSMAN",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "17",
      name: "JASPRIT BUMRAH",
      type: "BOWLER",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "18",
      name: "NEHAL WADHERA",
      type: "BATSMAN",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "19",
      name: "TILAK VARMA",
      type: "ALL-ROUNDER",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "20",
      name: "AKASH MADHWAL",
      type: "BOWLER",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "21",
      name: "KUMAR KARTIKEYA",
      type: "BOWLER",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
    {
      id: "22",
      name: "PIYUSH CHAWLA",
      type: "BOWLER",
      team: "MI",
      points: "207",
      cost: "12",
      score: "89",
    },
  ];

  const [dropZoneCards, setDropZoneCards] =
    useState<CardData[]>(initialDropZoneCards);
  const [dragZoneCards, setDragZoneCards] =
    useState<CardData[]>(initialDragZoneCards);

  const moveToDropZone = (card: CardData) => {
    if (dropZoneCards.length >= 11) {
      // If DropZone is full, swap the last card back to DragZone
      const cardToSwap = dropZoneCards[dropZoneCards.length - 1]; // Get the last card
      const updatedDropZone = [...dropZoneCards.slice(0, -1), card]; // Replace last card with new card

      setDropZoneCards(updatedDropZone);
      setDragZoneCards([
        ...dragZoneCards.filter((c) => c.id !== card.id),
        cardToSwap,
      ]);
    } else {
      // If DropZone is not full, simply add the card
      setDropZoneCards([...dropZoneCards, card]);
      setDragZoneCards(dragZoneCards.filter((c) => c.id !== card.id));
    }
  };

  const removeFromDropZone = (card: CardData) => {
    setDropZoneCards(dropZoneCards.filter((c) => c.id !== card.id));
    setDragZoneCards([...dragZoneCards, card]);
  };

  const [showContainer, setShowContainer] = useState(false);

  const toggleContainer = () => {
    setShowContainer((prev) => !prev);
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div
        style={{
          display: "flex",
          // width: "8000000px",
          height: "110px",
          // backgroundColor: "grey",
          alignItems: "center",
          // margin: "auto"
          justifyContent: "space-around",
        }}
      ></div>

      <div
        className={`main-container ${showContainer ? "shifted" : ""}`}
        style={{
          display: "flex",
          justifyContent: showContainer ? "center" : "center",
        }}
      >
        <div className={`team-container ${showContainer ? "shifted" : ""}`}>
          <DropZone
            cards={dropZoneCards}
            onRemove={removeFromDropZone}
            isedit={showContainer}
          />

          <div
            className="bottom-buttons"
            style={{ display: "flex", justifyContent: "space-evenly" }}
          >
            <button
              className={`expected-team-score ${
                showContainer ? "shifted" : ""
              }`}
              onClick={() => {}}
            >
              Expected Team Score
            </button>

            <button
              className={`team-cost ${showContainer ? "shifted" : ""}`}
              onClick={() => {}}
            >
              Team Cost
            </button>

            {!showContainer && (
              <button className="edit-team" onClick={toggleContainer}>
                Edit Team
              </button>
            )}

            {!showContainer && (
              <button className="submit-team" onClick={() => {}}>
                Submit Team
              </button>
            )}
          </div>
        </div>

        {showContainer && (
          // <div className={`side-container ${showContainer ? "visible" : ""}`}>
          <div className="side-container">
            {/* <div style={{
          // position: "relative",
          // display: "flex",
          // backgroundColor: "darkgrey",
          width: "90px",
          height: "110px",
          borderRadius: 5
          }}></div> */}

            <DragZone
              cards={dragZoneCards}
              onDrag={moveToDropZone}
              // style={{ width: "50%", border: "1px solid black" }}
            />

            <button
              className="complete-team"
              onClick={() => {
                navigate("/player-info");
              }}
            >
              Complete Team
            </button>

            <button className="complete-and-submit-team" onClick={() => {}}>
              Complete and Submit Team
            </button>
          </div>
        )}
      </div>
    </DndProvider>
  );
};

export default TeamPage;
