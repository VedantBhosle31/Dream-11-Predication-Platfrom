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
import usePlayerStore from "../../store/playerStore";
import { CardData } from "../../SlidingPanels";
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
}//

interface Graphs {
  title: string;
  description: string;
}//

const DisplayScreen: React.FC = () => {




  const {displayscreencards} = usePlayerStore();

  // const DisplayCards: DisplayCardData[] = [
  //   {
  //     id: "1",
  //     name: "FAF DU PLESSIS",
  //     type: "BATSMAN",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "199",
  //     average: "49",
  //     strike_rate: "120",
  //     cvc: "VC",
  //     country: "SOUTH AFRICA",
  //   },
  //   {
  //     id: "2",
  //     name: "VIRAT KOHLI",
  //     type: "BATSMAN",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "299",
  //     average: "59",
  //     strike_rate: "140",
  //     cvc: "C",
  //     country: "INDIA",
  //   },
  //   {
  //     id: "3",
  //     name: "GLENN MAXWELL",
  //     type: "ALL-ROUNDER",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  //   {
  //     id: "4",
  //     name: "DINESH KARTHIK",
  //     type: "WICKETKEEPER-BATSMAN",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  //   {
  //     id: "5",
  //     name: "MOHAMMED SIRAJ",
  //     type: "BOWLER",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  //   {
  //     id: "6",
  //     name: "WILL JACKS",
  //     type: "ALL-ROUNDER",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  //   {
  //     id: "7",
  //     name: "MAHIPAL LOMROR",
  //     type: "ALL-ROUNDER",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  //   {
  //     id: "8",
  //     name: "REECE TOPLEY",
  //     type: "BOWLER",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  //   {
  //     id: "9",
  //     name: "RAJAT PATIDAR",
  //     type: "BATSMAN",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  //   {
  //     id: "10",
  //     name: "ANUJ RAWAT",
  //     type: "WICKETKEEPER-BATSMAN",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  //   {
  //     id: "11",
  //     name: "ALZARRI JOSEPH",
  //     type: "BOWLER",
  //     team: "RCB",
  //     points: "207",
  //     cost: "12",
  //     score: "89",
  //     runs: "150",
  //     average: "39",
  //     strike_rate: "135",
  //     cvc: "",
  //     country: "AUSTRALIA",
  //   },
  // ];

  // const row1 = DisplayCards.slice(0, 3); // First 3 cards
  // const row2 = DisplayCards.slice(3, 7); // Next 4 cards
  // const row3 = DisplayCards.slice(7, 11); // Last 4 cards



  // Sort cards so that captain and vc comes first
  
  
  
  const sortedCards = [...displayscreencards].sort((a, b) => {
    if (a.cvc === "C" && b.cvc !== "C") return -1; // Prioritize "C"
    if (a.cvc === "VC" && b.cvc !== "VC" && b.cvc !== "C") return -1;
    return 0;
  });




  // const row1 = displayscreencards.slice(0, 3); // First 3 cards
  // const row2 = displayscreencards.slice(3, 7); // Next 4 cards
  // const row3 = displayscreencards.slice(7, 11); // Last 4 cards


  const row1 = sortedCards.slice(0, 3); // First 3 cards
  const row2 = sortedCards.slice(3, 7); // Next 4 cards
  const row3 = sortedCards.slice(7, 11); // Last 4 cards

  // const { allmaindata, setallmaindata } = usePlayerStore();

  
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
  card: CardData;
}> = ({ card }) => {
  const containerRef = useRef<HTMLDivElement | null>(null); //

  


  // const { allmaindata, setallmaindata } = usePlayerStore();
  const {allmaindata} = usePlayerStore();
  console.log("here we got allmaindata", allmaindata);

  const {displayscreencards} = usePlayerStore();




  var [isExpanded, setExpanded] = useState(false); //
  const handleOpen = () => setExpanded(true); //
  const handleClose = () => setExpanded(false); //

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
  ];//

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
  ]; //

  interface BattingProps {
    average: number;
    strikeRate: number;
    centuries: number;
    halfCenturies: number;
  }//

  interface BowlingProps {
    average: number;
    economyRate: number;
    wickets: number;
    fiveWicketHauls: number;
  }//

  interface FieldingProps {
    catches: number;
    runOuts: number;
    stumpings: number;
  }//

  type Stat = {
    key: string;
    value: string;
  };//

  type TypeData = {
    title: string;
    stats: Stat[];
  };//

  const [currentIndex, setCurrentIndex] = useState(0);//
  const [currentIndexTypes, setCurrentIndexTypes] = useState(0);//

  const { model } = usePlayerStore();
  const { matchDate } = usePlayerStore();

  const handleLeftClick = async () => {
    if (currentIndex === 3) {
      const response = await fetch(
        "http://127.0.0.1:8000/players/get-player-matchups",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json", // Tell the server it's JSON
          },
          body: JSON.stringify({
            player_name: card.name,
            player_opponents:"RR Hendricks, Q de Kock,AK Markram, T Stubbs,DA Miller, M Jansen,KA Maharaj, K Rabada,A Nortje, T Shamsi,KS Williamson",
            date: matchDate,
            model: model,
          }), // Convert the data to a JSON string
        }
      );
      
      const matchupsdata = await response.json();




      console.log("response herenhere",matchupsdata["stats"]["AK Markram"]);

      setnewmatchupsdata(matchupsdata);
    }
    setCurrentIndex((prev) => (prev === 0 ? data.length - 1 : prev - 1));
  };

  const handleRightClick = async () => {

    if (currentIndex === 1) {
      const response = await fetch(
        "http://127.0.0.1:8000/players/get-player-matchups",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json", // Tell the server it's JSON
          },
          body: JSON.stringify({
            player_name: card.name,
            player_opponents:
              "RR Hendricks, Q de Kock,AK Markram, T Stubbs,DA Miller, M Jansen,KA Maharaj, K Rabada,A Nortje, T Shamsi,KS Williamson",
            date: matchDate,
            model: model,
          }), // Convert the data to a JSON string
        }
      );
      
      const matchupsdata = await response.json();




      console.log("response herenhere",matchupsdata["stats"]["AK Markram"]);

      setnewmatchupsdata(matchupsdata);
    }
    setCurrentIndex((prev) => (prev === data.length - 1 ? 0 : prev + 1));
  };

  const handleLeftClickTypes = () => {
    setCurrentIndexTypes((prev) =>
      prev === 0 ? typeData_2.length - 1 : prev - 1
    );
  };//

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
  ];//

  const handleSearch = (query: string) => {
    console.log("Search Query:", query);
    alert(`You searched for: ${query}`);
  };//

  // const format= "";
  const [format, setformat] = useState("Odi");//

  //for filterBar(All,T20I, T20)
  const [selectedFilter, setSelectedFilter] = useState("All"); //// State for the selected filter
  const [selectedFilter2, setSelectedFilter2] = useState("Overall");// // State for the selected filter
  const [selectedFilter3, setSelectedFilter3] = useState("venue"); //// State for the selected filter

  const filters =
    model === "T20"
      ? ["All", "T20I", "T20"]
      : model === "Odi"
      ? ["All", "OdiI", "Odi"]
      : ["All", "TestI", "Test"]; // Filter options
  const filters2 = ["Overall", "Powerplay", "Middle", "Death"]; // Filter options
  const filters3 = ["venue", "opposition", "form"]; // Filter options
