import React, { useState } from "react";
import { useDrag } from "react-dnd";
import "./DragZone.css";
import MyImage from "../../assets/images/virat_kohli.png"; // Replace with your player image
import { IconButton} from "@mui/material";
import { AddCircleOutline, ArrowDownward, ArrowUpward } from "@mui/icons-material";
import { CardData } from "../../SlidingPanels";


interface DragZoneProps {
  cards: CardData[];
  filterType: "points" | "cost";
  onDrag: (card: CardData) => void;
  applyFilter: (filter: "points" | "cost") => void;
  onSwap: (card: CardData) => void;
  selectedCard: CardData | null
}

const DragZone: React.FC<DragZoneProps> = ({ cards, filterType, onDrag, applyFilter, onSwap  }) => {

  const [ascending, setAscending] = useState(true);

  const handleFilterClick = (filter: "points" | "cost") => {
    if (filterType === filter) {
      setAscending(!ascending);
    } else {
      setAscending(true);
      applyFilter(filter);
    }
  };
  
  // Filter cards based on selected filterType
  const filteredCards = [...cards].sort((a, b) => {
    const valueA = filterType === "points" ? Number(a.points) : Number(a.cost);
    const valueB = filterType === "points" ? Number(b.points) : Number(b.cost);
    return ascending ? valueA - valueB : valueB - valueA;
  });
  
  
  
  return (
    <div style={{backgroundColor: "#1f1f1f", padding: "20px", borderRadius: "15px", height: "88%",  width: "100%"}}>
      
      <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between"}}>
        
        <h3 className="dragzone-title">Player</h3>

        <div style={{display: "flex", alignContent: "center", justifyContent: "space-between", width: "50%"}}>
          
          <button className={`score-filter-button ${filterType === "points" ? "selected" : ""}`} onClick={() => handleFilterClick("points")}>
            EXPT SCORE
            <div className={filterType === "points" && ascending ? "selected" : ""}>
              {filterType === "points" && ascending ? (
                <ArrowUpward />
              ): <ArrowDownward />
            }
              
            </div>
          </button>
          
          <button className={`cost-filter-button ${filterType === "cost" ? "selected" : ""}`} onClick={() => handleFilterClick("cost")}>
            COST
            <div className={filterType === "cost" && ascending ? "selected" : ""}>
              {filterType === "cost" && ascending ? (
                <ArrowUpward />
              ): <ArrowDownward />
            }
            </div>
          </button>
          <div style={{width: "20%"}}>

          </div>
          {/* <button className="score-filter-button" onClick={() => {}}>
            Score
          </button> */}
        </div>

      </div>

      <div className="dragzone-container" style={{height: "95%", width: "100%"}}>
        <div className="dragzone-cards">
          {filteredCards.map((card) => (
            <DraggableCard 
              key={card.id}
              card={card}
              onDrag={onDrag}
              handleSwap={function (card: CardData): void {
                onSwap(card);
              } } />
          ))}
        </div>
      </div>

    </div>
    
  );
};


const DraggableCard: React.FC<{
  card: CardData;
  onDrag: (card: CardData) => void;
  // handleClickCard: (card: CardData) => void;
  handleSwap: (card: CardData) => void;
}> = ({ card, onDrag, handleSwap }) => {
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
      style={{ opacity: isDragging ? 0.8 : 1}}
    >
      <div style={{width: "5px", height: "90%", backgroundColor: "red"}}>

      </div>
      
      <div className="card-image-container">
        <img className="card-image-drag" src={MyImage} alt="Player" />
      </div>

      <div className="draggable-card-name" style={{display: "flex",left: "0px"}}>
        
        <div style={{fontSize: "15px"}}>
          {card.name}
        </div>

        <div style={{fontSize: "10px", fontWeight: "100"}}>
          {card.type}
        </div>

      </div>

      <div style={{display: "flex", width: "48%", height: "100%", backgroundColor: "black", justifyContent: "space-around"}}>
        <div style={{width: "33%", alignContent:"center", color: "red", fontSize: "20px", fontWeight: "15px"}}>
          {card.points}
        </div>

        <div style={{width: "33%", alignContent:"center", color: "white", fontSize: "20px", fontWeight: "15px"}}>
          {card.cost}
        </div>

        <IconButton onClick={() => {}} style={{width: "33%"}}>
          <AddCircleOutline style={{color: "red"}}/>
        </IconButton>

        {/* <button className="add-button" onClick={() => {}}>
            +
          </button> */}
      </div>

      
    </div>
  );
};

export default DragZone;
