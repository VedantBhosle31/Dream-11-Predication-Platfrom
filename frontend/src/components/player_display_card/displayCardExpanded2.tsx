import React, { useState, useRef, useEffect } from "react"; //
import rcblogo from "../../assets/images/rcb_logo.png";
import bccilogo from "../../assets/images/bcci_logo.png";
import dream11background from "../../assets/images/dream11bg.png";
import "./displayCard2.css";
import RadarChart from "../radar_chart/radar";
import FormBar from "../player_form/formbar";
import SearchBar from "../search_bar/searchbar";
import FantasyPointsChart from "../points_chart/pointschart";
import { Box, Modal, Skeleton, Typography } from "@mui/material";
import { ChartContainer } from "@mui/x-charts/ChartContainer";
// import { BarChart, BarPlot } from "@mui/x-charts/BarChart";

import {
  Bar,
  BarChart,
  CartesianGrid,
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
import FilterButton from "../filterButton/filterButton";
import FilterBar from "../filterBar/filterBar";

const piedata = [
  { name: "0", value: 400 },
  { name: "1", value: 300 },
  { name: "2", value: 300 },
  { name: "4", value: 200 },
  { name: "5", value: 100 },
  { name: "6", value: 50 },
];

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#6366F1",
  "#FA2433",
];

const exampleQueries = [
  "Recent Form of Virat Kohli",
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

const datatitles = [
  "FANTASY POINTS VS MATCHES",
  "RECENT PERFORMANCE",
  "MATCHUPS",
  "PLAYER DEMOGRAPHY",
];

const graphdata = [
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

const yValues = graphdata.map((data) => data.value);

yValues.sort((a, b) => a - b);

export interface Matchups {
  name: string;
  balls: string;
  runs: string;
  out: string;
  strikerate: string;
}

const MatchupsData: Matchups[] = [
  {
    name: "JOfra Archer",
    balls: "150",
    runs: "60",
    out: "3",
    strikerate: "115",
  },
  {
    name: "JOfra Archer",
    balls: "150",
    runs: "60",
    out: "3",
    strikerate: "115",
  },
  {
    name: "JOfra Archer",
    balls: "150",
    runs: "60",
    out: "3",
    strikerate: "115",
  },
];

interface DisplayCardExpandedProps {
  containerRef: React.RefObject<HTMLDivElement>;
  isExpanded: boolean;
  setExpanded: React.Dispatch<React.SetStateAction<boolean>>;
  playerImage: string;
  card: {
    name: string;
    country: string;
    type: string;
    cvc: string;
  };
  handleLeftClick: () => void;
  handleRightClick: () => void;
  handleRightClickTypes: () => void;
  handleLeftClickTypes: () => void;
  data: {
    title: string;
    stats: { key: string; value: string }[];
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
  filters: string[];
  handleFilterChange: (filter: string) => void;
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
  filters,
  handleFilterChange,
}) => (
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
              ROYAL CHALLENGERS BANGLORE
            </div>
          </div>

          {/* Image */}
          <img
            className="display-expanded-card-team-logo"
            style={{
              width: "15%",
              height: "auto",
              objectFit: "contain", // Ensures the image scales properly
            }}
            src={card.country === "INDIA" ? bccilogo : rcblogo}
            alt="Player"
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
            src={playerImage}
            alt="Player"
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
                86
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
                50
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
                157
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
                157
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
                height: "100%",
                padding: "16px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "stretch",
                gap: "8px",
                boxSizing: "border-box",
              }}
            >
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
            <SearchBar suggestions={exampleQueries} onSearch={handleSearch} />
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


              
              <div style={{width:"100%", height:"30px", top: "10px", right: "15px",display:"flex", position: "relative"}}>
              <FilterBar
                filters={filters}
                selected={selectedFilter}
                onFilterChange={handleFilterChange}
              />
              </div>

              {currentIndex === 0 && (
                <ResponsiveContainer width="90%" height={250}>
                  <BarChart
                    data={graphdata}
                    //   width={600}
                    //   height={30}
                    // margin={{ top: 20, right: 30, bottom: 50, left: 50 }}
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
                    height: "100%",
                    display: "flex",
                    justifyContent: "space-around",
                    alignItems: "center",
                  }}
                >
                  <div style={{ alignItems: "center", alignContent: "center" }}>
                    <CircularProgress percentage={75} />
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
                    <CircularProgress percentage={60} />
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
                    <CircularProgress percentage={85} />
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
                    justifyContent: "center",
                    alignItems: "center",
                    justifyItems: "center",
                    width: "100%",
                    height: "100%",
                  }}
                >
                  {MatchupsData.map((player, index) => (
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-evenly",
                        fontSize: "10px",
                        backgroundColor: "#333333",
                        width: "90%",
                        height: "20%",
                        borderRadius: "10px",
                        marginTop: "5px",
                      }}
                    >
                      <div
                        style={{
                          width: "20%",
                          height: "100%",
                          display: "flex",
                        }}
                      >
                        <div style={{ width: "50%", height: "100%" }}>
                          <img
                            src={playerImage}
                            alt="player"
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
                            fontSize: "15px",
                            width: "50%",
                            color: "white",
                            alignContent: "center",
                          }}
                        >
                          {player.name}
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

                      <div
                        style={{
                          width: "20%",
                          height: "100%",
                          color: "white",
                          justifyItems: "center",
                          alignContent: "center",
                          fontSize: "15px",
                        }}
                      >
                        BALLS
                        <div style={{ color: "#FA2433" }}>{player.balls}</div>
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
                          fontSize: "15px",
                        }}
                      >
                        RUNS
                        <div style={{ color: "#FA2433" }}>{player.runs}</div>
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
                          fontSize: "15px",
                        }}
                      >
                        OUT
                        <div style={{ color: "#FA2433" }}>{player.out}</div>
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
                          fontSize: "15px",
                        }}
                      >
                        STRIKE RATE
                        <div style={{ color: "#FA2433" }}>
                          {player.strikerate}
                        </div>
                      </div>
                    </div>
                  ))}

                  <div></div>
                </div>
              )}

              {currentIndex === 3 && (
                <div
                  style={{
                    width: "100%",
                    height: "90%",
                    backgroundColor: "#1A1A1A",
                  }}
                >
                  <PieChart width={500} height={200}>
                    <Pie
                      data={piedata}
                      dataKey="value"
                      nameKey="name"
                      // cx="50%"
                      // cy="50%"
                      outerRadius={90}
                      //   label
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
                    height: "90%",
                    backgroundColor: "#1A1A1A",
                  }}
                >
                  <FantasyPointsChart />
                </div>
              )}

              {currentIndex === 5 && (
                <div
                  style={{
                    width: "100%",
                    height: "90%",
                    backgroundColor: "#1A1A1A",
                  }}
                >
                  <FantasyPointsChart />
                </div>
              )}



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
            <div className="grid-container" style={{ width: "100%", height: "20%" }}>
              {typeData_2[currentIndexTypes].stats.map((stat, index) => (
                <div className="grid-item" key={index}>
                  {stat.value}
                  <div style={{ color: "white", fontSize: "10px" }}>
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
                height: "90%",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "#1A1A1A",
              }}
            >
              <RadarChart />

            </div>
          </div>
        </div>
      </div>
    </Box>
  </Modal>
);

export default DisplayCardExpanded;