//

  const handleFilterChange = (filter: string) => {
    setSelectedFilter(filter); // Update the selected filter
  };//
  const handleFilterChange2 = (filter: string) => {
    setSelectedFilter2(filter); // Update the selected filter
  };//
  const handleFilterChange3 = (filter: string) => {
    setSelectedFilter3(filter); // Update the selected filter
  };//

  interface ChartData {
    match: string;
    venue: number;
    opposition: number;
    form: number;
    id: number;
  }

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
  };//

  const piedata = [
    { name: "0", value: 400 },
    { name: "1", value: 300 },
    { name: "2", value: 300 },
    { name: "3", value: 200 },
    { name: "4", value: 100 },
    { name: "6", value: 50 },
  ];//

  const venuedata: ChartData[] = [
    {
      match: "vs AUS",
      id: 1,
      venue: 120,
      opposition: 80,
      form: 169.2,
    },
    {
      match: "vs ENG",
      venue: 112,
      opposition: 80,
      form: 169.2,
      id: 2,
    },
    {
      match: "vs USA",
      venue: 120,
      opposition: 80,
      form: 169.2,
      id: 3,
    },
    {
      match: "vs NZ",
      venue: 120,
      opposition: 80,
      form: 169.2,
      id: 4,
    },
    {
      match: "vs AFG",
      venue: 120,
      opposition: 80,
      form: 169.2,
      id: 5,
    },
    {
      match: "vs SL",
      venue: 120,
      opposition: 80,
      form: 169.2,
      id: 5,
    },
    {
      match: "vs SA",
      venue: 140,
      opposition: 100,
      form: 150,
      id: 7,
    },
    {
      match: "vs BAN",
      venue: 110,
      opposition: 90,
      form: 132.8,
      id: 8,
    },
    {
      match: "vs WI",
      venue: 130,
      opposition: 110,
      form: 120.8,
      id: 9,
    },
    {
      match: "vs PAK",
      venue: 150,
      opposition: 120,
      form: 167.9,
      id: 10,
    },
  ];

  const radardata: number[] = [10, 20, 30, 40, 50, 60];

  const fantasygraphdata = [
    { date: "13 Nov", value: 50 },
    { date: "14 Nov", value: 30 },
    { date: "15 Nov", value: 20 },
    { date: "16 Nov", value: 27 },
    { date: "17 Nov", value: 18 },
    { date: "18 Nov", value: 23 },
    { date: "19 Nov", value: 34 },
    { date: "21 Nov", value: 50 },
    { date: "22 Nov", value: 30 },
    { date: "23 Nov", value: 20 },
    { date: "24 Nov", value: 27 },
    { date: "25 Nov", value: 18 },
    { date: "26 Nov", value: 23 },
    { date: "27 Nov", value: 34 },
  ];

  const percentages = [75, 50, 90];

  const [mydata, setmyData] =
    useState<{ [key in "BATTING" | "BOWLING" | "FIELDING"]: TypeData }>(
      typesMap
    );//

    const [newpiedata, setnewpieData] =
    useState<{ name: string; value: number }[]>(piedata);

  const [newradardata, setnewradarData] = useState<number[]>(radardata);

  const [newfantasygraphdata, setnewfantasygraphData] =
    useState<{ date: string; value: number }[]>(fantasygraphdata);

    const [newvenuedata, setnewvenueData] = useState<ChartData[]>(venuedata);
  
  const [newpercentages, setnewpercentages] = useState<number[]>(percentages);

  const [newimpactdata, setnewimpactdata] = useState<any>([]);

  const [newmatchupsdata, setnewmatchupsdata] = useState<any>([]);

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
  }));//

  interface DisplayCardExpandedProps {
    typeData_2: TypeData[];
  }//



  // const handleClick = () => {
  //   setExpanded(true);
  //   // alert('Button clicked!');
  // };


  useEffect(() => {
    // const response = await fetch(
    //   "http://127.0.0.1:8000/players/get-player-data",
    //   {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json", // Tell the server it's JSON
    //     },
    //     body: JSON.stringify({
    //       // name: "V Kohli",
    //       // name: "GJ Maxwell",
    //       // name: "MS Dhoni",
    //       // name: "G Gambhir",
    //       // name: "JJ Bumrah",
    //       // name: "RG Sharma",
    //       // name: "R Ashwin",
    //       name: "SR Tendulkar",
    //       // name: "HH Pandya",
    //       date: "2025-01-01",
    //       model: "Odi",
    //     }), // Convert the data to a JSON string
    //   }
    // );

    // if (!response.ok) {
    //   throw new Error(`Error: ${response.statusText}`);
    // }

    // const fetcheddata = await response.json();

    const maindata:any = allmaindata;

    // storing the fetched data to maindata
    // setallmaindata(maindata);

    setmyData({
      BATTING: {
        title: "BATTING",
        stats: [
          {
            key: "MATCHES",
            value: maindata["stats"]["batting"][0]["innings_played"],
          },
          {
            key: "INNINGS",
            value: maindata["stats"]["batting"][0]["innings_played"],
          },
          {
            key: "RUNS",
            value: maindata["stats"]["batting"][0]["previous_runs"],
          },
          {
            key: "AVERAGE",
            value:
              maindata["stats"]["batting"][0]["previous_average"].toFixed(2),
          },
          {
            key: "STRIKE RATE",
            value:
              maindata["stats"]["batting"][0]["previous_strike_rate"].toFixed(
                2
              ),
          },
          {
            key: "HIGHEST SCORE",
            value: maindata["stats"]["batting"][0]["highest_score"],
          },
          {
            key: "4s/6s",
            value: `${maindata["stats"]["batting"][0]["previous_4s"]}/${maindata["stats"]["batting"][0]["previous_6s"]}`,
          },
          {
            key: "50/100",
            value: `${maindata["stats"]["batting"][0]["previous_fifties"]}/${maindata["stats"]["batting"][0]["previous_centuries"]}`,
          },
        ],
      },
      BOWLING: {
        title: "BOWLING",
        stats: [
          {
            key: "MATCHES",
            value: maindata["stats"]["bowling"][0]["innings_played"],
          },
          {
            key: "BALLS",
            value: maindata["stats"]["bowling"][0]["previous_balls_involved"],
          },
          {
            key: "WICKETS",
            value: maindata["stats"]["bowling"][0]["previous_wickets"],
          },
          {
            key: "STRIKE RATE",
            value:
              maindata["stats"]["bowling"][0]["previous_strike_rate"].toFixed(
                2
              ),
          },
          {
            key: "MAIDENS",
            value: maindata["stats"]["bowling"][0]["previous_maidens"],
          },
          {
            key: "ECONOMY",
            value:
              maindata["stats"]["bowling"][0]["previous_economy"].toFixed(2),
          },
          {
            key: "AVERAGE",
            value:
              maindata["stats"]["bowling"][0]["previous_average"].toFixed(2),
          },
          {
            key: "3/4/5 WICKETS",
            value: `${maindata["stats"]["bowling"][0]["previous_wickets"]}/${maindata["stats"]["bowling"][0]["previous_wickets"]}/${maindata["stats"]["bowling"][0]["previous_wickets"]}`,
          },
        ],
      },
      FIELDING: {
        title: "FIELDING",
        stats: [
          {
            key: "MATCHES",
            value: maindata["stats"]["bowling"][0]["innings_played"],
          },
          {
            key: "INNINGS",
            value: maindata["stats"]["bowling"][0]["innings_played"],
          },
          {
            key: "RUN OUTS",
            value: maindata["stats"]["fielding"][0]["previous_runouts"],
          },
          {
            key: "CATCHES",
            value: maindata["stats"]["fielding"][0]["previous_catches"],
          },
        ],
      },
    });

    let sums = { "0": 0, "4": 0, "6": 0 };
    // let sumsrecent = { "form": 0, "opposition": 0, "venue": 0 };

    maindata["stats"]["batting"].forEach((battingData: any) => {
      sums["0"] += battingData["dots"];
      // sums["4"] += battingData["previous_4s"];
      // sums["6"] += battingData["sixes"];
    });

    var formRatio = 0;
    var oppositionRatio = 0;
    var venueRatio = 0;

    const processData = (data: any[]) => {
      // Initialize the variables to track the max values and sums
      let formMax = -Infinity;
      let oppositionMax = -Infinity;
      let venueMax = -Infinity;

      let formSum = 0;
      let oppositionSum = 0;
      let venueSum = 0;

      // Loop through the data to find max values and sum the corresponding fields
      data.forEach((item) => {
        // Max value for form
        if (item.form > formMax) {
          formMax = item.form;
        }
        // Max value for opposition
        if (item.opposition > oppositionMax) {
          oppositionMax = item.opposition;
        }
        // Max value for venue
        if (item.venue > venueMax) {
          venueMax = item.venue;
        }

        // Summing values
        formSum += item.form;
        oppositionSum += item.opposition;
        venueSum += item.venue;
      });

      // Calculate ratios
      formRatio = formMax !== 0 ? (formSum * 10) / formMax : 0;
      oppositionRatio =
        oppositionMax !== 0 ? (oppositionSum * 10) / oppositionMax : 0;
      venueRatio = venueMax !== 0 ? (venueSum * 10) / venueMax : 0;

      return {
        formRatio,
        oppositionRatio,
        venueRatio,
      };
    };

    processData(maindata["stats"]["batting"]);

    setnewpieData([
      { name: "0", value: sums["0"] },
      { name: "4", value: maindata["stats"]["batting"][0]["previous_4s"] },
      { name: "6", value: maindata["stats"]["batting"][0]["previous_6s"] },
      {
        name: "1,2,3",
        value:
          maindata["stats"]["batting"][0]["previous_balls_involved"] -
          (maindata["stats"]["batting"][0]["previous_4s"] +
            maindata["stats"]["batting"][0]["previous_6s"]),
      },
    ]);


    setnewradarData([
      maindata["stats"]["batting"][0]["previous_strike_rate"],
      maindata["stats"]["bowling"][0]["previous_wickets"],
      maindata["stats"]["bowling"][0]["previous_economy"],

      maindata["stats"]["batting"][0]["opposition"],

      maindata["stats"]["fielding"][0]["pfa_catches"],
      maindata["stats"]["batting"][0]["previous_average"],
    ]);

    setnewfantasygraphData([
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][0]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][0]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][1]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][1]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][2]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][2]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][3]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][3]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][4]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][4]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][5]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][5]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][6]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][6]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][7]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][7]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][8]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][8]["odi_match_fantasy_points"],
      },
      {
        date: "13 Nov",
        value:
          maindata["stats"]["batting"][9]["odi_match_fantasy_points"] < 0
            ? 0
            : maindata["stats"]["batting"][9]["odi_match_fantasy_points"],
      },
    ]);

    setnewvenueData(
      Array.from({ length: 10 }, (_, index) => {
        return {
          match: `${index}`,
          id: index,
          venue: maindata["stats"]["batting"][index]["venue_avg"],
          opposition: maindata["stats"]["batting"][index]["opposition"],
          form: maindata["stats"]["batting"][index]["form"],
        };
      })
    );

    setnewpercentages([
      Math.round(formRatio * 100) / 100,
      Math.round(oppositionRatio * 100) / 100,
      Math.round(venueRatio * 100) / 100,
    ]);

    // Extract stats from maindata
    const battingStats = maindata["stats"]["batting"];

    setnewimpactdata(battingStats);

    console.log("maindata", maindata["stats"]);
  }, []);


  // const handleClick = () => {
  //   setExpanded(true);
    

  //   // const response = await fetch(
  //   //   "http://127.0.0.1:8000/players/get-player-data",
  //   //   {
  //   //     method: "POST",
  //   //     headers: {
  //   //       "Content-Type": "application/json", // Tell the server it's JSON
  //   //     },
  //   //     body: JSON.stringify({
  //   //       // name: "V Kohli",
  //   //       // name: "GJ Maxwell",
  //   //       // name: "MS Dhoni",
  //   //       // name: "G Gambhir",
  //   //       // name: "JJ Bumrah",
  //   //       // name: "RG Sharma",
  //   //       // name: "R Ashwin",
  //   //       name: "SR Tendulkar",
  //   //       // name: "HH Pandya",
  //   //       date: "2025-01-01",
  //   //       model: "Odi",
  //   //     }), // Convert the data to a JSON string
  //   //   }
  //   // );

  //   // if (!response.ok) {
  //   //   throw new Error(`Error: ${response.statusText}`);
  //   // }

  //   // const fetcheddata = await response.json();

  //   const maindata:any = allmaindata;

  //   // storing the fetched data to maindata
  //   // setallmaindata(maindata);

  //   setmyData({
  //     BATTING: {
  //       title: "BATTING",
  //       stats: [
  //         {
  //           key: "MATCHES",
  //           value: maindata["stats"]["batting"][0]["innings_played"],
  //         },
  //         {
  //           key: "INNINGS",
  //           value: maindata["stats"]["batting"][0]["innings_played"],
  //         },
  //         {
  //           key: "RUNS",
  //           value: maindata["stats"]["batting"][0]["previous_runs"],
  //         },
  //         {
  //           key: "AVERAGE",
  //           value:
  //             maindata["stats"]["batting"][0]["previous_average"].toFixed(2),
  //         },
  //         {
  //           key: "STRIKE RATE",
  //           value:
  //             maindata["stats"]["batting"][0]["previous_strike_rate"].toFixed(
  //               2
  //             ),
  //         },
  //         {
  //           key: "HIGHEST SCORE",
  //           value: maindata["stats"]["batting"][0]["highest_score"],
  //         },
  //         {
  //           key: "4s/6s",
  //           value: `${maindata["stats"]["batting"][0]["previous_4s"]}/${maindata["stats"]["batting"][0]["previous_6s"]}`,
  //         },
  //         {
  //           key: "50/100",
  //           value: `${maindata["stats"]["batting"][0]["previous_fifties"]}/${maindata["stats"]["batting"][0]["previous_centuries"]}`,
  //         },
  //       ],
  //     },
  //     BOWLING: {
  //       title: "BOWLING",
  //       stats: [
  //         {
  //           key: "MATCHES",
  //           value: maindata["stats"]["bowling"][0]["innings_played"],
  //         },
  //         {
  //           key: "BALLS",
  //           value: maindata["stats"]["bowling"][0]["previous_balls_involved"],
  //         },
  //         {
  //           key: "WICKETS",
  //           value: maindata["stats"]["bowling"][0]["previous_wickets"],
  //         },
  //         {
  //           key: "STRIKE RATE",
  //           value:
  //             maindata["stats"]["bowling"][0]["previous_strike_rate"].toFixed(
  //               2
  //             ),
  //         },
  //         {
  //           key: "MAIDENS",
  //           value: maindata["stats"]["bowling"][0]["previous_maidens"],
  //         },
  //         {
  //           key: "ECONOMY",
  //           value:
  //             maindata["stats"]["bowling"][0]["previous_economy"].toFixed(2),
  //         },
  //         {
  //           key: "AVERAGE",
  //           value:
  //             maindata["stats"]["bowling"][0]["previous_average"].toFixed(2),
  //         },
  //         {
  //           key: "3/4/5 WICKETS",
  //           value: `${maindata["stats"]["bowling"][0]["previous_wickets"]}/${maindata["stats"]["bowling"][0]["previous_wickets"]}/${maindata["stats"]["bowling"][0]["previous_wickets"]}`,
  //         },
  //       ],
  //     },
  //     FIELDING: {
  //       title: "FIELDING",
  //       stats: [
  //         {
  //           key: "MATCHES",
  //           value: maindata["stats"]["bowling"][0]["innings_played"],
  //         },
  //         {
  //           key: "INNINGS",
  //           value: maindata["stats"]["bowling"][0]["innings_played"],
  //         },
  //         {
  //           key: "RUN OUTS",
  //           value: maindata["stats"]["fielding"][0]["previous_runouts"],
  //         },
  //         {
  //           key: "CATCHES",
  //           value: maindata["stats"]["fielding"][0]["previous_catches"],
  //         },
  //       ],
  //     },
  //   });

  //   let sums = { "0": 0, "4": 0, "6": 0 };
  //   // let sumsrecent = { "form": 0, "opposition": 0, "venue": 0 };

  //   maindata["stats"]["batting"].forEach((battingData: any) => {
  //     sums["0"] += battingData["dots"];
  //     // sums["4"] += battingData["previous_4s"];
  //     // sums["6"] += battingData["sixes"];
  //   });

  //   var formRatio = 0;
  //   var oppositionRatio = 0;
  //   var venueRatio = 0;

  //   const processData = (data: any[]) => {
  //     // Initialize the variables to track the max values and sums
  //     let formMax = -Infinity;
  //     let oppositionMax = -Infinity;
  //     let venueMax = -Infinity;

  //     let formSum = 0;
  //     let oppositionSum = 0;
  //     let venueSum = 0;

  //     // Loop through the data to find max values and sum the corresponding fields
  //     data.forEach((item) => {
  //       // Max value for form
  //       if (item.form > formMax) {
  //         formMax = item.form;
  //       }
  //       // Max value for opposition
  //       if (item.opposition > oppositionMax) {
  //         oppositionMax = item.opposition;
  //       }
  //       // Max value for venue
  //       if (item.venue > venueMax) {
  //         venueMax = item.venue;
  //       }

  //       // Summing values
  //       formSum += item.form;
  //       oppositionSum += item.opposition;
  //       venueSum += item.venue;
  //     });

  //     // Calculate ratios
  //     formRatio = formMax !== 0 ? (formSum * 10) / formMax : 0;
  //     oppositionRatio =
  //       oppositionMax !== 0 ? (oppositionSum * 10) / oppositionMax : 0;
  //     venueRatio = venueMax !== 0 ? (venueSum * 10) / venueMax : 0;

  //     return {
  //       formRatio,
  //       oppositionRatio,
  //       venueRatio,
  //     };
  //   };

  //   processData(maindata["stats"]["batting"]);

  //   setnewpieData([
  //     { name: "0", value: sums["0"] },
  //     { name: "4", value: maindata["stats"]["batting"][0]["previous_4s"] },
  //     { name: "6", value: maindata["stats"]["batting"][0]["previous_6s"] },
  //     {
  //       name: "1,2,3",
  //       value:
  //         maindata["stats"]["batting"][0]["previous_balls_involved"] -
  //         (maindata["stats"]["batting"][0]["previous_4s"] +
  //           maindata["stats"]["batting"][0]["previous_6s"]),
  //     },
  //   ]);


  //   setnewradarData([
  //     maindata["stats"]["batting"][0]["previous_strike_rate"],
  //     maindata["stats"]["bowling"][0]["previous_wickets"],
  //     maindata["stats"]["bowling"][0]["previous_economy"],

  //     maindata["stats"]["batting"][0]["opposition"],

  //     maindata["stats"]["fielding"][0]["pfa_catches"],
  //     maindata["stats"]["batting"][0]["previous_average"],
  //   ]);

  //   setnewfantasygraphData([
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][0]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][0]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][1]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][1]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][2]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][2]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][3]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][3]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][4]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][4]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][5]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][5]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][6]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][6]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][7]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][7]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][8]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][8]["odi_match_fantasy_points"],
  //     },
  //     {
  //       date: "13 Nov",
  //       value:
  //         maindata["stats"]["batting"][9]["odi_match_fantasy_points"] < 0
  //           ? 0
  //           : maindata["stats"]["batting"][9]["odi_match_fantasy_points"],
  //     },
  //   ]);

  //   setnewvenueData(
  //     Array.from({ length: 10 }, (_, index) => {
  //       return {
  //         match: `${index}`,
  //         id: index,
  //         venue: maindata["stats"]["batting"][index]["venue_avg"],
  //         opposition: maindata["stats"]["batting"][index]["opposition"],
  //         form: maindata["stats"]["batting"][index]["form"],
  //       };
  //     })
  //   );

  //   setnewpercentages([
  //     Math.round(formRatio * 100) / 100,
  //     Math.round(oppositionRatio * 100) / 100,
  //     Math.round(venueRatio * 100) / 100,
  //   ]);

  //   // Extract stats from maindata
  //   const battingStats = maindata["stats"]["batting"];

  //   setnewimpactdata(battingStats);

  //   console.log("maindata", maindata["stats"]);
  // };



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
                // handleClick();
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
          // newpiedata={piedata}
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
          newpiedata={newpiedata}
        venuechartdata={newvenuedata}
        radarnumbers={newradardata}
        fantasygraphdata={newfantasygraphdata}
        percentages={newpercentages}
        impactdata={newimpactdata} 
        matchupsdata={newmatchupsdata}        
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
