import dream11background from "../../assets/images/dream11bg.png";
import "./displayCard2.css";
import RadarChart from "../radar_chart/radar";
import SearchBar from "../search_bar/searchbar";
import VenueGraph from "../points_chart/pointschart";
import { Box, Modal, Skeleton } from "@mui/material";
import { useEffect } from "react";
import {
  Bar,
  BarChart,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import CircularProgress from "../circular_preformance/circularBar";
import FilterBar from "../filterBar/filterBar";
import ImpactChart from "../impactindexchart/impactchart";
import ExplainGraphButton from "../explain_graph/explaingraph";
import usePlayerStore from "../../store/playerStore";
import { CardData } from "../../SlidingPanels";
import defaultimg from "../../assets/images/default.png";

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#6366F1",
  "#FA2433",
];

const exampleQueries = [
  "Top Scorers in IPL 2024",
  "Fastest Bowler Stats",
  "Most Runs by a Player",
];

const handleSearch = (query: string) => {
  console.log("Search query:", query);
};

const style = {
  position: "absolute",
  width: "70%",
  height: "90%",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  bgcolor: "black",
  border: "2px solid #000",
  boxShadow: 24,
  p: 1,
  display: "flex",
  transition: "0.5s all ease",
  fontFamily: "Montserrat",
};

interface ChartData {
  match: string;
  venue: number;
  opposition: number;
  form: number;
  id: number;
}

interface DisplayCardExpandedProps {
  containerRef: React.RefObject<HTMLDivElement>;
  isExpanded: boolean;
  setExpanded: React.Dispatch<React.SetStateAction<boolean>>;
  playerImage: string;
  card: CardData;
  handleLeftClick: () => void;
  handleRightClick: () => void;
  handleRightClickTypes: () => void;
  handleLeftClickTypes: () => void;
  data: {
    title: string;
    description: string;
  }[];
  typeData: {
    title: string;
    stats: { key: string; value: string }[];
  }[];
  typeData_2: {
    title: string;
    stats: { key: string; value: string }[];
  }[];
  currentIndex: number;
  currentIndexTypes: number;
  suggestions: string[];
  handleSearch: (search: string) => void;
  handleClose: (search: string) => void;
  open: boolean;
  selectedFilter: string;
  selectedFilter2: string;
  selectedFilter3: string;
  filters: string[];
  filters2: string[];
  filters3: string[];
  handleFilterChange: (filter: string) => void;
  handleFilterChange2: (filter: string) => void;
  handleFilterChange3: (filter: string) => void;
  newpiedata: { name: string; value: number }[];
  venuechartdata: ChartData[];
  radarnumbers: number[];
  fantasygraphdata: { date: string; value: number }[];
  percentages: number[];
  impactdata: any;
  matchupsdata: any;
  team: string;
}

