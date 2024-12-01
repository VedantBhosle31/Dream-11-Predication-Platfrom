import React, { useRef, useState } from "react";
import { useDrop } from "react-dnd";
import "./DropZone.css";
import MyImage from "../../assets/images/virat_kohli.png";
import milogo from "../../assets/images/mumbai_indians.png";
import rcblogo from "../../assets/images/rcb_logo.png";
import { IconButton } from "@mui/material";
import { AddCircleOutline, RemoveCircleOutline } from "@mui/icons-material";
import { CardData } from "../../SlidingPanels";
import DisplayCardExpanded from "../player_display_card/displayCardExpanded2";
import playerImage from "../../assets/images/virat_kohli.png"; // Replace with your player image
import { DisplayCardData } from "../../pages/player_display_card/displayCard";

interface DropZoneProps {
  cards: CardData[];
  onRemove: (card: CardData) => void;
  isedit: boolean;
  handleSelectCard: (card: CardData) => void;
  selectedCard: CardData | null;
  handleSetCVC: (id: string, role: "C" | "VC") => void;
}

const DropZone: React.FC<DropZoneProps> = ({
  cards,
  onRemove,
  isedit,
  handleSelectCard,
  selectedCard,
  handleSetCVC,
}) => {
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

  const allSlots = [
    ...sortedCards,
    ...Array.from({ length: totalSlots - sortedCards.length }, () => null),
  ];

  const row1 = allSlots.slice(0, 3); // First 3 cards
  const row2 = allSlots.slice(3, 7); // Next 4 cards
  const row3 = allSlots.slice(7, 11); // Last 4 cards

  return (
    <div ref={dropRef} className="dropzone-container">
      <div className="dropzone-row">
        {row1.map((card, index) =>
          card ? (
            <DroppableCard
              key={card.id || `placeholder-${index}`}
              card={card}
              onRemove={onRemove}
              isedit={isedit}
              onSelectCard={handleSelectCard}
              selectedCard={selectedCard}
              handleSetCVC={handleSetCVC}
            />
          ) : (
            <Placeholder key={`placeholder-${index}`} />
          )
        )}
      </div>
      <div className="dropzone-row">
        {row2.map((card, index) =>
          card ? (
            <DroppableCard
              key={card.id}
              card={card}
              onRemove={onRemove}
              isedit={isedit}
              onSelectCard={handleSelectCard}
              selectedCard={selectedCard}
              handleSetCVC={handleSetCVC}
            />
          ) : (
            <Placeholder key={`placeholder-${index}`} />
          )
        )}
      </div>
      <div className="dropzone-row">
        {row3.map((card, index) =>
          card ? (
            <DroppableCard
              key={card.id}
              card={card}
              onRemove={onRemove}
              isedit={isedit}
              onSelectCard={handleSelectCard}
              selectedCard={selectedCard}
              handleSetCVC={handleSetCVC}
            />
          ) : (
            <Placeholder key={`placeholder-${index}`} />
          )
        )}
      </div>
    </div>
  );
};

