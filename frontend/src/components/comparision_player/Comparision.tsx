import React, { useState } from "react";
import playerImg from "../../assets/images/virat_kohli.png";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

interface Player {
  id: number;
  name: string;
  role: string;
  imageUrl: string;
  stats: {
    runs: number;
    strikeRate: number;
    boundaries: number;
    wickets: number;
    economy: number;
    catches: number;
    runOuts: number;
    form: number;
    matchup: number; // Added for radar comparison
    fielding: number; // Added for radar comparison
    average: number; // Added for radar comparison
  };
}

const players: Player[] = [
  {
    id: 1,
    name: "Virat Kohli sadsdg",
    role: "Batsman",
    imageUrl: playerImg,
    stats: {
      runs: 49,
      strikeRate: 20,
      boundaries: 12,
      wickets: 2,
      economy: 12,
      catches: 2,
      runOuts: 1,
      form: 92,
      matchup: 90,
      fielding: 80,
      average: 50,
    },
  },
  {
    id: 2,
    name: "MS Dhoni sdasfddsfds",
    role: "Batsman",
    imageUrl: playerImg,
    stats: {
      runs: 6300,
      strikeRate: 15,
      boundaries: 15,
      wickets: 5,
      economy: 18,
      catches: 1,
      runOuts: 1,
      form: 73,
      matchup: 85,
      fielding: 85,
      average: 48,
    },
  },
];

