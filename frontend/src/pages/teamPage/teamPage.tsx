import React, { useEffect, useState } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import DropZone from "../../components/dropzone/DropZone";
import DragZone from "../../components/dragzone/DragZone";
import "./teamPage.css";
import EditComponent from "./EditComponent";
import { getSessionData } from "../../utils/sessionStorageUtils";
import { BackendData } from "../../api/fetchData";
import { CardData } from "../../SlidingPanels";

// export interface CardData {
//   id: string;
//   name: string;
//   type: string;
//   team: string;
//   points: string;
//   cost: string;
//   score: string;
//   cvc: string;
// }

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
  handleSetCVC: (id: string, role: "C" | "VC") => void;
}

type DataType = {
  Date: string;
  Previous_Runs: number;
};

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
  handleSetCVC,
}) => {
  const [fetchedData, setData] = useState<DataType[] | null>(null);

  useEffect(() => {
    const cachedData = getSessionData<BackendData[]>("runsData");
    console.log(cachedData);
    if (cachedData) {
      setData(cachedData);
    }
  }, []);

  // if (!fetchedData) return <div>No data available. Go back to the home page to fetch data.</div>;

  return (
    <DndProvider backend={HTML5Backend}>
        {
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
                  handleSetCVC={handleSetCVC}
                />

              <div className="bottom-stats">
                <div
                  style={{
                    color: "red",
                    fontSize: "280%",
                    alignContent: "center",
                    justifyItems: "center",
                    fontWeight: "700",
                    fontFamily: "Montserrat",
                  }}
                >
                  688
                  <div style={{ color: "white", fontSize: "20%" }}>
                    EXPECTED TEAM SCORE
                  </div>
                </div>

                <div
                  style={{
                    color: "red",
                    fontSize: "280%",
                    alignContent: "center",
                    justifyItems: "center",
                    fontWeight: "700",
                    fontFamily: "Montserrat",
                  }}
                >
                  132
                  <div style={{ color: "white", fontSize: "20%" }}>
                    TEAM COST
                  </div>
                </div>
              </div>
            </div>
          </div>
        }
    </DndProvider>
  );
};

export default TeamPage;