const DisplayCardExpanded: React.FC<DisplayCardExpandedProps> = ({
  containerRef,
  isExpanded,
  setExpanded,
  playerImage,
  card,
  handleLeftClick,
  handleRightClick,
  handleRightClickTypes,
  handleLeftClickTypes,
  data,
  typeData,
  typeData_2,
  currentIndex,
  currentIndexTypes,
  suggestions,
  handleSearch,
  open,
  handleClose,
  selectedFilter,
  selectedFilter2,
  selectedFilter3,
  filters,
  filters2,
  filters3,
  handleFilterChange,
  handleFilterChange2,
  handleFilterChange3,
  newpiedata,
  venuechartdata,
  radarnumbers,
  fantasygraphdata,
  percentages,
  impactdata,
  matchupsdata,
  team,
}) => {
  const { model } = usePlayerStore();
  const { matchDate } = usePlayerStore();

  var temptitleexplain: string = "";
  var explaindate: string = matchDate;
  var opponents: string = "RR Hendricks, Q de Kock,AK Markram, T Stubbs,DA Miller, M Jansen,KA Maharaj, K Rabada,A Nortje, T Shamsi,KS Williamson";
  var typeofplayer: string = "";

  const { playerdescription, setplayerdescription } = usePlayerStore();
  const {
    playerTeamMap,
  } = usePlayerStore();

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/genai/describe-player/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            feature_name: "player_description",
            // user_task: user_task,
            player_name: card.name,
            date: matchDate,
            model: model,
            player_opponents:Object.keys(playerTeamMap).filter(player => playerTeamMap[player] !== playerTeamMap[card.name]).join(","),
            player_type: card.type,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const fetcheddata = await response.json();
      console.log("Fetched Data:", fetcheddata["description"]);

      setplayerdescription(fetcheddata["description"]);
    };

    fetchData();
  }, []);

  const containsBat = (str: string) => str.includes("bat");
  const containsbowl = (str: string) => str.includes("bowl");
  const containsall = (str: string) => str.includes("all");
  const containswk = (str: string) => str.includes("wicketkeeper");

  if (containsBat(card.type)) {
    typeofplayer = "BATTER";
    if (currentIndex === 0) {
      temptitleexplain = "fantasy_points_vs_matches";
    } else if (currentIndex === 1) {
      temptitleexplain = "recent_performance";
    } else if (currentIndex === 2) {
      temptitleexplain = "matchups_bat";
    } else if (currentIndex === 3) {
      temptitleexplain = "demography_bat";
    } else if (currentIndex === 4) {
      if (selectedFilter3 === "venue") {
        temptitleexplain = "differential_exp_venue";
      } else if (selectedFilter3 === "opposition") {
        temptitleexplain = "differential_exp_opposition";
      } else if (selectedFilter3 === "form") {
        temptitleexplain = "differential_exp_form";
      }
    } else if (currentIndex === 5) {
      if (selectedFilter2 === "Overall") {
        temptitleexplain = "impact_index_overall_bat";
      } else if (selectedFilter2 === "Powerplay") {
        temptitleexplain = "impact_index_pp_bat";
      } else if (selectedFilter2 === "Middle") {
        temptitleexplain = "impact_index_middle_bat";
      } else if (selectedFilter2 === "Death") {
        temptitleexplain = "impact_index_death_bat";
      }
    } else {
      temptitleexplain = "Graph not relevant for Batter";
    }
  } else if (containsbowl(card.type)) {
    typeofplayer = "BOWLER";
    if (currentIndex === 0) {
      temptitleexplain = "fantasy_points_vs_matches";
    } else if (currentIndex === 1) {
      temptitleexplain = "recent_performance";
    } else if (currentIndex === 2) {
      temptitleexplain = "matchups_bowl";
    } else if (currentIndex === 3) {
      temptitleexplain = "demography_bowl";
    } else if (currentIndex === 4) {
      if (selectedFilter3 === "venue") {
        temptitleexplain = "differential_exp_venue";
      } else if (selectedFilter3 === "opposition") {
        temptitleexplain = "differential_exp_opposition";
      } else if (selectedFilter3 === "form") {
        temptitleexplain = "differential_exp_form";
      }
    } else if (currentIndex === 5) {
      if (selectedFilter2 === "Overall") {
        temptitleexplain = "impact_index_overall_bowl";
      } else if (selectedFilter2 === "Powerplay") {
        temptitleexplain = "impact_index_pp_bowl";
      } else if (selectedFilter2 === "Middle") {
        temptitleexplain = "impact_index_middle_bowl";
      } else if (selectedFilter2 === "Death") {
        temptitleexplain = "impact_index_death_bowl";
      }
    } else {
      temptitleexplain = "Graph not relevant for Bowler";
    }
  } else if (containsall(card.type)) {
    typeofplayer = "ALLROUNDER";
    if (currentIndex === 0) {
      temptitleexplain = "fantasy_points_vs_matches";
    } else if (currentIndex === 1) {
      temptitleexplain = "recent_performance";
    } else if (currentIndex === 2) {
      temptitleexplain = "matchups_bat";
    } else if (currentIndex === 3) {
      temptitleexplain = "demography_bat";
    } else if (currentIndex === 4) {
      if (selectedFilter3 === "venue") {
        temptitleexplain = "differential_exp_venue";
      } else if (selectedFilter3 === "opposition") {
        temptitleexplain = "differential_exp_opposition";
      } else if (selectedFilter3 === "form") {
        temptitleexplain = "differential_exp_form";
      }
    } else if (currentIndex === 5) {
      if (selectedFilter2 === "Overall") {
        temptitleexplain = "impact_index_overall_bat";
      } else if (selectedFilter2 === "Powerplay") {
        temptitleexplain = "impact_index_pp_bat";
      } else if (selectedFilter2 === "Middle") {
        temptitleexplain = "impact_index_middle_bat";
      } else if (selectedFilter2 === "Death") {
        temptitleexplain = "impact_index_death_bat";
      }
    }
  } else if (containswk(card.type)) {
    typeofplayer = "WICKETKEEPER";
    if (currentIndex === 0) {
      temptitleexplain = "fantasy_points_vs_matches";
    } else if (currentIndex === 1) {
      temptitleexplain = "recent_performance";
    } else if (currentIndex === 2) {
      temptitleexplain = "matchups_bat";
    } else if (currentIndex === 3) {
      temptitleexplain = "demography_bat";
    } else if (currentIndex === 4) {
      if (selectedFilter2 === "venue") {
        temptitleexplain = "differential_exp_venue";
      } else if (selectedFilter2 === "opposition") {
        temptitleexplain = "differential_exp_opposition";
      } else if (selectedFilter2 === "form") {
        temptitleexplain = "differential_exp_form";
      }
    } else if (currentIndex === 5) {
      if (selectedFilter3 === "Overall") {
        temptitleexplain = "impact_index_overall_bat";
      } else if (selectedFilter3 === "Powerplay") {
        temptitleexplain = "impact_index_pp_bat";
      } else if (selectedFilter3 === "Middle") {
        temptitleexplain = "impact_index_middle_bat";
      } else if (selectedFilter3 === "Death") {
        temptitleexplain = "impact_index_death_bat";
      }
    } else {
      temptitleexplain = "Graph not relevant for Batter";
    }
  } else {
    typeofplayer = "ALLROUNDER";
    if (currentIndex === 0) {
      temptitleexplain = "fantasy_points_vs_matches";
    } else if (currentIndex === 1) {
      temptitleexplain = "recent_performance";
    } else if (currentIndex === 2) {
      temptitleexplain = "matchups_bat";
    } else if (currentIndex === 3) {
      temptitleexplain = "demography_bat";
    } else if (currentIndex === 4) {
      if (selectedFilter3 === "venue") {
        temptitleexplain = "differential_exp_venue";
      } else if (selectedFilter3 === "opposition") {
        temptitleexplain = "differential_exp_opposition";
      } else if (selectedFilter3 === "form") {
        temptitleexplain = "differential_exp_form";
      }
    } else if (currentIndex === 5) {
      if (selectedFilter2 === "Overall") {
        temptitleexplain = "impact_index_overall_bat";
      } else if (selectedFilter2 === "Powerplay") {
        temptitleexplain = "impact_index_pp_bat";
      } else if (selectedFilter2 === "Middle") {
        temptitleexplain = "impact_index_middle_bat";
      } else if (selectedFilter2 === "Death") {
        temptitleexplain = "impact_index_death_bat";
      }
    }
  }

  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <div
          className="expanded-card-left"
          style={{
            width: "30%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            color: "white",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              width: "100%",
            }}
          >
            <div
              style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ fontSize: "32px", fontWeight: "bold" }}>
                {card.name}
              </div>
              <div style={{ fontSize: "14px", color: "gray" }}>
                {team.toUpperCase()}
              </div>
            </div>

            {/* Image */}
            <img
              className="display-expanded-card-team-logo"
              style={{
                width: "15%",
                height: "auto",
                objectFit: "contain",
              }}
              src={card.team_url}
              alt="Team"
            />
          </div>

          <div
            className="top-left"
            style={{
              display: "flex",
              height: "50%",
              flexDirection: "column",
              color: "white",
              position: "relative",
              backgroundImage: `url(${dream11background})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
              marginTop: -10,
              zIndex: -1,
              flex: "0.6",
            }}
          >
            <img
              className="display-card-expanded-player-image"
              src={card.img_url}
              alt="PLayer"
              onError={(e) => {
                e.currentTarget.src = defaultimg;
              }}
              style={{
                position: "absolute",
                left: "50%",
                transform: "translateX(-50%)",
              }}
            />

            <div className="display-card-overlay-section">
              <div className="card-overlay-row-display">
                <div
                  className="overlay-section"
                  style={{
                    borderTopLeftRadius: "15px",
                    borderBottomLeftRadius: "15px",
                    color: "green",
                  }}
                >
                  {parseFloat(card.points).toFixed(2)}
                  <div
                    style={{
                      fontSize: "8px",
                      marginBottom: "10px",
                      color: "white",
                    }}
                  >
                    EXPT PTS
                  </div>
                </div>

                <div className="overlay-section" style={{ color: "red" }}>
                  {card.cost}
                  <div
                    style={{
                      fontSize: "8px",
                      marginBottom: "10px",
                      color: "white",
                    }}
                  >
                    COST
                  </div>
                </div>

                <div
                  className="overlay-section"
                  style={{
                    borderTopRightRadius: "15px",
                    borderBottomRightRadius: "15px",
                    color: "gray",
                  }}
                >
                  {parseFloat(card.runs).toFixed()}
                  <div
                    style={{
                      fontSize: "8px",
                      marginBottom: "10px",
                      color: "white",
                    }}
                  >
                    EXPT RUNS
                  </div>
                </div>

                <div
                  className="overlay-section"
                  style={{
                    borderTopRightRadius: "15px",
                    borderBottomRightRadius: "15px",
                    color: "grey",
                  }}
                >
                  {parseFloat(card.boundaries).toFixed()}
                  <div
                    style={{
                      fontSize: "8px",
                      marginBottom: "10px",
                      color: "white",
                    }}
                  >
                    EXPT 4s & 6s
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
            className="bottom-left"
            style={{
              display: "flex",
              flexDirection: "column",
              height: "100%",
              flex: "0.40",
            }}
          >
            {/* AI Text Section */}
            <div
              className="ai-text"
              style={{
                flexGrow: 1,
                position: "relative",
                overflow: "hidden",
              }}
            >
              <Box
                sx={{
                  width: "100%",
                  maxHeight: 200,
                  padding: "16px",
                  justifyContent: "center",
                  alignItems: "stretch",
                  boxSizing: "border-box",
                  overflowY: "auto",
                  overflowX: "hidden",
                  marginTop: "25px",
                  scrollbarColor: "grey",
                  scrollbarWidth: "5px",
                }}
              >
                {playerdescription !== "" ? (
                  playerdescription
                ) : (
                  <>
                    <Skeleton
                      animation="pulse"
                      sx={{ bgcolor: "white", opacity: 0.8, height: "20px" }}
                    />
                    <Skeleton
                      animation="wave"
                      sx={{ bgcolor: "white", opacity: 0.8, height: "20px" }}
                    />
                    <Skeleton
                      animation="pulse"
                      sx={{ bgcolor: "white", opacity: 0.8, height: "20px" }}
                    />
                    <Skeleton
                      animation="wave"
                      sx={{ bgcolor: "white", opacity: 0.8, height: "20px" }}
                    />
                  </>
                )}
              </Box>
            </div>

            {/* SearchBar Section */}
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                marginTop: "50px",
              }}
            >
              <SearchBar
                suggestions={exampleQueries}
                feature_name={"query_answering"}
                player_name={card.name}
                date={matchDate}
                model={model}
                player_opponents={Object.keys(playerTeamMap).filter(player => playerTeamMap[player] !== playerTeamMap[card.name]).join(",")}
                player_type={card.type}
              />
            </div>
          </div>
        </div>

        <div
          className="expanded-card-right"
          style={{
            width: "70%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            color: "white",
            justifyContent: "space-around",
            alignItems: "center",
          }}
        >
          <div
            className="top-right"
            style={{
              width: "95%",
              height: "55%",
              backgroundColor: "black",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-evenly",
              marginBottom: "10px",
            }}
          >
            {/* <button className="filterbutton" onClick={() => setExpanded(false)}>
            &times;
          </button> */}

            <div
              className="quote-card"
              style={{ width: "100%", height: "30px" }}
            ></div>

            <div className="stats-div" style={{ width: "100%", height: "80%" }}>
              {/* <FilterButton /> */}

              {/* Header */}
              <div
                className="stats-div-header"
                style={{ width: "100%", height: "30px" }}
              >
                <div
                  onClick={handleLeftClick}
                  style={{
                    width: "0",
                    height: "0",
                    borderLeft: "10px solid transparent",
                    borderRight: "10px solid transparent",
                    borderBottom: "15px solid white",
                    cursor: "pointer",
                    transform: "rotate(270deg)",
                  }}
                ></div>

                <div
                  style={{
                    fontSize: "20px",
                    marginLeft: "17px",
                    marginRight: "17px",
                  }}
                >
                  {data[currentIndex].title}
                </div>

                <div
                  onClick={handleRightClick}
                  style={{
                    width: "0",
                    height: "0",
                    borderLeft: "10px solid transparent",
                    borderRight: "10px solid transparent",
                    borderBottom: "15px solid white",
                    cursor: "pointer",
                    transform: "rotate(90deg)",
                  }}
                ></div>
              </div>

              {/* Stats Column */}
              <div
                className="stats-div-screen"
                style={{
                  height: "100%",
                  width: "100%",
                  transition: "all 0.5s ease",
                }}
              >
                <button
                  className="closeButton"
                  onClick={() => setExpanded(false)}
                >
                  &times;
                </button>

                {(currentIndex === 0 ||
                  currentIndex === 1 ||
                  currentIndex === 2 ||
                  currentIndex === 3) && (
                  <div
                    style={{
                      width: "100%",
                      height: "30px",
                      top: "10px",
                      right: "15px",
                      display: "flex",
                      position: "relative",
                    }}
                  >
                    <FilterBar
                      filters={filters}
                      selected={selectedFilter}
                      onFilterChange={handleFilterChange}
                    />
                  </div>
                )}

                {currentIndex === 4 && (
                  <div
                    style={{
                      width: "100%",
                      height: "30px",
                      top: "10px",
                      right: "15px",
                      display: "flex",
                      position: "relative",
                    }}
                  >
                    <FilterBar
                      filters={filters3}
                      selected={selectedFilter3}
                      onFilterChange={handleFilterChange3}
                    />
                  </div>
                )}

                {currentIndex === 5 && (
                  <div
                    style={{
                      width: "100%",
                      height: "30px",
                      top: "10px",
                      right: "15px",
                      display: "flex",
                      position: "relative",
                    }}
                  >
                    <FilterBar
                      filters={filters2}
                      selected={selectedFilter2}
                      onFilterChange={handleFilterChange2}
                    />
                  </div>
                )}

                {currentIndex === 0 && (
                  <ResponsiveContainer width="90%" height={250}>
                    <BarChart
                      data={fantasygraphdata}
                    >
                      <XAxis
                        dataKey="date"
                        tick={{ fill: "grey", fontSize: 5 }}
                        tickLine={false}
                      />

                      <YAxis
                        axisLine={false}
                        tickLine={false}
                        tick={{ fill: "grey", fontSize: 7 }}
                        minTickGap={10}
                      />

                      <Tooltip
                        labelStyle={{
                          color: "#FA2433",
                          fontSize: "20px",
                          backgroundColor: "black",
                        }}
                        contentStyle={{
                          color: "#FA2433",
                          fontSize: "20px",
                          backgroundColor: "black",
                        }}
                      />

                      <Bar
                        dataKey="value"
                        fill={"#FA2433"}
                        radius={[5, 5, 0, 0]}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                )}

                {currentIndex === 1 && (
                  <div
                    style={{
                      width: "100%",
                      height: "85%",
                      display: "flex",
                      justifyContent: "space-around",
                      alignItems: "center",
                    }}
                  >
                    <div
                      style={{ alignItems: "center", alignContent: "center" }}
                    >
                      <CircularProgress percentage={percentages[0]} />
                      <div
                        style={{
                          display: "flex",
                          fontSize: "15px",
                          color: "white",
                          marginTop: "10px",
                          justifyContent: "space-evenly",
                        }}
                      >
                        OVERALL
                      </div>
                    </div>

                    <div>
                      <CircularProgress percentage={percentages[1]} />
                      <div
                        style={{
                          display: "flex",
                          fontSize: "15px",
                          color: "white",
                          marginTop: "10px",
                          justifyContent: "space-evenly",
                        }}
                      >
                        Vs TEAM
                      </div>
                    </div>

                    <div>
                      <CircularProgress percentage={percentages[2]} />
                      <div
                        style={{
                          display: "flex",
                          fontSize: "15px",
                          color: "white",
                          marginTop: "10px",
                          justifyContent: "space-evenly",
                        }}
                      >
                        VENUE
                      </div>
                    </div>
                  </div>
                )}

                {currentIndex === 2 && (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "center",
                      justifyItems: "center",
                      alignContent: "center",
                      width: "100%",
                      height: "70%",
                      overflowY: "scroll",
                      marginTop: "10px",
                    }}
                  >
                    <MatchupsComponent
                      key={card.name}
                      matchupsdata={matchupsdata}
                    />

                    <div></div>
                  </div>
                )}

                {currentIndex === 3 && (
                  <div
                    style={{
                      width: "100%",
                      height: "85%",
                      backgroundColor: "#1A1A1A",
                    }}
                  >
                    <PieChart width={500} height={200}>
                      <Pie
                        data={newpiedata}
                        dataKey="value"
                        nameKey="name"
                        outerRadius={90}
                      >
                        {data.map((entry, index) => (
                          <Cell
                            key={`cell-${index}`}
                            fill={COLORS[index % COLORS.length]}
                          />
                        ))}
                      </Pie>
                      <Tooltip
                        labelStyle={{ fontSize: "10px" }}
                        contentStyle={{ fontSize: "10px" }}
                      />
                      <Legend
                        width={150}
                        layout="vertical"
                        verticalAlign="middle"
                        align="right"
                        wrapperStyle={{ fontSize: "10px" }}
                      />
                    </PieChart>
                  </div>
                )}

                {currentIndex === 4 && (
                  <div
                    style={{
                      width: "100%",
                      height: "85%",
                      backgroundColor: "#1A1A1A",
                    }}
                  >
                    <VenueGraph
                      selected={selectedFilter3}
                      maindata={venuechartdata}
                    />
                  </div>
                )}

                {/* {currentIndex === 5 && (
                <div
                  style={{
                    width: "100%",
                    height: "85%",
                    backgroundColor: "#1A1A1A",
                  }}
                >
                  <VenueGraph />
                </div>
              )} */}

                {currentIndex === 5 && (
                  <div
                    style={{
                      width: "100%",
                      height: "85%",
                      backgroundColor: "#1A1A1A",
                    }}
                  >
                    <ImpactChart
                      battingStats={impactdata}
                      filter={selectedFilter2}
                    />
                  </div>
                )}

                <div
                  style={{
                    width: "100%",
                    height: "25px",
                    bottom: "10px",
                    display: "flex",
                    position: "relative",
                    zIndex: "10",
                    justifyContent: "end",
                    paddingRight: "10px",
                    paddingBottom: "2px",
                  }}
                >
                  <ExplainGraphButton
                    title={temptitleexplain}
                    explaindate={explaindate}
                    opponents={opponents}
                    typeofplayer={typeofplayer}
                    player_name={card.name}
                    model={model}
                  />
                </div>
              </div>
            </div>
          </div>

          <div
            className="bottom-right"
            style={{
              width: "95%",
              height: "45%",
              backgroundColor: "black",
              display: "flex",
              justifyContent: "space-around",
              justifyItems: "center",
              alignItems: "center",
            }}
          >
            <div className="type-stats">
              {/* Header */}
              <div
                className="stats-div-header"
                style={{ width: "100%", height: "30px" }}
              >
                <div
                  onClick={handleLeftClickTypes}
                  style={{
                    width: "0",
                    height: "0",
                    borderLeft: "10px solid transparent",
                    borderRight: "10px solid transparent",
                    borderBottom: "15px solid white",
                    cursor: "pointer",
                    transform: "rotate(270deg)",
                  }}
                ></div>

                <div
                  style={{
                    fontSize: "15px",
                    marginLeft: "17px",
                    marginRight: "17px",
                    fontWeight: "bold",
                  }}
                >
                  {typeData_2[currentIndexTypes].title}
                </div>

                <div
                  onClick={handleRightClickTypes}
                  style={{
                    width: "0",
                    height: "0",
                    borderLeft: "10px solid transparent",
                    borderRight: "10px solid transparent",
                    borderBottom: "15px solid white",
                    cursor: "pointer",
                    transform: "rotate(90deg)",
                  }}
                ></div>
              </div>

              {/* Stats Column */}
              <div
                className="grid-container"
                style={{ width: "100%", height: "90%" }}
              >
                {typeData_2[currentIndexTypes].stats.map((stat, index) => (
                  <div className="grid-item" key={index}>
                    {stat.value}
                    <div style={{ color: "white", fontSize: "9px" }}>
                      {stat.key}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div
              style={{ width: "55%", backgroundColor: "white", height: "90%" }}
            >
              <div
                style={{
                  width: "100%",
                  height: "30px",
                  backgroundColor: "black",
                  border: "2px solid white",
                  textAlign: "center",
                  alignContent: "center",
                  fontWeight: "bold",
                }}
              >
                PLAYER PROFILE
              </div>

              <div
                style={{
                  display: "flex",
                  width: "100%",
                  maxHeight: "90%",
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: "#1A1A1A",
                }}
              >
                <RadarChart numbers={radarnumbers} />

                <ExplainGraphButton
                  title={
                    card.type === "BAT"
                      ? "spider_chart_bat"
                      : card.type === "BOWL"
                      ? "spider_chart_bowl"
                      : "spider_chart_all"
                  }
                  player_name={card.name}
                  explaindate={explaindate}
                  model={model}
                  opponents={opponents}
                  typeofplayer={typeofplayer}
                />
              </div>
            </div>
          </div>
        </div>
      </Box>
    </Modal>
  );
};

const MatchupsComponent: React.FC<{ matchupsdata: any }> = ({
  matchupsdata,
}) => {
  const stats = matchupsdata["stats"];

  return (
    <>
      {Object.keys(stats).map((playerName, index) => {
        const playerStats = stats[playerName];

        return playerStats !== null ? (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent: "space-around",
              fontSize: "9px",
              backgroundColor: "#333333",
              width: "90%",
              height: "25%",
              borderRadius: "10px",
              marginBottom: "10px",
            }}
          >
            {/* Player Name and Image */}
            <div
              style={{
                width: "20%",
                height: "100%",
                display: "flex",
              }}
            >
              <div style={{ width: "50%", height: "100%" }}>
                <img
                  src={defaultimg}
                  alt="Player"
                  onError={(e) => {
                    e.currentTarget.src = defaultimg;
                  }}
                  style={{
                    width: "100%",
                    height: "100%",
                    position: "relative",
                    objectFit: "contain",
                  }}
                />
              </div>
              <div
                style={{
                  fontSize: "12px",
                  width: "50%",
                  color: "white",
                  alignContent: "center",
                }}
              >
                {playerName.trim()}
              </div>
            </div>

            <div
              style={{
                width: "2px",
                height: "100%",
                backgroundColor: "white",
                marginLeft: "5px",
              }}
            ></div>

            {/* Stats */}
            <div
              style={{
                width: "20%",
                height: "100%",
                color: "white",
                justifyItems: "center",
                alignContent: "center",
                fontSize: "11px",
              }}
            >
              BALLS
              <div style={{ color: "#FA2433" }}>
                {/* {playerStats?.balls ?? "N/A"} */}
                {playerStats["previous_runs"] !== null &&
                playerStats["previous_runs"] !== 0 &&
                playerStats["previous_avg_strike_rate"] !== null &&
                playerStats["previous_avg_strike_rate"] !== 0
                  ? Math.round(
                      (playerStats["previous_runs"] * 100) /
                        playerStats["previous_avg_strike_rate"]
                    )
                  : 0}
              </div>
            </div>

            <div
              style={{
                width: "2px",
                height: "100%",
                backgroundColor: "white",
              }}
            ></div>

            <div
              style={{
                width: "20%",
                height: "100%",
                color: "white",
                justifyItems: "center",
                alignContent: "center",
                fontSize: "11px",
              }}
            >
              RUNS
              <div style={{ color: "#FA2433" }}>
                {playerStats !== null ? playerStats["previous_runs"] : "N/A"}
              </div>
            </div>

            <div
              style={{
                width: "2px",
                height: "100%",
                backgroundColor: "white",
              }}
            ></div>

            <div
              style={{
                width: "20%",
                height: "100%",
                color: "white",
                justifyItems: "center",
                alignContent: "center",
                fontSize: "11px",
              }}
            >
              OUT
              <div style={{ color: "#FA2433" }}>
                {playerStats !== null ? playerStats["previous_wickets"] : "N/A"}
              </div>
            </div>

            <div
              style={{
                width: "2px",
                height: "100%",
                backgroundColor: "white",
              }}
            ></div>

            <div
              style={{
                width: "20%",
                height: "100%",
                color: "white",
                justifyItems: "center",
                alignContent: "center",
                fontSize: "11px",
              }}
            >
              STRIKE RATE
              <div style={{ color: "#FA2433" }}>
                {playerStats !== null
                  ? playerStats["previous_avg_strike_rate"].toFixed(2)
                  : "N/A"}
              </div>
            </div>
          </div>
        ) : (
          <div key={index}></div>
        );
      })}
    </>
  );
};

export default DisplayCardExpanded;
