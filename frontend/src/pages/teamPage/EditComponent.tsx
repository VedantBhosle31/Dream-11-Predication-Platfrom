import React, { useState } from "react";
import DragZone from "../../components/dragzone/DragZone";


import "../teamPage/teamPage.css";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { useNavigate } from "react-router-dom";
import VideoPlayer from "../../components/video_player/videoplayer";
import Slideshow from "../../components/slide-show/SlideShow";
import { CardData } from "../../SlidingPanels";
import {motion} from 'framer-motion'

export interface EditComponentProps {
  showContainer: boolean;
  toggleContainer: () => void;
  dragZoneCards: CardData[];
  dropZoneCards: CardData[];
  filterType: "points" | "cost";
  applyFilter: (filter: "points" | "cost") => void;
  handleSwapCards: (card: CardData) => void;
  selectedCard: CardData | null;
  addToDropZone: (card: CardData) => void;
}

const EditComponent: React.FC<EditComponentProps> = ({
  showContainer,
  toggleContainer,
  dragZoneCards,
  dropZoneCards,
  filterType,
  applyFilter,
  handleSwapCards,
  selectedCard,
  addToDropZone,
}) => {
  const navigation = useNavigate();

  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  // Replace this with the actual URL of your Django backend
  const backendUrl = "http://127.0.0.1:8000/video/stream/stream_video.mp4";

  const handleButtonClick = () => {
    // Check if Captain and Vice-Captain are assigned
    const hasCaptain = dropZoneCards.some((card) => card.cvc === "C");
    const hasViceCaptain = dropZoneCards.some((card) => card.cvc === "VC");

    if (!hasCaptain || !hasViceCaptain) {
      alert("Assign a Captain and Vice-Captain to your dream team!");
      return;
    }

    // Check if 11 players are selected in the drag zone
    if (dragZoneCards.length > 11) {
      alert("Complete 11 players of your dream team!");
      return;
    }

    // Navigate to the player-info page if both conditions are satisfied
    navigation("/player-info");
  };

  if (!showContainer) {
    return (
      <div className="video-section">
        <div className="video-wrapper">

          <div className="video-card">
            {/* {<VideoPlayer videoUrl={backendUrl} />} */}
            <Slideshow />
          </div>

          <motion.button   whileTap={{
          scale: 0.98,
        }} whileHover={{scale:1.02}} className="edit-team" onClick={toggleContainer}>
            EDIT TEAM
          </motion.button>

        </div>
        
      </div>
    );
  }

  return (
    <div className="dragzone-section">
      <DndProvider backend={HTML5Backend}>
        <div className="dragzone-wrapper">
          <DragZone
            cards={dragZoneCards}
            filterType={filterType}
            applyFilter={applyFilter}
            onSwap={handleSwapCards}
            onDrag={handleSwapCards}
            selectedCard={selectedCard}
            addToDropZone={addToDropZone}
          />
      
          <motion.button   whileTap={{
          scale: 0.98,
        }} whileHover={{scale:1.02}} className="complete-team" onClick={handleButtonClick}>
            COMPLETE TEAM
          </motion.button>
          
          {/* <button className="complete-team" onClick={() => {}}>
            Submit Team
          </button> */}
        </div>
      </DndProvider>
    </div>
  );
};

export default EditComponent;
