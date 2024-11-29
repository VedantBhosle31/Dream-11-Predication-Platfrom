// SlidingPanels.jsx
import React, { useState } from "react";
import Comparision from "./components/comparision_player/Comparision";
import TeamPage from "./pages/teamPage/teamPage";
import EditComponent from "./pages/teamPage/EditComponent";

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

const SlidingPanels = () => {
  const [isOpen, setIsOpen] = useState(false);

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
    },
    // { id: "11", name: "ALZARRI JOSEPH", type: "BOWL", team: "RCB", points: "207", cost: "12", score: "89" }
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

  const moveToDropZone = (card: CardData) => {
    if (dropZoneCards.length >= 11) {
      // If DropZone is full, swap the last card back to DragZone
      const cardToSwap = dropZoneCards[dropZoneCards.length - 1]; // Get the last card
      // const cardToSwap = selectedCard;
      const updatedDropZone = [...dropZoneCards.slice(0, -1), card]; // Replace last card with new card

      setDropZoneCards(updatedDropZone);
      setDragZoneCards([
        ...dragZoneCards.filter((c) => c.id !== card.id),
        cardToSwap,
      ]);
    } else {
      // If DropZone is not full, simply add the card
      setDropZoneCards([...dropZoneCards, card]);
      setDragZoneCards(dragZoneCards.filter((c) => c.id !== card.id));
    }
  };

  const removeFromDropZone = (card: CardData) => {
    setDropZoneCards(dropZoneCards.filter((c) => c.id !== card.id));
    setDragZoneCards([...dragZoneCards, card]);
    setSelectedCard(null);
  };

  const [showContainer, setShowContainer] = useState(false);

  // handle selected card
  const handleSelectCard = (card: CardData) => {
    setSelectedCard(card);
  };

  // handle swap cards
  const handleSwapCards = (card: CardData) => {
    if (selectedCard !== null) {
      const updatedDropZone = dropZoneCards.map((c) =>
        c.id === selectedCard.id ? card : c
      );
      const updatedDragZone = dragZoneCards.map((c) =>
        c.id === card.id ? selectedCard : c
      );
      setDropZoneCards(updatedDropZone);
      setDragZoneCards(updatedDragZone);
      setSelectedCard(null);
    } else {
      setSelectedCard(null);
    }
    setSelectedCard(null);
  };

  const toggleContainer = () => {
    setShowContainer((prev) => !prev);
  };

  return (
    <div className="relative w-full h-screen overflow-hidden">
      {/* Button with higher z-index and clear positioning */}
      { showContainer && <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed -left-4 top-1/2 transform -translate-y-1/2 z-50 px-2 bg-[#88000A] 
        text-white rounded-lg shadow-lg transition-colors duration-200  -rotate-90 uppercase
        font-semibold text-lg"
      >
        {isOpen ? "<" : "compare players"}
      </button>}

      <div className="flex h-full">
        <div
          className={`fixed top-0 w-[45%] h-full bg-black-100 shadow-lg transition-transform 
          duration-500 ease-in-out  ${
            isOpen ? "translate-x-20" : "-translate-x-full"
          }`}
        >
          <Comparision />
        </div>

        <div
          className={`fixed top-0 h-full bg-black-200 transition-transform duration-500 
          ease-in-out ${
            isOpen ? "w-[58%] translate-x-[81.8%]" : "w-[58%] translate-x-0"
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
          />
        </div>

        <div
          className={`fixed right-0 w-[50%] h-full bg-black transition-transform 
          duration-500 ease-in-out ${
            isOpen ? "translate-x-full" : "translate-x-0"
          }`}
        >
          {/* <div className="p-6">Component 3</div> */}
          <EditComponent
            showContainer={showContainer}
            toggleContainer={toggleContainer}
            dragZoneCards={dragZoneCards}
            filterType={filterType}
            applyFilter={applyFilter}
            handleSwapCards={handleSwapCards}
            selectedCard={selectedCard}
          />
        </div>
      </div>
    </div>
  );
};

export default SlidingPanels;
