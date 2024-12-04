// SlidingPanels.jsx
import React, { useState } from "react";
import Comparision from "./components/comparision_player/Comparision";
import TeamPage from "./pages/teamPage/teamPage";
import EditComponent from "./pages/teamPage/EditComponent";
import usePlayerStore from "./store/playerStore";
import Navbar from "./components/navbar/navbar";

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

export interface CardData {
  id: string;
  name: string;
  type: string;
  team: string;
  points: string;
  cost: string;
  score: string;
  cvc: string;
  runs: string;
  average: string;
  strike_rate: string;
  country: string;
}

const SlidingPanels = () => {


  const [isOpen, setIsOpen] = useState(false);
  // const { best11Players, playerStats } = usePlayerStore();

  //   from teamPage.tsx
  const initialDropZoneCards: CardData[] = [
    {
      id: "1",
      name: "FAF DU PLESSIS",
      type: "BAT",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "VC",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "2",
      name: "VIRAT KOHLI",
      type: "BAT",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "C",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "3",
      name: "GLENN MAXWELL",
      type: "ALL",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "4",
      name: "DINESH KARTHIK",
      type: "WK",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "5",
      name: "MOHAMMED SIRAJ",
      type: "BOWL",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "6",
      name: "WILL JACKS",
      type: "ALL",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "7",
      name: "MAHIPAL LOMROR",
      type: "ALL",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "8",
      name: "REECE TOPLEY",
      type: "BOWL",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "9",
      name: "RAJAT PATIDAR",
      type: "BAT",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "10",
      name: "ANUJ RAWAT",
      type: "WK",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "11",
      name: "ALZARRI JOSEPH",
      type: "BOWL",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
  ];

  const initialDragZoneCards: CardData[] = [
    {
      id: "12",
      name: "ROHIT SHARMA",
      type: "BATSMAN",
      team: "MI",
      points: "207",
      cost: "10",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "13",
      name: "SURYAKUMAR YADAV",
      type: "BATSMAN",
      team: "MI",
      points: "206",
      cost: "4.5",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "14",
      name: "HARDIK PANDYA",
      type: "ALL-ROUNDER",
      team: "MI",
      points: "204",
      cost: "15",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "15",
      name: "TIM DAVID",
      type: "BATSMAN",
      team: "MI",
      points: "217",
      cost: "27",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "16",
      name: "ISHAN KISHAN",
      type: "WICKETKEEPER-BATSMAN",
      team: "MI",
      points: "210",
      cost: "27.65",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "17",
      name: "JASPRIT BUMRAH",
      type: "BOWLER",
      team: "MI",
      points: "300",
      cost: "11",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "18",
      name: "NEHAL WADHERA",
      type: "BATSMAN",
      team: "MI",
      points: "200",
      cost: "2",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "19",
      name: "TILAK VARMA",
      type: "ALL-ROUNDER",
      team: "MI",
      points: "213",
      cost: "20",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "20",
      name: "AKASH MADHWAL",
      type: "BOWLER",
      team: "MI",
      points: "247",
      cost: "22",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "21",
      name: "KUMAR KARTIKEYA",
      type: "BOWLER",
      team: "MI",
      points: "256",
      cost: "3.8",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
    {
      id: "22",
      name: "PIYUSH CHAWLA",
      type: "BOWLER",
      team: "MI",
      points: "267",
      cost: "7",
      score: "89",
      cvc: "",
      runs: "",
      average: "",
      strike_rate: "",
      country: "",
    },
  ];

  const [dropZoneCards, setDropZoneCards] =
    useState<CardData[]>(initialDropZoneCards);

  const [dragZoneCards, setDragZoneCards] =
    useState<CardData[]>(initialDragZoneCards);

  const [filterType, setFilterType] = useState<"points" | "cost">("points");

  // selected card
  const [selectedCard, setSelectedCard] = useState<CardData | null>(null);

  const applyFilter = (filter: "points" | "cost") => {
    setFilterType(filter);
  };

  // const moveToDropZone = (card: CardData) => {
  //   if (dropZoneCards.length >= 11) {
  //     // If DropZone is full, swap the last card back to DragZone
  //     const cardToSwap = dropZoneCards[dropZoneCards.length - 1]; // Get the last card
  //     // const cardToSwap = selectedCard;
  //     const updatedDropZone = [...dropZoneCards.slice(0, -1), card]; // Replace last card with new card

  //     setDropZoneCards(updatedDropZone);
  //     setDragZoneCards([
  //       ...dragZoneCards.filter((c) => c.id !== card.id),
  //       cardToSwap,
  //     ]);
  //   } else {
  //     // If DropZone is not full, simply add the card
  //     setDropZoneCards([...dropZoneCards, card]);
  //     setDragZoneCards(dragZoneCards.filter((c) => c.id !== card.id));
  //   }
  // };

  const removeFromDropZone = (card: CardData) => {
    // Remove the card from the DropZone
    const updatedDropZone = dropZoneCards.filter((c) => c.id !== card.id);

    // Reset the removed card's CVC value if it's Captain or Vice-Captain
    if (card.cvc === "C" || card.cvc === "VC") {
      // card.cvc = "";

      // Assign new Captain or Vice-Captain if the removed card was one
      if (updatedDropZone.length >= 3) {
        const thirdCard = updatedDropZone[4];
        thirdCard.cvc = card.cvc === "C" ? "C" : "VC";
      }
      card.cvc = "";
    }

    // Update the state
    setDropZoneCards(updatedDropZone);
    // setDropZoneCards(dropZoneCards.filter((c) => c.id !== card.id));
    setDragZoneCards([...dragZoneCards, card]);
    setSelectedCard(null);
  };

  const [showContainer, setShowContainer] = useState(false);

  // handle selected card
  const handleSelectCard = (card: CardData) => {
    setSelectedCard(card);
  };

  // handle swap cards
  // const handleSwapCards = (card: CardData) => {
  //   if (selectedCard !== null) {
  //     const updatedDropZone = dropZoneCards.map((c) =>
  //       c.id === selectedCard.id ? card : c
  //     );
  //     const updatedDragZone = dragZoneCards.map((c) =>
  //       c.id === card.id ? selectedCard : c
  //     );
  //     setDropZoneCards(updatedDropZone);
  //     setDragZoneCards(updatedDragZone);
  //     setSelectedCard(null);
  //   } else {
  //     setSelectedCard(null);
  //   }

  //   setSelectedCard(null);
  // };


  const handleSwapCards = (card: CardData) => {
    if (selectedCard !== null) {
      const updatedDropZone = dropZoneCards.map((c) => {
        // Replace the selected card in the drop zone with the incoming card
        if (c.id === selectedCard.id) {
          // If the selected card was a captain or vice-captain, remove its cvc
          return { ...card, cvc: "" };
        }
        return c;
      });
  
      const updatedDragZone = dragZoneCards.map((c) => {
        // Replace the dragged card in the drag zone with the selected card
        if (c.id === card.id) {
          // If the dragged card was a captain or vice-captain, reset its cvc
          return { ...selectedCard, cvc: selectedCard.cvc === "C" || selectedCard.cvc === "VC" ? "" : selectedCard.cvc };
        }
        return c;
      });
  
      setDropZoneCards(updatedDropZone);
      setDragZoneCards(updatedDragZone);
      setSelectedCard(null);
    } else {
      setSelectedCard(null);
    }
  };
  
  

  const toggleContainer = () => {
    setShowContainer((prev) => !prev);
  };

  const handleSetCVC = (id: string, role: "C" | "VC") => {
    setDropZoneCards((prevCards) =>
      prevCards.map((card) => {
        if (card.id === id) {
          // Set the new Captain or Vice-Captain
          return { ...card, cvc: role };
        }

        // If we are swapping roles, we check if the other card is a Vice-Captain or Captain
        if (
          (role === "C" && card.cvc === "VC") || // If the role is being set to "C", and the card is currently "VC"
          (role === "VC" && card.cvc === "C") // If the role is being set to "VC", and the card is currently "C"
        ) {
          // Swap the roles
          return { ...card, cvc: role === "C" ? "VC" : "C" }; // Set the swapped role
        }

        // Reset the previously selected Captain or Vice-Captain
        if (
          (role === "C" && card.cvc === "C") ||
          (role === "VC" && card.cvc === "VC")
        ) {
          return { ...card, cvc: "" };
        }

        return card;
      })
    );
  };

  const addToDropZone = (card: CardData) => {
    if (dropZoneCards.length < 11) {
      setDropZoneCards([...dropZoneCards, card]);
      setDragZoneCards(dragZoneCards.filter((c) => c.id !== card.id));
    } else {
      alert("Dream team is already full!");
    }
  };

  return (
        <div className="relative w-full h-screen overflow-hidden">
        {/* Button with higher z-index and clear positioning */}
        {showContainer && (
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="fixed left-0 top-1/2 transform -translate-y-1/2 z-50 px-1 py-3 bg-[#88000A] 
          text-white rounded-l-3xl shadow-lg transition-colors duration-200 -rotate-180 uppercase
          font-semibold text-lg"
            style={{ writingMode: "vertical-rl" }}
          >
            {isOpen ? "^" : "compare players"}
          </button>
        )}

        <div className="flex h-full">
          <div
            className={`fixed top-0 w-[45%] h-full bg-black-100 shadow-lg transition-transform 
            duration-500 ease-in-out  ${
              isOpen ? "translate-x-0" : "-translate-x-full"
            }`}
          >
            <Comparision />
          </div>  
  
          <div
            className={`fixed top-0 h-full bg-white transition-transform duration-500 
            ease-in-out ${
              isOpen ? "w-[55%] translate-x-[81.8%]" : "w-[60%] translate-x-0"
            }`}
          >
            {/* <div className="p-6">Component 2</div> */}
            <TeamPage
              showContainer={showContainer}
              toggleContainer={toggleContainer}
              dragZoneCards={dragZoneCards}
              filterType={filterType}
              applyFilter={applyFilter}
              handleSwapCards={handleSwapCards}
              selectedCard={selectedCard}
              dropZoneCards={dropZoneCards}
              removeFromDropZone={removeFromDropZone}
              handleSelectCard={handleSelectCard}
              handleSetCVC={handleSetCVC}
            />
          </div>
  
          <div
            className={`fixed right-0 w-[40%] h-full bg-black transition-transform 
            duration-500 ease-in-out ${
              isOpen ? "translate-x-full" : "translate-x-0"
            }`}
          >
            {/* <div className="p-6">Component 3</div> */}
            <EditComponent
              showContainer={showContainer}
              toggleContainer={toggleContainer}
              dragZoneCards={dragZoneCards}
              dropZoneCards={dropZoneCards}
              filterType={filterType}
              applyFilter={applyFilter}
              handleSwapCards={handleSwapCards}
              selectedCard={selectedCard}
              addToDropZone={addToDropZone}
            />
          </div>
        </div>
      </div>
    
  );
};

export default SlidingPanels;
