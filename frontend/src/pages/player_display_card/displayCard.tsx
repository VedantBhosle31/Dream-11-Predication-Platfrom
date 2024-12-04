import React, { useState, useRef, useEffect } from "react";
import playerImage from "../../assets/images/virat_kohli.png"; // Replace with your player image
import milogo from "../../assets/images/mumbai_indians.png";
import rcblogo from "../../assets/images/rcb_logo.png";
import "./displayCard.css";
import DisplayCardExpanded from "../../components/player_display_card/displayCardExpanded2";
import usePlayerStore from "../../store/playerStore";
import { CardData } from "../../SlidingPanels";
import { round } from "lodash";

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
  team_url: string;
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




  const { displayscreencards } = usePlayerStore();


  const sortedCards = [...displayscreencards].sort((a, b) => {
    if (a.cvc === "C" && b.cvc !== "C") return -1; // Prioritize "C"
    if (a.cvc === "VC" && b.cvc !== "VC" && b.cvc !== "C") return -1;
    return 0;
  });


  const row1 = sortedCards.slice(0, 3); // First 3 cards
  const row2 = sortedCards.slice(3, 7); // Next 4 cards
  const row3 = sortedCards.slice(7, 11); // Last 4 cards


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




  const { allmaindata } = usePlayerStore();
  console.log("here we got allmaindata", allmaindata);

  const { displayscreencards } = usePlayerStore();




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
        `${process.env.REACT_APP_BACKEND_URL}/players/get-player-matchups`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            player_name: card.name,
            player_opponents: "RR Hendricks, Q de Kock,AK Markram, T Stubbs,DA Miller, M Jansen,KA Maharaj, K Rabada,A Nortje, T Shamsi,KS Williamson",
            date: matchDate,
            model: model,
          }),
        }
      );

      const matchupsdata = await response.json();
      console.log("response herenhere", matchupsdata["stats"]["AK Markram"]);

      setnewmatchupsdata(matchupsdata);
    }
    setCurrentIndex((prev) => (prev === 0 ? data.length - 1 : prev - 1));
  };

  const handleRightClick = async () => {

    if (currentIndex === 1) {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/players/get-player-matchups`,
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




      console.log("response herenhere", matchupsdata["stats"]["AK Markram"]);

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



  const typesMap: { [key in "BATTING" | "BOWLING" | "FIELDING"]: TypeData } = {
    BATTING: {
      title: "BATTING",
      stats: [],
    },
    BOWLING: {
      title: "BOWLING",
      stats: [],
    },
    FIELDING: {
      title: "FIELDING",
      stats: [],
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

  // Prepare data for the `typeData_2` prop

  const typeData_2 = Object.values(mydata).map((type) => ({
    title: type.title,
    stats: type.stats,
  }));//

  interface DisplayCardExpandedProps {
    typeData_2: TypeData[];
  }//



  useEffect(() => {

    const maindata: any = allmaindata;

    console.log("maindata", maindata);

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

    maindata["stats"]["batting"].forEach((battingData: any) => {
      sums["0"] += battingData["dots"];
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



  return (
    !isExpanded ? (
      <div
        ref={containerRef}
        className={`display-card ${card.cvc === "C"
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
                height: "13vh",
              }}
            >
              <div style={{ fontSize: "13px", marginBottom: "5px" }}>
                RUNS
              </div>
              {round(parseInt(card.runs), 2)}
            </div>
            {/* <div className="divider"></div> */}
            <div className="overlay-row-section" style={{
              height: "13vh",

            }}>
              <div style={{ fontSize: "13px", marginBottom: "5px" }}>
                AVERAGE
              </div>
              {round(parseInt(card.average), 2)}
            </div>
            {/* <div className="divider"></div> */}
            <div
              className="overlay-row-section"
              style={{
                borderTopRightRadius: "15px",
                borderBottomRightRadius: "15px",
                height: "13vh",

              }}
            >
              <div style={{ fontSize: "13px", marginBottom: "5px" }}>
                STRIKE RATE
              </div>
              {round(parseInt(card.strike_rate), 2)}
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

};

























































export default DisplayScreen;
