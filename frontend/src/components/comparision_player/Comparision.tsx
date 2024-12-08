import React, { useEffect, useState } from "react";
import playerImg from "../../assets/images/virat_kohli.png";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import "./Comparison.css";
import usePlayerStore from "../../store/playerStore";
import defaultimg from "../../assets/images/default.png";

export interface Player {
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
    matchup: number;
    fielding: number; // Added for radar comparison
    average: number; // Added for radar comparison
  };
}


const CustomDropdown: React.FC<{
  options: any[];
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
        className="flex flex-col gap-2 items-center py-2 bg-black font-semibold uppercase text-xs text-white w-full h-[90%] text-left"
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
        <div className="absolute left-0 w-full bg-black shadow-lg z-10 max-h-48 overflow-y-scroll overflow-x-hidden">
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

      <div className="w-[160px] h-2 relative mx-2">
        <div
          className="h-full bg-[#FA2433] absolute right-0"
          style={{
            width: `${leftWidth}%`,
            borderTopLeftRadius: "10px", // Rounded corners only on the left side
            borderBottomLeftRadius: "10px",
          }}
        />
      </div>

      <span className="w-32 text-center text-xs text-white font-semibold uppercase">
        {label}
      </span>

      <div className="w-[160px] h-2 relative mx-2">
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

const fetchPlayerData = async (
  name: string,
  model: string,
  matchDate: string
) => {
  const response = await fetch(
    `${process.env.REACT_APP_BACKEND_URL}/players/get-player-data`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Tell the server it's JSON
      },
      body: JSON.stringify({
        name: name,
        model: model,
        date: matchDate,
      }), // Send required data
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch data for ${name}: ${response.statusText}`);
  }

  return await response.json();
};

const Comparision: React.FC = () => {
  const { playerStats } = usePlayerStore();
  const { model } = usePlayerStore();
  const { matchDate } = usePlayerStore();

  const [playersData, setPlayersData] = useState<{ [key: string]: any }>({});

  useEffect(() => {
    const fetchDataForAllPlayers = async () => {
      const playerNames = Object.keys(playerStats); // Get player names from playerStats

      try {
        
        const results = await Promise.all(
          playerNames.map((playerName) =>
            fetchPlayerData(playerName, model, matchDate)
              .then((data) => ({ name: playerName, data }))
              .catch((error) => {
                console.error(error);
                return { name: playerName, data: null };
              })
          )
        );

        
        const playersMap = results.reduce(
          (acc, { name, data }) => ({ ...acc, [name]: data }),
          {}
        );

        console.log("playersMap", playersMap);

        setPlayersData(playersMap); // Update state with the fetched data
      } catch (error) {
        console.error("Error fetching player data:", error);
      }
    };

    fetchDataForAllPlayers();
  }, [playerStats, model, matchDate]);

  const extractComparisonPlayers = (): Player[] => {
    const playersStats = Object.keys(playerStats);

    console.log("asdhuio",playerStats);

    return playersStats?.map((playerName: any, index: number) => {
      const playerStatsData: any = playerStats[playerName] || [];

      const fetchedData: any = playersData[playerName] || [];

      const espnId = playerStatsData.player_id2 || "";

      console.log("wguiehfjierbgn",fetchedData["stats"]);

      return {
        id: index, // Unique ID for remaining players
        name: playerName,
        role: playerStatsData.position || "N/A",
        imageUrl: espnId
          ? `https://a.espncdn.com/i/headshots/cricket/players/full/${espnId}.png`
          : "",
        stats: {
          runs:
            parseFloat(Math.abs(parseFloat(playerStatsData.runs)).toFixed(2)) ||
            0,
          strikeRate:
            parseFloat(
              Math.abs(parseFloat(playerStatsData.strike_rate)).toFixed(2)
            ) || 0.0,
          boundaries: parseFloat(
            Math.abs(
              parseFloat(playerStatsData["4s"]) +
                parseFloat(playerStatsData["6s"])
            ).toFixed(2)
          ),
          wickets:
            parseFloat(
              Math.abs(parseFloat(playerStatsData.wickets)).toFixed(2)
            ) || 0,
          economy:
            parseFloat(
              Math.abs(parseFloat(playerStatsData.economy)).toFixed(2)
            ) || 0,
          catches:
            parseFloat(
              Math.abs(parseFloat(playerStatsData.catches)).toFixed(2)
            ) || 0,
          runOuts:
            parseFloat(
              Math.abs(parseFloat(playerStatsData.runouts)).toFixed(2)
            ) || 0,


          

          form:0,
            // fetchedData.length !== 0 &&
            // fetchedData["stats"]["batting"].length > 0 &&
            // fetchedData["stats"]["batting"][0]["form"] === 0
            //   ? fetchedData["stats"]["bowling"][0].length > 0
            //     ? fetchedData["stats"]["bowling"][0]["form"] * 10
            //     : 0
            //   : fetchedData["stats"]["batting"].length > 0
            //   ? fetchedData["stats"]["batting"][0]["form"] * 10
            //   : 0,

          matchup:
            fetchedData.length !== 0
              ? fetchedData["stats"]["batting"].length !== 0
                ? fetchedData["stats"]["batting"][0]["opposition"] * 10
                : 0
              : 0,
          fielding:
            fetchedData.length !== 0
              ? fetchedData["stats"]["fielding"].length !== 0
                ? fetchedData["stats"]["fielding"][0]["pfa_catches"] * 10
                : 0
              : 0,
          average:
            fetchedData.length !== 0 ? (fetchedData["stats"]["batting"].length !== 0 ? fetchedData["stats"]["batting"][0]["previous_average"]: 0): 0,
        },
      };
    });
  };

  const ComparisonPlayers = extractComparisonPlayers();

  const [leftPlayer, setLeftPlayer] = useState<Player>(ComparisonPlayers[0]);
  const [rightPlayer, setRightPlayer] = useState<Player>(ComparisonPlayers[1]);

  const filteredLeftPlayers = ComparisonPlayers.filter(
    (player) => player.id !== rightPlayer.id
  );
  const filteredRightPlayers = ComparisonPlayers.filter(
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
    <div className="comparison-section">
      <div className="comparison-wrapper">
        <div className="row1">
          <div className="selector-container">
            <div className="selector-wrapper">
              <div className="compare-title">COMPARE PLAYERS</div>
              {/* Left Card */}
              <div className="selector-top">
                <div className="sel-col-1">
                  <div className="h-full w-[1vh] bg-red-600"></div>
                  {/* Increased the width of the gap container */}

                  <img
                    src={leftPlayer.imageUrl}
                    alt={leftPlayer.name}
                    onError={(e) => {
                      e.currentTarget.src = defaultimg;
                    }}
                    className="h-full w-[90%]"
                  />
                </div>
                <div className="flex h-full justify-center items-end flex-col text-white w-full">
                  <CustomDropdown
                    options={filteredLeftPlayers}
                    card="left"
                    selected={leftPlayer}
                    onSelect={setLeftPlayer}
                  />
                  {/* <div className="font-semibold uppercase">{leftPlayer.role}</div> */}
                </div>
              </div>

              {/* Right Card (Reversed Order) */}
              <div className="selector-bottom">
                <div className="sel-col-1">
                  <div className="h-full w-[1vh] bg-[#8B24FA]"></div>
                  <img
                    src={rightPlayer.imageUrl}
                    alt={rightPlayer.name}
                    onError={(e) => {
                      e.currentTarget.src = defaultimg;
                    }}
                    className="h-full w-[90%]"
                  />
                </div>
                {/* Increased the width of the gap container */}
                <div className="flex h-full justify-center items-end flex-col text-white w-full">
                  <CustomDropdown
                    options={filteredRightPlayers}
                    selected={rightPlayer}
                    card="right"
                    onSelect={setRightPlayer}
                  />
                  {/* <div className="font-semibold uppercase">{rightPlayer.role}</div> */}
                </div>
              </div>
            </div>
          </div>

          {/* Radar Chart */}
          <div className="radar-container">
            <ReactApexChart
              options={chartOptions}
              series={chartSeries}
              type="radar"
              height="100%"
            />
          </div>
        </div>

        <div className="row2">
          <div className="flex items-center justify-center w-full">
            <div className="flex-1 h-[0.3vh] bg-[#363636] ml-[2vh]"></div>
            <span className="stats-title">STATISTICS</span>
            <div className="flex-1 h-[0.3vh] bg-[#363636] mr-[2vh]"></div>
          </div>

          <div className="flex flex-col px-8">
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
            {/* <StatRow
              label="Form"
              leftValue={leftPlayer.stats.form}
              rightValue={rightPlayer.stats.form}
            /> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Comparision;