const CustomDropdown: React.FC<{
  options: Player[];
  selected: Player;
  onSelect: (player: Player) => void;
  card: string;
}> = ({ options, selected, onSelect, card }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleSelect = (player: Player) => {
    onSelect(player);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex flex-col gap-2 items-center py-2 bg-black font-bold uppercase text-white w-full text-left"
      >
        <div className="flex gap-2">
          <span>{isOpen ? "▲" : "▼"}</span>
          <div
            className={`flex flex-col ${card === "right" ? "items-end" : ""}`}
          >
            <div>{selected.name}</div>
            <div>{selected.role}</div>
          </div>
        </div>
      </button>

      {isOpen && (
        <div className="absolute left-0 w-full bg-black shadow-lg z-10">
          {[
            selected,
            ...options.filter((player) => player.id !== selected.id),
          ].map((player) => (
            <div
              key={player.id}
              onClick={() => handleSelect(player)}
              className={`px-4 py-2 cursor-pointer hover:bg-gray-800 text-white ${
                player.id === selected.id ? "bg-gray-500" : ""
              }`}
            >
              {player.name}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const StatRow: React.FC<{
  label: string;
  leftValue: number;
  rightValue: number;
}> = ({ label, leftValue, rightValue }) => {
  const barWidthScale = 100;

  const leftWidth = (leftValue / (leftValue + rightValue)) * barWidthScale;
  const rightWidth = (rightValue / (leftValue + rightValue)) * barWidthScale;

  return (
    <div className="flex items-center justify-between w-full py-1">
      <span className="w-12 text-left text-[#FA2433] font-semibold">
        {leftValue}
      </span>

      <div className="w-[160px] h-3 relative mx-2">
        <div
          className="h-full bg-[#FA2433] absolute right-0"
          style={{
            width: `${leftWidth}%`,
            borderTopLeftRadius: "10px", // Rounded corners only on the left side
            borderBottomLeftRadius: "10px",
          }}
        />
      </div>

      <span className="w-32 text-center text-white font-semibold uppercase">
        {label}
      </span>

      <div className="w-[160px] h-3 relative mx-2">
        <div
          className="h-full bg-[#8B24FA] absolute left-0"
          style={{
            width: `${rightWidth}%`,
            borderTopRightRadius: "10px", // Rounded corners only on the right side
            borderBottomRightRadius: "10px",
          }}
        />
      </div>

      <span className="w-12 text-right text-[#8B24FA] font-semibold">
        {rightValue}
      </span>
    </div>
  );
};

const Comparision: React.FC = () => {
  const [leftPlayer, setLeftPlayer] = useState<Player>(players[0]);
  const [rightPlayer, setRightPlayer] = useState<Player>(players[1]);

  const filteredLeftPlayers = players.filter(
    (player) => player.id !== rightPlayer.id
  );
  const filteredRightPlayers = players.filter(
    (player) => player.id !== leftPlayer.id
  );

  const chartOptions: ApexOptions = {
    chart: {
      type: "radar",
      toolbar: {
        show: false,
      },
    },
    xaxis: {
      categories: [
        "STRIKE RATE",
        "WICKETS",
        "ECONOMY",
        "MATCHUP",
        "FIELDING",
        "AVERAGE",
      ],
      labels: {
        style: {
          colors: ["white", "white", "white", "white", "white", "white"],
          fontSize: "12px",
          fontWeight: "bold",
        },
      },
    },
    plotOptions: {
      radar: {
        size: 110,
        polygons: {
          strokeColors: "#e9e9e9",
          connectorColors: "#e9e9e9",
          strokeWidth: "0.3px",
        },
      },
    },
    markers: {
      size: 8,
      colors: ["#FA2433", "#8B24FA"],
      strokeColors: "white",
      strokeWidth: 1,
      fillOpacity: 1,
    },
    fill: {
      opacity: 0.5,
      colors: ["#8E1F26", "#1F218E"],
    },
    tooltip: {
      enabled: true,
    },
    dataLabels: {
      enabled: false,
    },
    yaxis: {
      show: false,
    },
    legend: {
      show: false,
    },
  };

  const chartSeries = [
    {
      name: leftPlayer.name,
      data: [
        leftPlayer.stats.strikeRate,
        leftPlayer.stats.wickets,
        leftPlayer.stats.economy,
        leftPlayer.stats.matchup,
        leftPlayer.stats.fielding,
        leftPlayer.stats.average,
      ], // Use only the first 6 stats for the radar chart
    },
    {
      name: rightPlayer.name,
      data: [
        rightPlayer.stats.strikeRate,
        rightPlayer.stats.wickets,
        rightPlayer.stats.economy,
        rightPlayer.stats.matchup,
        rightPlayer.stats.fielding,
        rightPlayer.stats.average,
      ], // Use only the first 6 stats for the radar chart
    },
  ];

  return (
    <div className="flex items-center justify-center h-full p-4">
      <div className="min-h-[80%] w-full bg-[#1A1A1A] rounded-3xl p-3 flex flex-col">
        <div className="flex w-full bg-black px-2">
          {/* Left Card */}
          <div className="flex-1 flex items-center py-2 justify-between">
            <div className="flex items-center h-full">
              <div className="h-full w-6 bg-red-600"></div>
              {/* Increased the width of the gap container */}
              <div className="w-6"></div>
              <img
                src={leftPlayer.imageUrl}
                alt={leftPlayer.name}
                className="w-24 h-24"
              />
            </div>
            <div className="flex h-full justify-center items-end flex-col text-white w-full  pr-4">
              <CustomDropdown
                options={filteredLeftPlayers}
                card="left"
                selected={leftPlayer}
                onSelect={setLeftPlayer}
              />
              {/* <div className="font-semibold uppercase">{leftPlayer.role}</div> */}
            </div>
          </div>

          {/* Center Red Line */}
          <div className="w-4 bg-red-600"></div>

          {/* Right Card (Reversed Order) */}
          <div className="flex-1 flex items-center py-2 justify-between ">
            <div className="flex h-full justify-center items-start flex-col text-white w-full pl-4">
              <CustomDropdown
                options={filteredRightPlayers}
                selected={rightPlayer}
                card="right"
                onSelect={setRightPlayer}
              />
              {/* <div className="font-semibold uppercase">{rightPlayer.role}</div> */}
            </div>
            <div className="flex items-center h-full">
              <img
                src={rightPlayer.imageUrl}
                alt={rightPlayer.name}
                className="w-24 h-24"
              />
              {/* Increased the width of the gap container */}
              <div className="w-6"></div>
              <div className="h-full w-6 bg-red-600"></div>
            </div>
          </div>
        </div>

        {/* Separator with "COMPARISON" */}
        <div className="flex items-center justify-center w-full my-1">
          <div className="flex-1 h-[1px] bg-white"></div>
          <span className="px-4 text-white text-semibold text-2xl">
            COMPARISON
          </span>
          <div className="flex-1 h-[1px] bg-white"></div>
        </div>

        {/* Radar Chart */}
        <div className="w-full ">
          <ReactApexChart
            options={chartOptions}
            series={chartSeries}
            type="radar"
            height={280}
            width="100%"
          />
        </div>

        {/* Separator with "STATISTICS" */}
        <div className="flex items-center justify-center w-full">
          <div className="flex-1 h-[1px] bg-white"></div>
          <span className="px-4 text-white text-semibold text-2xl">
            STATISTICS
          </span>
          <div className="flex-1 h-[1px] bg-white"></div>
        </div>

        <div className="flex flex-col  px-8">
          <StatRow
            label="Runs"
            leftValue={leftPlayer.stats.runs}
            rightValue={rightPlayer.stats.runs}
          />
          <StatRow
            label="Strike Rate"
            leftValue={leftPlayer.stats.strikeRate}
            rightValue={rightPlayer.stats.strikeRate}
          />
          <StatRow
            label="Boundaries"
            leftValue={leftPlayer.stats.boundaries}
            rightValue={rightPlayer.stats.boundaries}
          />
          <StatRow
            label="Wickets"
            leftValue={leftPlayer.stats.wickets}
            rightValue={rightPlayer.stats.wickets}
          />
          <StatRow
            label="Economy"
            leftValue={leftPlayer.stats.economy}
            rightValue={rightPlayer.stats.economy}
          />
          <StatRow
            label="Catches"
            leftValue={leftPlayer.stats.catches}
            rightValue={rightPlayer.stats.catches}
          />
          <StatRow
            label="Run Outs"
            leftValue={leftPlayer.stats.runOuts}
            rightValue={rightPlayer.stats.runOuts}
          />
          <StatRow
            label="Form"
            leftValue={leftPlayer.stats.form}
            rightValue={rightPlayer.stats.form}
          />
        </div>
      </div>
    </div>
  );
};

export default Comparision;