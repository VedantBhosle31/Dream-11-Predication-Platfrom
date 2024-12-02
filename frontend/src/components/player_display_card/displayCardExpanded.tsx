// import React , { useState, useRef, useEffect } from "react";//
// import rcblogo from "../../assets/images/rcb_logo.png";
// import bccilogo from "../../assets/images/bcci_logo.png";
// import dream11background from "../../assets/images/dream11bg.png";
// import "./displayCard.css";
// import RadarChart from "../radar_chart/radar";
// import FormBar from "../player_form/formbar";
// import SearchBar from "../search_bar/searchbar";
// import VenueGraph from "../points_chart/pointschart";

// interface DisplayCardExpandedProps {
//     containerRef: React.RefObject<HTMLDivElement>;
//     isExpanded: boolean;
//     setExpanded: React.Dispatch<React.SetStateAction<boolean>>;
//     playerImage: string;
//     card: {
//       name: string;
//       country: string;
//       type: string;
//       cvc: string;
//     };
//     handleLeftClick: () => void;
//     handleRightClick: () => void;
//     data: {
//       title: string;
//       stats: { key: string; value: string }[];
//     }[];
//     currentIndex: number;
//     suggestions: string[];
//     handleSearch: (search: string) => void;
//   }


// const DisplayCardExpanded : React.FC<DisplayCardExpandedProps> = ({
//   containerRef,
//   isExpanded,
//   setExpanded,
//   playerImage,
//   card,
//   handleLeftClick,
//   handleRightClick,
//   data,
//   currentIndex,
//   suggestions,
//   handleSearch,
// }) => (
//   <div
//     ref={containerRef}
//     className="display-card-expanded"
//     style={{
//       position: isExpanded ? "absolute" : "relative",
//       transition: "all 0.7s ease",
//     }}
//   >
//     <button className="closeButton" onClick={() => setExpanded(false)}>
//       &times;
//     </button>
//     <img src={dream11background} alt="dream11bg" className="dream11bg" />

//     <div className="display-card-top-left">
//       <div style={{ height: "100%" }}>
//         <img
//           className="display-card-expanded-player-image"
//           src={playerImage}
//           alt="Player"
//         />
//         <div className="display-card-expanded-overlay">{card.name}</div>
//       </div>

//       <div className="display-card-expanded-points">
//         <div>
//           207
//           <div style={{ fontSize: 20, textAlign: "center" }}>PTS</div>
//         </div>

//         <div
//           style={{
//             width: "80%",
//             height: "30%",
//             alignItems: "center",
//             justifyItems: "center",
//           }}
//         >
//           <img
//             className="display-expanded-card-team-logo"
//             src={card.country === "INDIA" ? bccilogo : rcblogo}
//             alt="Player"
//           />
//           <div style={{ fontSize: 20, textAlign: "center" }}>
//             {card.country}
//           </div>
//         </div>

//         <div style={{ fontSize: 17 }}>{card.type}</div>
//       </div>

//       {card.cvc === "C" && (
//         <div
//           className="display-card-expanded-c"
//           style={{ display: "flex" }}
//         >
//           C
//         </div>
//       )}

//       {card.cvc === "VC" && (
//         <div
//           className="display-card-expanded-vc"
//           style={{ display: "flex" }}
//         >
//           VC
//         </div>
//       )}
//     </div>

//     <div className="display-card-bottom-left">
//       <div
//         style={{
//           height: "100%",
//           width: "70%",
//           display: "flex",
//           flexDirection: "column",
//         }}
//       >
//         <FormBar hotness={90} />
        
//         <RadarChart numbers={[]} />
//         <div
//           style={{
//             fontFamily: "Montserrat",
//             fontWeight: "bolder",
//             fontSize: "24px",
//             color: "white",
//             width: "100%",
//             textAlign: "center",
//           }}
//         >
//           PLAYER PROFILE
//         </div>
//       </div>

//       <div className="stats">
//         {/* Header */}
//         <div
//           style={{
//             display: "flex",
//             justifyContent: "space-between",
//             marginBottom: "10px",
//             width: "100%",
//           }}
//         >
//           <div
//             onClick={handleLeftClick}
//             style={{
//               width: "0",
//               height: "0",
//               borderLeft: "10px solid transparent",
//               borderRight: "10px solid transparent",
//               borderBottom: "15px solid black",
//               cursor: "pointer",
//               transform: "rotate(270deg)",
//             }}
//           ></div>

//           <div
//             style={{
//               fontSize: "10px",
//               marginLeft: "17px",
//               marginRight: "17px",
//             }}
//           >
//             {data[currentIndex].title}
//           </div>

//           <div
//             onClick={handleRightClick}
//             style={{
//               width: "0",
//               height: "0",
//               borderLeft: "10px solid transparent",
//               borderRight: "10px solid transparent",
//               borderBottom: "15px solid black",
//               cursor: "pointer",
//               transform: "rotate(90deg)",
//             }}
//           ></div>
//         </div>

//         {/* Stats Column */}
//         <div style={{ height: "70%", width: "100%" }}>
//           {data[currentIndex].stats.map((stat, index) => (
//             <div
//               key={index}
//               style={{
//                 display: "flex",
//                 justifyContent: "space-between",
//                 paddingBottom: "14px",
//                 height: "5%",
//                 width: "100%",
//               }}
//             >
//               <div style={{ fontSize: "12px", color: "gray" }}>
//                 {stat.key}
//               </div>
//               <div style={{ fontSize: "12px" }}>{stat.value}</div>
//             </div>
//           ))}
//         </div>
//       </div>
//     </div>

//     <div className="display-card-top-right">
//       <SearchBar suggestions={suggestions} onSearch={handleSearch} />
//       {/* <VenueGraph /> */}
//       <div
//         style={{
//           width: "80%",
//           height: "2px",
//           backgroundColor: "white",
//         }}
//       ></div>
//     </div>

//     <div className="display-card-bottom-right">
//       <div
//         style={{
//           display: "flex",
//           width: "90%",
//           height: "20%",
//           justifyContent: "space-evenly",
//         }}
//       >
//         <div className="quote-card-1"></div>
//         <div className="quote-card-1"></div>
//       </div>

//       <div
//         style={{
//           border: "2px solid white",
//           width: "80%",
//           height: "70%",
//         }}
//       ></div>
//     </div>
//   </div>
// );

// export default DisplayCardExpanded;

export {}