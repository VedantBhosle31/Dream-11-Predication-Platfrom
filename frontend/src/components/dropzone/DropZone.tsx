import React from "react";
import { useDrop } from "react-dnd";
import "./DropZone.css";
import MyImage from "../../assets/images/virat_kohli.png";
import milogo from "../../assets/images/mumbai_indians.png";
import rcblogo from "../../assets/images/rcb_logo.png";
import { IconButton } from "@mui/material";
import { AddCircleOutline, RemoveCircleOutline } from "@mui/icons-material";
import { CardData } from "../../SlidingPanels";

interface DropZoneProps {
  cards: CardData[];
  onRemove: (card: CardData) => void;
  isedit: boolean;
  handleSelectCard: (card: CardData) => void;
  selectedCard: CardData | null;
}

const DropZone: React.FC<DropZoneProps> = ({ cards, onRemove, isedit, handleSelectCard, selectedCard }) => {
  
  const [, dropRef] = useDrop({
    accept: "CARD",
    drop: (item: { card: CardData }) => ({ ...item }),
  });

  // Sort cards so that captain and vc comes first
  const sortedCards = [...cards].sort((a, b) => {
    if (a.cvc === "C" && b.cvc !== "C") return -1; // Prioritize "C"
    if (a.cvc === "VC" && b.cvc !== "VC" && b.cvc !== "C") return -1; 
    return 0; 
  });

  const totalSlots = 11;

  
  const allSlots = [...sortedCards, 
    ...Array.from({ length: totalSlots - sortedCards.length }, () => null),
  ];

  const row1 = allSlots.slice(0, 3); // First 3 cards
  const row2 = allSlots.slice(3, 7); // Next 4 cards
  const row3 = allSlots.slice(7, 11); // Last 4 cards

  return (
    <div ref={dropRef} className="dropzone-container">
      <div className="dropzone-row">
        {row1.map((card, index) => (
          card ? (<DroppableCard key={card.id || `placeholder-${index}`} card={card} onRemove={onRemove} isedit={isedit} onSelectCard={handleSelectCard} selectedCard={selectedCard}/>)
          : (
            <Placeholder key={`placeholder-${index}`} />
          )
        ))}
      </div>
      <div className="dropzone-row">
        {row2.map((card, index) => (
          card ? (<DroppableCard 
            key={card.id} 
            card={card} 
            onRemove={onRemove} 
            isedit={isedit} 
            onSelectCard={handleSelectCard} 
            selectedCard={selectedCard}
          />)
          : (
            <Placeholder key={`placeholder-${index}`} />
          )
        ))}
      </div>
      <div className="dropzone-row">
        {row3.map((card, index) => (
          card ? (
          <DroppableCard 
            key={card.id} 
            card={card} 
            onRemove={onRemove} 
            isedit={isedit} 
            onSelectCard={handleSelectCard}
            selectedCard={selectedCard}
          />)
          : (
            <Placeholder key={`placeholder-${index}`} />
          )
        ))}
      </div>
    </div>
  );
};

const DroppableCard: React.FC<{
  card: CardData;
  onRemove: (card: CardData) => void;
  onSelectCard: (card: CardData) => void;
  isedit: boolean;
  selectedCard: CardData | null;
}> = ({ card, onRemove, isedit, onSelectCard, selectedCard }) => {
  return (
    <div className="droppable-card" onClick={() => {}} style={{border: selectedCard === card ? "2px solid white": "none"}} onDropCapture={() => onSelectCard(card)}>
      <div className="left-half"></div>
      <div className="right-half"></div>

      <div className="droppable-card-points">

        <div>
           {card.points}
           <div style={{fontSize: 6, color: "red"}}>
             PTS
           </div>
        </div>

         <img className="team-logo" src={card.team === "RCB" ? rcblogo : milogo} alt="Player" />

      </div>
      
      <div className="card-overlay">
        {card.name}
        <div className="card-overlay-row">
        <div style={{fontSize: "9px", display: "flex"}}>
          {card.score}
          <div style={{color: "red"}}>RNS</div>
         </div>
         <div style={{fontSize: "9px", fontWeight: 900}}>
           {card.type}
         </div>
         <div style={{fontSize: "9px", fontWeight: 900, display: "flex"}}>
           {card.cost}
           <div style={{color: "red"}}>CR</div>
         </div>
        </div>
      </div>

      {isedit && (

        <button className="remove-button" onClick={() => onRemove(card)} >
         <RemoveCircleOutline style={{ width: "13px", height: "13px",}}/>
        </button>
      //   <button className="remove-button" onClick={() => onSelectCard(card)} onDoubleClick={() => onRemove(card)}>
      //   <RemoveCircleOutline style={{ width: "13px", height: "13px",}}/>
      //  </button>
      )}

      <img className="card-image" src={MyImage} alt="Player" />

    </div>
  );
};

const Placeholder: React.FC = () => {
  return (
    <div className="placeholder-card">
      <div className="placeholder-border">
        <IconButton onClick={() => {}}>
          <AddCircleOutline style={{color: "gray", opacity: "0.4", width: "50%", height: "50%"}}/>
        </IconButton>
      </div>
    </div>
  );
};

export default DropZone;