import React from "react";
import DragZone from "../../components/dragzone/DragZone";

import { CardData } from "./teamPage";

import "../teamPage/teamPage.css";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { useNavigate } from "react-router-dom";

export interface EditComponentProps {
  showContainer: boolean;
  toggleContainer: () => void;
  dragZoneCards: CardData[];
  filterType: "points" | "cost";
  applyFilter: (filter: "points" | "cost") => void;
  handleSwapCards: (card: CardData) => void;
  selectedCard: CardData | null;
}

const EditComponent: React.FC<EditComponentProps> = ({
  showContainer,
  toggleContainer,
  dragZoneCards,
  filterType,
  applyFilter,
  handleSwapCards,
  selectedCard,
}) => {


  const navigation = useNavigate();

  if (!showContainer) {
    return (
      <div className="video-card">
        <div className="video-section"></div>
        <button className="edit-team" onClick={toggleContainer}>
          Edit Team
        </button>
      </div>
    );
  }



  return (
    <div className="flex items-center justify-center h-full border-10 -mb-10 border-red-600">

    <DndProvider backend={HTML5Backend}>
        <div className="side-container">
          <DragZone
            cards={dragZoneCards}
            filterType={filterType}
            applyFilter={applyFilter}
            onSwap={handleSwapCards}
            onDrag={handleSwapCards}
            selectedCard={selectedCard}
          />
          <button className="complete-team" onClick={() => {navigation("/player-info");}}>
            COMPLETE TEAM
          </button>
          {/* <button className="complete-team" onClick={() => {}}>
            Submit Team
          </button> */}
        </div>
      
    </DndProvider>
    </div>
  );
};

export default EditComponent;