const DroppableCard: React.FC<{
  card: DisplayCardData;
  onRemove: (card: CardData) => void;
  onSelectCard: (card: CardData) => void;
  isedit: boolean;
  selectedCard: CardData | null;
  handleSetCVC: (id: string, role: "C" | "VC") => void;
}> = ({ card, onRemove, isedit, onSelectCard, selectedCard, handleSetCVC }) => {

  // const [ishovered, setShowButtons] = useState(false);
  var [isCardExpanded, setCardExpanded] = useState(false);

  const containerRef = useRef<HTMLDivElement | null>(null);



























  // var [isExpanded, setExpanded] = useState(false);
  const handleOpen = () => setCardExpanded(true);
  const handleClose = () => setCardExpanded(false);



  interface Stats {
    title: string;
    stats: Stat[];
  }



  interface Graphs {
    title: string;
    description: string;
  }

  // graphs
  
  const data: Graphs[] = [
    {
      title: "FANTASY POINTS VS MATCHES",
      description:
        "Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum",
    },
    {
      title: "RECENT PERFORMANCE",
      description:
        "Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum",
    },
    {
      title: "MATCHUPS",
      description:
        "Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum",
    },
    {
      title: "PLAYER DEMOGRAPHY",
      description:
        "Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum",
    },
    {
      title: "Differential Exp",
      description:
        "Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum",
    },
    // { title: 'Opposition Performance Index vs Number of Matches', stats: [{ key: 'P', value: '100' }, { key: 'Q', value: '200' }, { key: 'R', value: '300' }] },
    {
      title: "Impact Index",
      description:
        "Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum",
    },
  ];

  // batting , bowling AND fielder
  const typeData: Stats[] = [
    {
      title: "FANTASY POINTS VS MATCHES",
      stats: [
        { key: "INNINGS", value: "244" },
        { key: "AGGREGATE", value: "8004" },
        { key: "HIGHEST SCORE", value: "113" },
        { key: "AVERAGE", value: "38.67" },
        { key: "FIFTYS", value: "55" },
        { key: "HUNDREDS", value: "8" },
        { key: "DUCKS", value: "10" },
        { key: "FOURS", value: "705" },
        { key: "SIXES", value: "272" },
      ],
    },
    {
      title: "RECENT PERFORMANCE",
      stats: [
        { key: "X", value: "10" },
        { key: "Y", value: "20" },
        { key: "Z", value: "30" },
      ],
    },
    {
      title: "MATCHUPS",
      stats: [
        { key: "P", value: "100" },
        { key: "Q", value: "200" },
        { key: "R", value: "300" },
      ],
    },
    {
      title: "PLAYER DEMOGRAPHY",
      stats: [
        { key: "P", value: "100" },
        { key: "Q", value: "200" },
        { key: "R", value: "300" },
      ],
    },
    {
      title: "PLAYER DEMOGRAPHY",
      stats: [
        { key: "P", value: "100" },
        { key: "Q", value: "200" },
        { key: "R", value: "300" },
      ],
    },
  ];

  interface BattingProps {
    average: number;
    strikeRate: number;
    centuries: number;
    halfCenturies: number;
  }

  interface BowlingProps {
    average: number;
    economyRate: number;
    wickets: number;
    fiveWicketHauls: number;
  }

  interface FieldingProps {
    catches: number;
    runOuts: number;
    stumpings: number;
  }

  type Stat = {
    key: string;
    value: string;
  };

  type TypeData = {
    title: string;
    stats: Stat[];
  };

  const typesMap: { [key in "BATTING" | "BOWLING" | "FIELDING"]: TypeData } = {
    BATTING: {
      title: "BATTING",
      stats: [
        { key: "MATCHES", value: "8" },
        { key: "INNINGS", value: "50.0" },
        { key: "RUNS", value: "80%" },
        { key: "AVERAGE", value: "5" },
        { key: "STRIKE RATE", value: "8" },
        { key: "HIGHEST SCORE", value: "8" },
        { key: "4s/6s", value: "8" },
        { key: "50/100", value: "8" },
      ],
    },
    BOWLING: {
      title: "BOWLING",
      stats: [
        { key: "Average", value: "30.0" },
        { key: "Economy Rate", value: "5.5" },
        { key: "Wickets", value: "15" },
        { key: "Five Wicket Hauls", value: "2" },
      ],
    },
    FIELDING: {
      title: "FIELDING",
      stats: [
        { key: "Catches", value: "10" },
        { key: "Run Outs", value: "5" },
        { key: "Stumps", value: "3" },
      ],
    },
  };

  // Prepare data for the `typeData_2` prop
  const typeData_2 = Object.values(typesMap).map((type) => ({
    title: type.title,
    stats: type.stats,
  }));

  interface DisplayCardExpandedProps {
    typeData_2: TypeData[];
  }

  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentIndexTypes, setCurrentIndexTypes] = useState(0);

  const handleLeftClick = () => {
    setCurrentIndex((prev) => (prev === 0 ? data.length - 1 : prev - 1));
  };

  const handleRightClick = () => {
    setCurrentIndex((prev) => (prev === data.length - 1 ? 0 : prev + 1));
  };

  const handleLeftClickTypes = () => {
    setCurrentIndexTypes((prev) =>
      prev === 0 ? typeData_2.length - 1 : prev - 1
    );
  };

  const handleRightClickTypes = () => {
    setCurrentIndexTypes((prev) =>
      prev === typeData_2.length - 1 ? 0 : prev + 1
    );
  };

  const suggestions = [
    "ReactJS",
    "TypeScript",
    "React Native",
    "JavaScript",
    "Node.js",
  ];

  const handleSearch = (query: string) => {
    console.log("Search Query:", query);
    alert(`You searched for: ${query}`);
  };

  //for filterBar(All,T20I, T20)
  const [selectedFilter, setSelectedFilter] = useState("All"); // State for the selected filter
  const [selectedFilter2, setSelectedFilter2] = useState("Overall"); // State for the selected filter
  const [selectedFilter3, setSelectedFilter3] = useState("venue"); // State for the selected filter

  const filters = ["All", "T20I", "T20"]; // Filter options
  const filters2 = ["Overall", "Powerplay", "Middle", "Death"]; // Filter options
  const filters3 = ["venue", "opposition", "form"]; // Filter options

  const handleFilterChange = (filter: string) => {
    setSelectedFilter(filter); // Update the selected filter
  };
  const handleFilterChange2 = (filter: string) => {
    setSelectedFilter2(filter); // Update the selected filter
  };
  const handleFilterChange3 = (filter: string) => {
    setSelectedFilter3(filter); // Update the selected filter
  };

  interface somecarddata  {
    name: string;
    country: string;
    type: string;
    cvc: string;
  }





































  return !isCardExpanded ? (
    <div
      className="droppable-card"
      onClick={() => {}}
      style={{ border: selectedCard === card ? "2px solid white" : "none" }}
      onDropCapture={() => onSelectCard(card)}
    >
      <div className="left-half"></div>
      <div className="right-half"></div>

      <div className="droppable-card-points">
        <div>
          {card.points}
          <div style={{ fontSize: 6, color: "red" }}>PTS</div>
        </div>

        <img
          className="team-logo"
          src={card.team === "RCB" ? rcblogo : milogo}
          alt="Player"
        />
      </div>

      <div className="card-overlay">
        {card.name}
        <div className="card-overlay-row">
          <div style={{ fontSize: "9px", display: "flex" }}>
            {card.score}
            <div style={{ color: "red" }}>RNS</div>
          </div>
          <div style={{ fontSize: "9px", fontWeight: 900 }}>{card.type}</div>
          <div style={{ fontSize: "9px", fontWeight: 900, display: "flex" }}>
            {card.cost}
            <div style={{ color: "red" }}>CR</div>
          </div>
        </div>
      </div>

      {(card.cvc === "C" && 
        <div className="absolute text-white w-10 h-10 px-2 py-2 font-bold" style={{backgroundColor: "rgb(235, 134, 2)", fontFamily:"Montserrat"}}>
          C
        </div>)}

        {(card.cvc === "VC" && 
        <div className="absolute text-white bg-black w-10 h-10 px-2 py-2 font-bold" style={{backgroundColor: "rgb(2, 157, 235)", fontFamily:"Montserrat"}}>
          VC
        </div>)}

      {isedit && (
        <button className="remove-button" onClick={() => onRemove(card)}>
          <RemoveCircleOutline style={{ width: "13px", height: "13px" }} />
        </button>
        //   <button className="remove-button" onClick={() => onSelectCard(card)} onDoubleClick={() => onRemove(card)}>
        //   <RemoveCircleOutline style={{ width: "13px", height: "13px",}}/>
        //  </button>
      )}

      {isedit && (<div className="absolute inset-0 bg-black bg-opacity-60 flex flex-col items-center justify-center opacity-0 hover:opacity-100 transition-opacity z-10 text-xs">
        <button
          onClick={() => handleSetCVC(card.id, "C")}
          className=" py-1 px-3 rounded-lg mb-2 transition h-8 w-[%70]"
          style={{backgroundColor: "rgb(235, 134, 2)", fontFamily:"Montserrat", fontSize:"70%"}}
        >
          Make Captain
        </button>

        <button
          onClick={() => handleSetCVC(card.id, "VC")}
          className=" py-1 px-3 rounded-lg mb-2 transition h-8 w-[%70]"
          style={{backgroundColor: "rgb(2, 157, 235)", fontFamily:"Montserrat", fontSize:"70%"}}
        >
          Make Vice-Captain
        </button>

        <button
          onClick={() => setCardExpanded(true)}
          className=" py-1 px-3 rounded-lg mb-2 transition h-8 w-[%70]"
          style={{backgroundColor: "rgb(235, 134, 2)", fontFamily:"Montserrat", fontSize:"70%"}}
        >
          Show Info
        </button>
      </div>)}

      <img className="card-image" src={MyImage} alt="Player" />
    </div>
  ) :(
    // <div></div>
    <DisplayCardExpanded
      containerRef={containerRef}
      isExpanded={isCardExpanded}
      setExpanded={setCardExpanded}
      playerImage={playerImage}
      card={card}
      handleLeftClick={handleLeftClick}
      handleRightClick={handleRightClick}
      handleLeftClickTypes={handleLeftClickTypes}
      handleRightClickTypes={handleRightClickTypes}
      data={data}
      typeData={typeData}
      typeData_2={typeData_2}
      currentIndex={currentIndex}
      currentIndexTypes={currentIndexTypes}
      suggestions={suggestions}
      handleSearch={handleSearch}
      handleClose={handleClose}
      open={isCardExpanded}
      selectedFilter={selectedFilter}
      selectedFilter2={selectedFilter2}
      selectedFilter3={selectedFilter3}
      filters={filters}
      filters2={filters2}
      filters3={filters3}
      handleFilterChange={handleFilterChange}
      handleFilterChange2={handleFilterChange2}
      handleFilterChange3={handleFilterChange3}
    />
  )
  ;
};

const Placeholder: React.FC = () => {
  return (
    <div className="placeholder-card">
      <div className="placeholder-border">
        <IconButton onClick={() => {}}>
          <AddCircleOutline
            style={{
              color: "gray",
              opacity: "0.4",
              width: "50%",
              height: "50%",
            }}
          />
        </IconButton>
      </div>
    </div>
  );
};

export default DropZone;
