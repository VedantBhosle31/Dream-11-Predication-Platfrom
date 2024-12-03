import React, { useState, useRef, useEffect } from "react";
import playerImage from "../../assets/images/virat_kohli.png"; // Replace with your player image
import milogo from "../../assets/images/mumbai_indians.png";
import rcblogo from "../../assets/images/rcb_logo.png";
import bccilogo from "../../assets/images/bcci_logo.png";
import dream11background from "../../assets/images/dream11bg.png";
import "./displayCard.css";
import RadarChartComponent from "../../components/radar_chart/radar";
import RadarChart from "../../components/radar_chart/radar";
import FormBar from "../../components/player_form/formbar";
import SearchBar from "../../components/search_bar/searchbar";
import VenueGraph from "../../components/points_chart/pointschart";
import DisplayCardExpanded from "../../components/player_display_card/displayCardExpanded2";
// import RadarChartComponent from "../radar_chart/radar"

export interface DisplayCardData {
  id: string;
  name: string;
  type: string;
  team: string;
  points: string;
  cost: string;
  score: string;
  runs: string;
  average: string;
  strike_rate: string;
  cvc: string;
  country: string;
}

interface Stat {
  key: string;
  value: string;
}

interface Stats {
  title: string;
  stats: Stat[];
}

interface Graphs {
  title: string;
  description: string;
}

