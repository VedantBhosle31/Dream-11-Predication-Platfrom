import React, { useState } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import DropZone from "../../components/dropzone/DropZone";
import DragZone from "../../components/dragzone/DragZone";
import "./teamPage.css";
import EditComponent from "./EditComponent";

export interface CardData {
  id: string;
  name: string;
  type: string;
  team: string;
  points: string;
  cost: string;
  score: string;
  cvc: string;
}

export interface TeamPageProps {
  showContainer: boolean;
  toggleContainer: () => void;
  dragZoneCards: CardData[];
  dropZoneCards: CardData[];
  filterType: "points" | "cost";
  applyFilter: (filter: "points" | "cost") => void;
  handleSwapCards: (card: CardData) => void;
  selectedCard: CardData | null;
  removeFromDropZone: (card: CardData) => void;
  handleSelectCard: (card: CardData) => void;
}

const TeamPage: React.FC<TeamPageProps> = ({
  showContainer,
  toggleContainer,
  dragZoneCards,
  dropZoneCards,
  filterType,
  applyFilter,
  handleSwapCards,
  selectedCard,
  removeFromDropZone,
  handleSelectCard,
}) => {
  return (
    <DndProvider backend={HTML5Backend}>
      <div
        className="main-container"
        style={{ justifyContent: showContainer ? "center" : "center" }}
      >
        <div className={`team-container ${showContainer ? "shifted" : ""}`}>
          <DropZone
            cards={dropZoneCards}
            onRemove={removeFromDropZone}
            isedit={showContainer}
            handleSelectCard={handleSelectCard}
            selectedCard={selectedCard}
          />

          <div className="bottom-stats">
            <div
              style={{
                color: "red",
                fontSize: "60px",
                alignContent: "center",
                justifyItems: "center",
                fontWeight: "700",
                fontFamily: "Montserrat",
              }}
            >
              688
              <div style={{ color: "white", fontSize: "10px" }}>
                EXPECTED TEAM SCORE
              </div>
            </div>

            <div
              style={{
                color: "red",
                fontSize: "60px",
                alignContent: "center",
                justifyItems: "center",
                fontWeight: "700",
                fontFamily: "Montserrat",
              }}
            >
              132
              <div style={{ color: "white", fontSize: "10px" }}>TEAM COST</div>
            </div>
          </div>
        </div>
      </div>
    </DndProvider>
  );
};

export default TeamPage;
