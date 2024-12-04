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
import usePlayerStore from "../../store/playerStore";
import defaultimg from "../../assets/images/default.png"; // Replace with your player image

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

var maindata: any = [];

const DroppableCard: React.FC<{
  card: CardData;
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
  } //

  interface Graphs {
    title: string;
    description: string;
  } //

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
  ]; //

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
  }; //

  type TypeData = {
    title: string;
    stats: Stat[];
  }; //

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
  }; //

  const piedata = [
    { name: "0", value: 400 },
    { name: "1", value: 300 },
    { name: "2", value: 300 },
    { name: "3", value: 200 },
    { name: "4", value: 100 },
    { name: "6", value: 50 },
  ]; //

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

  // State to store fetched data (no specific type)
  const [mydata, setmyData] =
    useState<{ [key in "BATTING" | "BOWLING" | "FIELDING"]: TypeData }>(
      typesMap
    ); //

  const [newpiedata, setnewpieData] =
    useState<{ name: string; value: number }[]>(piedata);

  const [newvenuedata, setnewvenueData] = useState<ChartData[]>(venuedata);

  const [newradardata, setnewradarData] = useState<number[]>(radardata);

  const [newfantasygraphdata, setnewfantasygraphData] =
    useState<{ date: string; value: number }[]>(fantasygraphdata);

  const [newpercentages, setnewpercentages] = useState<number[]>(percentages);

  const [newimpactdata, setnewimpactdata] = useState<any>([]);

  const [newmatchupsdata, setnewmatchupsdata] = useState<any>([]);

  // Prepare data for the `typeData_2` prop

  const typeData_2 = Object.values(mydata).map((type) => ({
    title: type.title,
    stats: type.stats,
  })); //

  interface DisplayCardExpandedProps {
    typeData_2: TypeData[];
  } //

  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentIndexTypes, setCurrentIndexTypes] = useState(0);

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

      console.log("response herenhere", matchupsdata["stats"]["AK Markram"]);

      setnewmatchupsdata(matchupsdata);
    }
    setCurrentIndex((prev) => (prev === data.length - 1 ? 0 : prev + 1));
  };

  const handleLeftClickTypes = () => {
    setCurrentIndexTypes((prev) =>
      prev === 0 ? typeData_2.length - 1 : prev - 1
    );
  }; //

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
  ]; //

  const handleSearch = (query: string) => {
    console.log("Search Query:", query);
    alert(`You searched for: ${query}`);
  }; //

  //for filterBar(All,T20I, T20)
  const [selectedFilter, setSelectedFilter] = useState("All"); // State for the selected filter
  const [selectedFilter2, setSelectedFilter2] = useState("Overall"); // State for the selected filter
  const [selectedFilter3, setSelectedFilter3] = useState("venue"); // State for the selected filter

  // const [format, setformat] = useState("Odi");//

  const { model } = usePlayerStore();
  const { matchDate } = usePlayerStore();
  // const { model } = usePlayerStore();

  // const filters = ["All", "T20I", "T20"]; // Filter options
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
  }; //
  const handleFilterChange2 = (filter: string) => {
    setSelectedFilter2(filter); // Update the selected filter
  }; //
  const handleFilterChange3 = (filter: string) => {
    setSelectedFilter3(filter); // Update the selected filter
  }; //

  interface somecarddata {
    name: string;
    country: string;
    type: string;
    cvc: string;
  }

  interface ChartData {
    match: string;
    venue: number;
    opposition: number;
    form: number;
    id: number;
  }

  // const { details } = useUserContext();

  // const { setDetails } = useUserContext();

  // const updateDetails = () => {
  //   setDetails(["newDetail1", "newDetail2"]);
  // };

  const { allmaindata, setallmaindata } = usePlayerStore();

  const fetchData = async (url: string) => {
    setCardExpanded(true);

    const response = await fetch(
      "http://127.0.0.1:8000/players/get-player-data",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Tell the server it's JSON
        },
        body: JSON.stringify({
          // name: "V Kohli",
          // name: "GJ Maxwell",
          // name: "MS Dhoni",
          // name: "G Gambhir",
          // name: "JJ Bumrah",
          // name: "RG Sharma",
          // name: "R Ashwin",
          name: card.name,
          // name: "HH Pandya",
          date: matchDate,
          model: model,
        }), // Convert the data to a JSON string
      }
    );

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const fetcheddata = await response.json();

    maindata = fetcheddata;

    // storing the fetched data to maindata
    setallmaindata(maindata);

    console.log(maindata);

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
              maindata["stats"]["batting"][0]["previous_strike_rate"].toFixed(2),
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
              maindata["stats"]["bowling"][0]["previous_strike_rate"].toFixed(2),
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

    const result = [];

    for (let i = 0; i < maindata["stats"]["batting"].length; i++) {
      const format = model; // Replace with the actual model value

      result.push({
        date: maindata["stats"]["batting"][i]["date"],
        value: maindata["stats"]["batting"][i][`${model.toLowerCase()}_match_fantasy_points`] < 0
            ? 0
            : maindata["stats"]["batting"][i][`${model.toLowerCase()}_match_fantasy_points`],
      });
    }


    setnewfantasygraphData(result);

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
  };

  return !isCardExpanded ? (
    <div
      className="droppable-card"
      onClick={() => { }}
      style={{ border: selectedCard === card ? "2px solid white" : "none" }}
      onDropCapture={() => onSelectCard(card)}
    >
      <div className="left-half"></div>
      <div className="right-half"></div>

      <div className="droppable-card-points">
        <div>
        {parseFloat(card.points).toFixed(2)}
          <div style={{ fontSize: 6, color: "red" }}>PTS</div>
        </div>

        <img
          className="team-logo"
          src={card.team === "RCB" ? rcblogo : milogo}
          alt={defaultimg}
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

      {card.cvc === "C" && (
        <div
          className="absolute text-white w-10 h-10 px-2 py-2 font-bold"
          style={{
            backgroundColor: "rgb(235, 134, 2)",
            fontFamily: "Montserrat",
          }}
        >
          C
        </div>
      )}

      {card.cvc === "VC" && (
        <div
          className="absolute text-white bg-black w-10 h-10 px-2 py-2 font-bold"
          style={{
            backgroundColor: "rgb(2, 157, 235)",
            fontFamily: "Montserrat",
          }}
        >
          VC
        </div>
      )}

      {isedit && (
        <button className="remove-button" onClick={() => onRemove(card)}>
          <RemoveCircleOutline style={{ width: "13px", height: "13px" }} />
        </button>
      )}

      {isedit && (
        <div className="absolute inset-0 bg-black bg-opacity-60 flex flex-col items-center justify-center opacity-0 hover:opacity-100 transition-opacity z-10 text-xs">
          <button
            onClick={() => handleSetCVC(card.id, "C")}
            className=" py-1 px-3 rounded-lg mb-2 transition h-8 w-[%70]"
            style={{
              backgroundColor: "rgb(235, 134, 2)",
              fontFamily: "Montserrat",
              fontSize: "70%",
            }}
          >
            Make Captain
          </button>

          <button
            onClick={() => handleSetCVC(card.id, "VC")}
            className=" py-1 px-3 rounded-lg mb-2 transition h-8 w-[%70]"
            style={{
              backgroundColor: "rgb(2, 157, 235)",
              fontFamily: "Montserrat",
              fontSize: "70%",
            }}
          >
            Make Vice-Captain
          </button>

          <button
            // onClick={updateDetails}
            onClick={() =>
              fetchData("http://127.0.0.1:8080/players/get-player-data")
            }
            className=" py-1 px-3 rounded-lg mb-2 transition h-8 w-[%70]"
            style={{
              backgroundColor: "rgb(235, 134, 2)",
              fontFamily: "Montserrat",
              fontSize: "70%",
            }}
          >
            Show Info
          </button>
        </div>
      )}

      <img className="card-image" src={card.img_url} alt={defaultimg} />
    </div>
  ) : (
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
      newpiedata={newpiedata}
      venuechartdata={newvenuedata}
      radarnumbers={newradardata}
        // fantasygraphdata={newfantasygraphdata}
        fantasygraphdata={fantasygraphdata}
      percentages={newpercentages}
      impactdata={newimpactdata}
      matchupsdata={newmatchupsdata}
    />
  );
};

const Placeholder: React.FC = () => {
  return (
    <div className="placeholder-card">
      <div className="placeholder-border">
        <IconButton onClick={() => { }}>
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