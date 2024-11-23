import React from "react";
import { useDrop } from "react-dnd";
import "./DropZone.css";
import MyImage from "../../assets/images/virat_kohli.png"; // Replace with your player image
import milogo from "../../assets/images/mumbai_indians.png";
import rcblogo from "../../assets/images/rcb_logo.png";
import { CardData } from "../../pages/teamPage/teamPage";

interface DropZoneProps {
  cards: CardData[];
  onRemove: (card: CardData) => void;
  isedit: boolean
}

const DropZone: React.FC<DropZoneProps> = ({ cards, onRemove, isedit }) => {
  const [, dropRef] = useDrop({
    accept: "CARD",
    drop: (item: { card: CardData }) => ({ ...item }),
  });

  const row1 = cards.slice(0, 3); // First 3 cards
  const row2 = cards.slice(3, 7); // Next 4 cards
  const row3 = cards.slice(7, 11); // Last 4 cards

  return (
    <div ref={dropRef} className="dropzone-container">
      {/* <h3 className="dropzone-title">DropZone</h3> */}
      {/* Rows */}
      <div className="dropzone-row">
        {row1.map((card) => (
          <DroppableCard key={card.id} card={card} onRemove={onRemove} isedit={isedit} />
        ))}
      </div>
      <div className="dropzone-row">
        {row2.map((card) => (
          <DroppableCard key={card.id} card={card} onRemove={onRemove} isedit={isedit} />
        ))}
      </div>
      <div className="dropzone-row">
        {row3.map((card) => (
          <DroppableCard key={card.id} card={card} onRemove={onRemove} isedit={isedit} />
        ))}
      </div>
    </div>
  );
};

const DroppableCard: React.FC<{
  card: CardData;
  onRemove: (card: CardData) => void;
  isedit: boolean;
}> = ({ card, onRemove, isedit }) => {
  return (
    <div className="droppable-card">
      
      <div className="card-overlay">
        {card.name}
        <div style={{fontSize: "5px"}}>
          {card.type}
        </div>
        <div style={{fontSize: "12px", fontWeight: 900}}>
          {card.score}
        </div>
        <div style={{fontSize: "7px", fontWeight: 900, color: "red", marginBottom: "2px"}}>
          {card.cost}
        </div>
      </div>

      {isedit && (
        <button className="remove-button" onClick={() => onRemove(card)}>
          X
        </button>
      )}
      
      <div className="droppable-card-points">

        <div>
          207
          <div style={{fontSize: 4}}>
            PTS
          </div>
        </div>

        

        <img className="team-logo" src={card.team === "RCB" ? rcblogo : milogo} alt="Player" />

        {/* <div style={{fontSize: 6}}>
          BAT
        </div> */}

      </div>
      <img className="card-image" src={MyImage} alt="Player" />

    </div>
  );
};

export default DropZone;
