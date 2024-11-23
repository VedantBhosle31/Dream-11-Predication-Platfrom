// import React from "react";
// import { useDrag } from "react-dnd";
// import { CardData } from "../../App";

// interface DragZoneProps {
//   cards: CardData[];
//   onDrag: (card: CardData) => void;
//   style?: React.CSSProperties;
// }

// const DragZone: React.FC<DragZoneProps> = ({ cards, onDrag, style }) => {
//   return (
//     <div style={{ ...style, padding: "10px" }}>
//       <h3>DragZone</h3>
//       {cards.map((card) => (
//         <DraggableCard key={card.id} card={card} onDrag={onDrag} />
//       ))}
//     </div>
//   );
// };

// const DraggableCard: React.FC<{
//   card: CardData;
//   onDrag: (card: CardData) => void;
// }> = ({ card, onDrag }) => {
//   const [{ isDragging }, dragRef] = useDrag({
//     type: "CARD",
//     item: { card },
//     end: (item, monitor) => {
//       if (monitor.didDrop()) {
//         onDrag(item.card);
//       }
//     },
//     collect: (monitor) => ({
//       isDragging: monitor.isDragging(),
//     }),
//   });

//   return (
//     <div
//       ref={dragRef}
//       style={{
//         opacity: isDragging ? 0.5 : 1,
//         cursor: "move",
//         padding: "10px",
//         border: "1px solid gray",
//         marginBottom: "5px",
//         backgroundColor: "lightblue",
//       }}
//     >
//       {card.content}
//     </div>
//   );
// };

// export default DragZone;

import React from "react";
import { useDrag } from "react-dnd";
import "./DragZone.css";
import MyImage from "../../assets/images/virat_kohli.png"; // Replace with your player image
import { CardData } from "../../pages/teamPage/teamPage";

interface DragZoneProps {
  cards: CardData[];
  onDrag: (card: CardData) => void;
}

const DragZone: React.FC<DragZoneProps> = ({ cards, onDrag }) => {
  return (
    <div style={{backgroundColor: "#CD3939", padding: "20px", borderRadius: "15px"}}>
      
      <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between"}}>
        
        <h3 className="dragzone-title">Player</h3>
        <div style={{alignContent: "center", justifyContent: "space-evenly"}}>
          <button className="cost-filter-button" onClick={() => {}}>
            Cost
          </button>
          <button className="score-filter-button" onClick={() => {}}>
            Score
          </button>
        </div>

      </div>

      <div className="dragzone-container">
        <div className="dragzone-cards">
          {cards.map((card) => (
            <DraggableCard key={card.id} card={card} onDrag={onDrag} />
          ))}
        </div>
      </div>

    </div>
    
  );
};

const DraggableCard: React.FC<{
  card: CardData;
  onDrag: (card: CardData) => void;
}> = ({ card, onDrag }) => {
  const [{ isDragging }, dragRef] = useDrag({
    type: "CARD",
    item: { card },
    end: (item) => {
      if (item) {
        onDrag(item.card);
      }
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  return (
    <div
      ref={dragRef}
      className="draggable-card"
      style={{ opacity: isDragging ? 0.5 : 1 }}
    >
      <div className="card-image-container">
        <img className="card-image-drag" src={MyImage} alt="Player" />
      </div>

      <div className="draggable-card-name">
        
        <div>
          {card.name}
        </div>

        <div style={{fontSize: "8px"}}>
          {card.type}
        </div>

      </div>

      
    </div>
  );
};

export default DragZone;