const DisplayScreen: React.FC = () => {


  const DisplayCards: DisplayCardData[] = [
    {
      id: "1",
      name: "FAF DU PLESSIS",
      type: "BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "199",
      average: "49",
      strike_rate: "120",
      cvc: "VC",
      country: "SOUTH AFRICA",
    },
    {
      id: "2",
      name: "VIRAT KOHLI",
      type: "BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "299",
      average: "59",
      strike_rate: "140",
      cvc: "C",
      country: "INDIA",
    },
    {
      id: "3",
      name: "GLENN MAXWELL",
      type: "ALL-ROUNDER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
    {
      id: "4",
      name: "DINESH KARTHIK",
      type: "WICKETKEEPER-BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
    {
      id: "5",
      name: "MOHAMMED SIRAJ",
      type: "BOWLER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
    {
      id: "6",
      name: "WILL JACKS",
      type: "ALL-ROUNDER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
    {
      id: "7",
      name: "MAHIPAL LOMROR",
      type: "ALL-ROUNDER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
    {
      id: "8",
      name: "REECE TOPLEY",
      type: "BOWLER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
    {
      id: "9",
      name: "RAJAT PATIDAR",
      type: "BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
    {
      id: "10",
      name: "ANUJ RAWAT",
      type: "WICKETKEEPER-BATSMAN",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
    {
      id: "11",
      name: "ALZARRI JOSEPH",
      type: "BOWLER",
      team: "RCB",
      points: "207",
      cost: "12",
      score: "89",
      runs: "150",
      average: "39",
      strike_rate: "135",
      cvc: "",
      country: "AUSTRALIA",
    },
  ];

  const row1 = DisplayCards.slice(0, 3); // First 3 cards
  const row2 = DisplayCards.slice(3, 7); // Next 4 cards
  const row3 = DisplayCards.slice(7, 11); // Last 4 cards
  
  return (
    
      <div className="main-display">
        <div className="display-container">
          <div className="display-card-row">
            {row1.map((card) => (


                <DisplayCard key={card.id} card={card} />
              
            ))}
          </div>
        </div>
        <div className="display-container">
          <div className="display-card-row-2">
            {row2.map((card) => (
              <DisplayCard key={card.id} card={card} />
            ))}
          </div>
        </div>
        <div className="display-container">
          <div className="display-card-row-2">
            {row3.map((card) => (
              <DisplayCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      </div>
  );
};

const DisplayCard: React.FC<{
  card: DisplayCardData;
}> = ({ card }) => {
  const containerRef = useRef<HTMLDivElement | null>(null);

  // const { playerData, setPlayerData } = usePlayerData();


  var [isExpanded, setExpanded] = useState(false);
  const handleOpen = () => setExpanded(true);
  const handleClose = () => setExpanded(false);

  // put in context

  // Detect clicks outside the container to reset expanded card
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setExpanded(false); // Reset to initial state
      }
    };

    // Add event listener for clicks outside
    document.addEventListener("mousedown", handleClickOutside);

    // Clean up the event listener when the component unmounts

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

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

  // const format= "";
  const [format, setformat] = useState("Odi");

  //for filterBar(All,T20I, T20)
  const [selectedFilter, setSelectedFilter] = useState("All"); // State for the selected filter
  const [selectedFilter2, setSelectedFilter2] = useState("Overall"); // State for the selected filter
  const [selectedFilter3, setSelectedFilter3] = useState("venue"); // State for the selected filter

  const filters =
    format === "T20"
      ? ["All", "T20I", "T20"]
      : format === "Odi"
      ? ["All", "OdiI", "Odi"]
      : ["All", "TestI", "Test"]; // Filter options
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

  //   type BattingStats = {
  //     player_name: string,
  //                 previous_average: number,
  //                 previous_strike_rate: number,
  //                 innings_played:number,
  //                 previous_runs: number,
  //                 previous_4s: number,
  //                 previous_6s: number,
  //                 previous_fifties: number,
  //                 previous_centuries: number,
  //                 highest_score: number,
  //                 form: number,
  //                 venue_avg: number,
  //                 opposition: number,
  //                 previous_zeros: number,
  //                 tbahs_economy_agg: number,
  //                 tbahs_4s_agg: number,
  //                 tbahp_dismissals_agg: number
  // };

  // type StatsData = {
  //     batting: BattingStats[];
  // };

  // type ApiResponse = {
  //     stats: StatsData;
  // };

  // var maindata: ApiResponse = {
  //   stats: {
  //       batting: [], // Example input; replace with real data
  //   },
  // };

  const typesMap: { [key in "BATTING" | "BOWLING" | "FIELDING"]: TypeData } = {
    BATTING: {
      title: "BATTING",
      stats: [
        // { key: "MATCHES", value: "56" },
        // { key: "INNINGS", value: "50.0" },
        // { key: "RUNS", value: "80%" },
        // { key: "AVERAGE", value: "8989"},
        // { key: "STRIKE RATE", value: "8" },
        // { key: "HIGHEST SCORE", value: "8" },
        // { key: "4s/6s", value: "8" },
        // { key: "50/100", value: "8" },
      ],
    },
    BOWLING: {
      title: "BOWLING",
      stats: [
        // { key: "Average", value: "30.0" },
        // { key: "Economy Rate", value: "5.5" },
        // { key: "Wickets", value: "15" },
        // { key: "Five Wicket Hauls", value: "2" },
      ],
    },
    FIELDING: {
      title: "FIELDING",
      stats: [
        // { key: "Catches", value: "10" },
        // { key: "Run Outs", value: "5" },
        // { key: "Stumps", value: "3" },
      ],
    },
  };

  const piedata = [
    { name: "0", value: 400 },
    { name: "1", value: 300 },
    { name: "2", value: 300 },
    { name: "3", value: 200 },
    { name: "4", value: 100 },
    { name: "6", value: 50 },
  ];

  const [mydata, setmyData] =
    useState<{ [key in "BATTING" | "BOWLING" | "FIELDING"]: TypeData }>(
      typesMap
    );

  // const [allStats, setAllStats] = useState<{ [key in "BATTING" | "BOWLING" | "FIELDING"]: TypeData }>({
  //   BATTING: { title: '', stats: [] },
  //   BOWLING: { title: '', stats: [] },
  //   FIELDING: { title: '', stats: [] },
  // });

  //   const updateTypesMap = (data: any) => {
  //   typesMap.BATTING.stats = [
  //     { key: "MATCHES", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "INNINGS", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "RUNS", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "AVERAGE", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "STRIKE RATE", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "HIGHEST SCORE", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "4s/6s", value: `${data["stats"]["batting"][0]["previous_average"]}/${data["stats"]["batting"][0]["previous_average"]}` || "" },
  //     { key: "50/100", value: `${data["stats"]["batting"][0]["previous_average"]}/${data["stats"]["batting"][0]["previous_average"]}` || "" },
  //   ];

  //   typesMap.BOWLING.stats = [
  //     { key: "Average", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "Economy Rate", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "Wickets", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "Five Wicket Hauls", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //   ];

  //   typesMap.FIELDING.stats = [
  //     { key: "Catches", value:data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "Run Outs", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //     { key: "Stumps", value: data["stats"]["batting"][0]["previous_average"] || "" },
  //   ];

  //   console.log("Updated typesMap:", typesMap);
  // };

  // Prepare data for the `typeData_2` prop
  const typeData_2 = Object.values(mydata).map((type) => ({
    title: type.title,
    stats: type.stats,
  }));

  interface DisplayCardExpandedProps {
    typeData_2: TypeData[];
  }

  return (
      !isExpanded ? (
        <div
          ref={containerRef}
          className={`display-card ${
            card.cvc === "C"
              ? "big"
              : card.id === "5" ||
                card.id === "6" ||
                card.id === "9" ||
                card.id === "10"
              ? "middle"
              : ""
          }`}
        >
          <div className="background-overlay"></div>

          <div className="display-card-overlay">
            {card.name}

            <div className="display-card-overlay-row">
              <div
                className="overlay-row-section"
                style={{
                  borderTopLeftRadius: "15px",
                  borderBottomLeftRadius: "15px",
                }}
              >
                <div style={{ fontSize: "13px", marginBottom: "10px" }}>
                  RUNS
                </div>
                {card.runs}
              </div>
              {/* <div className="divider"></div> */}
              <div className="overlay-row-section">
                <div style={{ fontSize: "13px", marginBottom: "10px" }}>
                  AVERAGE
                </div>
                {card.average}
              </div>
              {/* <div className="divider"></div> */}
              <div
                className="overlay-row-section"
                style={{
                  borderTopRightRadius: "15px",
                  borderBottomRightRadius: "15px",
                }}
              >
                <div style={{ fontSize: "13px", marginBottom: "10px" }}>
                  STRIKE RATE
                </div>
                {card.strike_rate}
              </div>
            </div>
          </div>

          <div className="display-card-points">
            <div>
              207
              <div style={{ fontSize: 20 }}>PTS</div>
            </div>

            <img
              className="display-card-team-logo"
              src={card.team === "RCB" ? rcblogo : milogo}
              alt="Player"
            />

            <div style={{ fontSize: 13 }}>{card.type}</div>
          </div>

          <button
            className="info-button"
            onClick={
              () => {
                setExpanded(true);
              }
              // fetchData("http://127.0.0.1:8000/players/get-player-data")
            }
            aria-label="Info Button"
          >
            i
          </button>

          {card.cvc === "C" && <div className="display-card-c">C</div>}

          {card.cvc === "VC" && <div className="display-card-vc">VC</div>}

          {/* {( (card.cvc === "C" || card.cvc === "VC") && <div className="display-card-cvc">
                {( card.cvc === "C" ? "C" : (card.cvc === "VC" ? "VC" : "") )}
              </div>)} */}

          <img className="display-card-image" src={playerImage} alt="Player" />
        </div>
      ) : (
        <DisplayCardExpanded
          containerRef={containerRef}
          isExpanded={isExpanded}
          setExpanded={setExpanded}
          playerImage={playerImage}
          card={card}
          handleLeftClick={handleLeftClick}
          handleRightClick={handleRightClick}
          handleLeftClickTypes={handleLeftClickTypes}
          handleRightClickTypes={handleRightClickTypes}
          data={data}
          typeData={typeData}
          typeData_2={typeData_2}
          newpiedata={piedata}
          currentIndex={currentIndex}
          currentIndexTypes={currentIndexTypes}
          suggestions={suggestions}
          handleSearch={handleSearch}
          handleClose={handleClose}
          open={isExpanded}
          selectedFilter={selectedFilter}
          selectedFilter2={selectedFilter2}
          selectedFilter3={selectedFilter3}
          filters={filters}
          filters2={filters2}
          filters3={filters3}
          handleFilterChange={handleFilterChange}
          handleFilterChange2={handleFilterChange2}
          handleFilterChange3={handleFilterChange3}
          venuechartdata={[]}
          radarnumbers={[]}
          fantasygraphdata={[]}
          percentages={[]} 
          impactdata={[]}        
        />
      )
  );

  // <div ref={containerRef} className="display-card-expanded" style={{position: isExpanded ? 'absolute' : 'relative', transition: 'all 0.5s ease'}}>
  //   <button className="closeButton" onClick={() => setExpanded(false)}>
  //     &times;
  //   </button>
  //   <img src={dream11background} alt="dream11bg" className="dream11bg"/>

  //   <div className="display-card-top-left">

  //     <div style={{height: "100%"}}>
  //       <img className="display-card-expanded-player-image" src={playerImage} alt="Player" />
  //       <div className="display-card-expanded-overlay">
  //         {card.name}
  //       </div>
  //     </div>

  //     <div className="display-card-expanded-points">

  //       <div>
  //         207
  //         <div style={{fontSize: 20, textAlign: "center"}}>
  //           PTS
  //         </div>
  //       </div>

  //       <div style={{width: "80%", height: "30%", alignItems: "center", justifyItems: "center"}}>
  //         <img className="display-expanded-card-team-logo" src={card.country === "INDIA" ? bccilogo : rcblogo} alt="Player" />
  //         <div style={{fontSize: 20, textAlign: "center"}}>
  //           {card.country}
  //         </div>
  //       </div>

  //       <div style={{fontSize: 17}}>
  //         {card.type}
  //       </div>

  //     </div>

  //     {(card.cvc === "C" &&
  //     <div className="display-card-expanded-c" style={{display: "flex"}}>
  //       C
  //     </div>)}

  //     {(card.cvc === "VC" &&
  //     <div className="display-card-expanded-vc" style={{display: "flex"}}>
  //       VC
  //     </div>)}

  //   </div>

  //   <div className="display-card-bottom-left">

  //     <div style={{height: "100%", width: "70%", display: "flex", flexDirection: "column"}}>
  //       <FormBar hotness={90} />
  //       <RadarChart />
  //       <div style={{fontFamily: "Montserrat", fontWeight: "bolder", fontSize: "24px", color: "white", width: "100%", textAlign: "center"}}>
  //         PLAYER PROFILE
  //       </div>
  //     </div>

  //     <div className="stats">

  //       {/* Header */}
  //       <div style={{ display: 'flex', justifyContent: "space-between", marginBottom: '10px', width: "100%"}}>
  //         <div
  //         onClick={handleLeftClick}
  //         style={{
  //           width: '0',
  //           height: '0',
  //           borderLeft: '10px solid transparent',
  //           borderRight: '10px solid transparent',
  //           borderBottom: '15px solid black',
  //           cursor: 'pointer',
  //           transform: 'rotate(270deg)',
  //         }}
  //         ></div>

  //         <div style={{fontSize: "10px", marginLeft: "17px", marginRight: "17px"}}>
  //           {data[currentIndex].title}
  //         </div>

  //         <div
  //         onClick={handleRightClick}
  //         style={{
  //           width: '0',
  //           height: '0',
  //           borderLeft: '10px solid transparent',
  //           borderRight: '10px solid transparent',
  //           borderBottom: '15px solid black',
  //           cursor: 'pointer',
  //           transform: 'rotate(90deg)',
  //         }}
  //       ></div>
  //       </div>

  //       {/* Stats Column */}
  //       <div style={{height: "70%", width: "100%"}}>
  //         {data[currentIndex].stats.map((stat, index) => (
  //           <div key={index} style={{ display: 'flex', justifyContent: "space-between", paddingBottom: '14px', height: "5%", width: "100%"}}>
  //             <div style={{ fontSize: '12px', color: "gray"}}>{stat.key}</div>
  //             <div style={{ fontSize: '12px' }}>{stat.value}</div>
  //           </div>
  //         ))}
  //       </div>

  //    </div>

  //   </div>

  //   <div className="display-card-top-right">
  //     <SearchBar suggestions={suggestions} onSearch={handleSearch} />
  //     <FantasyPointsChart />
  //     <div style={{width: "80%", height: "2px", backgroundColor: "white"}}></div>
  //   </div>

  //   <div className="display-card-bottom-right">
  //     <div style={{display: "flex", width: "90%", height: "20%", justifyContent: "space-evenly"}}>
  //       <div className="quote-card-1"></div>
  //       <div className="quote-card-1"></div>
  //     </div>

  //     <div style={{border:"2px solid white", width: "80%", height: "70%"}}>

  //     </div>

  //   </div>

  // </div>
};

export default DisplayScreen;
