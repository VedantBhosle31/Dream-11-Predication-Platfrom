import React , { useState, useRef, useEffect } from "react";
import playerImage from "../../assets/images/virat_kohli.png"; // Replace with your player image
import milogo from "../../assets/images/mumbai_indians.png";
import rcblogo from "../../assets/images/rcb_logo.png";
import bccilogo from "../../assets/images/bcci_logo.png";
import dream11background from "../../assets/images/dream11bg.png";
import "./displayCard.css";
import RadarChart from "../radar_chart/radar";
import FormBar from "../player_form/formbar";
import SearchBar from "../search_bar/searchbar";
import FantasyPointsChart from "../points_chart/pointschart";
// import RadarChartComponent from "../radar_chart/radar"


export interface DisplayCardData {
    id: string;
    name: string;
    type: string;
    team: string;
    points:  string;
    cost: string;
    score: string;
    runs: string;
    average: string;
    strike_rate : string;
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

const DisplayScreen: React.FC = () => {

    const DisplayCards: DisplayCardData[] = [
        {
          id: "1", name: "FAF DU PLESSIS", type: "BATSMAN", team: "RCB", points: "207", cost: "12", score: "89",
          runs: "199",
          average: "49",
          strike_rate: "120",
          cvc: "VC",
          country: "SOUTH AFRICA"
        },
        {
          id: "2", name: "VIRAT KOHLI", type: "BATSMAN", team: "RCB", points: "207", cost: "12", score: "89",
          runs: "299",
          average: "59",
          strike_rate: "140",
          cvc: "C",
          country: "INDIA"
        },
        {
          id: "3", name: "GLENN MAXWELL", type: "ALL-ROUNDER", team: "RCB", points: "207", cost: "12", score: "89",
          runs: "150",
          average: "39",
          strike_rate: "135",
          cvc: "",
          country: "AUSTRALIA"
        },
    ];

    

    return (
        <div className="main-display">
            <div className="display-container">
                {DisplayCards.map((card) => (
                    <DisplayCard key={card.id} card={card}/>
                ))}
            </div>
        </div>
    )
}

const DisplayCard: React.FC<{
    card: DisplayCardData;
  }> = ({ card }) => {

    const containerRef = useRef<HTMLDivElement | null>(null);

    var [isExpanded, setExpanded] = useState(false);

    // Detect clicks outside the container to reset expanded card
    useEffect(() => {
      const handleClickOutside = (event: MouseEvent) => {
        if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
          setExpanded(false); // Reset to initial state
        }
      };
      
      // Add event listener for clicks outside
      document.addEventListener('mousedown', handleClickOutside);
      
      // Clean up the event listener when the component unmounts
      
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }, []);


    const data: Stats[] = [
      { title: 'BATTING', stats: [{ key: 'INNINGS', value: '244' }, { key: 'AGGREGATE', value: '8004' }, { key: 'HIGHEST SCORE', value: '113' }, { key: 'AVERAGE', value: '38.67' }, { key: 'FIFTYS', value: '55' }, { key: 'HUNDREDS', value: '8' }, { key: 'DUCKS', value: '10' }, { key: 'FOURS', value: '705' }, { key: 'SIXES', value: '272' },] },
      { title: 'BOWLING', stats: [{ key: 'X', value: '10' }, { key: 'Y', value: '20' }, { key: 'Z', value: '30' }] },
      { title: 'FIELDING', stats: [{ key: 'P', value: '100' }, { key: 'Q', value: '200' }, { key: 'R', value: '300' }] },
    ];

    const [currentIndex, setCurrentIndex] = useState(0);

    const handleLeftClick = () => {
      setCurrentIndex((prev) => (prev === 0 ? data.length - 1 : prev - 1));
    };
  
    const handleRightClick = () => {
      setCurrentIndex((prev) => (prev === data.length - 1 ? 0 : prev + 1));
    };

    const suggestions = ["ReactJS", "TypeScript", "React Native", "JavaScript", "Node.js"];
    
    const handleSearch = (query: string) => {
      console.log("Search Query:", query);
      alert(`You searched for: ${query}`);
    };

    return (
      
      !isExpanded ? 
      <div ref={containerRef} className={`display-card ${card.cvc === "C" ? "big" : ""}`}>
        
        <div className="background-overlay"></div>

        <div className="display-card-overlay">
          {card.name}

          <div className="display-card-overlay-row">
            <div className="overlay-row-section" style={{borderTopLeftRadius: "15px", borderBottomLeftRadius: "15px"}}>
                <div style={{fontSize: "13px", marginBottom: "10px"}}>
                    RUNS
                </div>
                {card.runs}
            </div>
            {/* <div className="divider"></div> */}
            <div className="overlay-row-section">
                <div style={{fontSize: "13px", marginBottom: "10px"}}>
                    AVERAGE
                </div>
                {card.average}
            </div>
            {/* <div className="divider"></div> */}
            <div className="overlay-row-section" style={{borderTopRightRadius: "15px", borderBottomRightRadius: "15px"}}>
                <div style={{fontSize: "13px", marginBottom: "10px"}}>
                    STRIKE RATE
                </div>
                {card.strike_rate}
            </div>
          </div>
        </div>
        
        <div className="display-card-points">
  
          <div>
            207
            <div style={{fontSize: 20}}>
              PTS
            </div>
          </div>
  
          
  
          <img className="display-card-team-logo" src={card.team === "RCB" ? rcblogo : milogo} alt="Player" />
  
          <div style={{fontSize: 13}}>
            {card.type}
          </div>
  
        </div>

        
        <button 
          className="info-button" 
          onClick={() => setExpanded(true)}
          
          aria-label="Info Button"
          >
            i
        </button>
        
        

        {(card.cvc === "C" && 
        <div className="display-card-c">
          C
        </div>)}

        {(card.cvc === "VC" && 
        <div className="display-card-vc">
          VC
        </div>)}

        {/* {( (card.cvc === "C" || card.cvc === "VC") && <div className="display-card-cvc">
          {( card.cvc === "C" ? "C" : (card.cvc === "VC" ? "VC" : "") )}
        </div>)} */}
        
        <img className="display-card-image" src={playerImage} alt="Player" />
  
      </div> : 
      
      <div ref={containerRef} className="display-card-expanded" style={{position: isExpanded ? 'absolute' : 'relative', transition: 'all 0.5s ease'}}>
        <button className="closeButton" onClick={() => setExpanded(false)}>
          &times;
        </button>
        <img src={dream11background} alt="dream11bg" className="dream11bg"/>

        <div className="display-card-top-left">

          <div style={{height: "100%"}}>
            <img className="display-card-expanded-player-image" src={playerImage} alt="Player" />
            <div className="display-card-expanded-overlay">
              {card.name}
            </div>
          </div>
          
          <div className="display-card-expanded-points">

            <div>
              207
              <div style={{fontSize: 20, textAlign: "center"}}>
                PTS
              </div>
            </div>

            <div style={{width: "80%", height: "30%", alignItems: "center", justifyItems: "center"}}>
              <img className="display-expanded-card-team-logo" src={card.country === "INDIA" ? bccilogo : rcblogo} alt="Player" />
              <div style={{fontSize: 20, textAlign: "center"}}>
                {card.country}
              </div>
            </div>

            
            
            <div style={{fontSize: 17}}>
              {card.type}
            </div>

          </div>

          {(card.cvc === "C" && 
          <div className="display-card-expanded-c" style={{display: "flex"}}>
            C
          </div>)}
          
          {(card.cvc === "VC" && 
          <div className="display-card-expanded-vc" style={{display: "flex"}}>
            VC
          </div>)}

          

        </div>

        <div className="display-card-bottom-left">

          <div style={{height: "100%", width: "70%", display: "flex", flexDirection: "column"}}>
            <FormBar hotness={90} />
            <RadarChart />
            <div style={{fontFamily: "Montserrat", fontWeight: "bolder", fontSize: "24px", color: "white", width: "100%", textAlign: "center"}}>
              PLAYER PROFILE
            </div>
          </div>

          <div className="stats">

            {/* Header */}
            <div style={{ display: 'flex', justifyContent: "space-between", marginBottom: '10px', width: "100%"}}>
              <div
              onClick={handleLeftClick}
              style={{
                width: '0',
                height: '0',
                borderLeft: '10px solid transparent',
                borderRight: '10px solid transparent',
                borderBottom: '15px solid black',
                cursor: 'pointer',
                transform: 'rotate(270deg)',
              }}
              ></div>
              
              <div style={{fontSize: "10px", marginLeft: "17px", marginRight: "17px"}}>
                {data[currentIndex].title}
              </div>
              
              <div
              onClick={handleRightClick}
              style={{
                width: '0',
                height: '0',
                borderLeft: '10px solid transparent',
                borderRight: '10px solid transparent',
                borderBottom: '15px solid black',
                cursor: 'pointer',
                transform: 'rotate(90deg)',
              }}
            ></div>
            </div>
            
            {/* Stats Column */}
            <div style={{height: "70%", width: "100%"}}>
              {data[currentIndex].stats.map((stat, index) => (
                <div key={index} style={{ display: 'flex', justifyContent: "space-between", paddingBottom: '14px', height: "5%", width: "100%"}}>
                  <div style={{ fontSize: '12px', color: "gray"}}>{stat.key}</div>
                  <div style={{ fontSize: '12px' }}>{stat.value}</div>
                </div>
              ))}
            </div>

         </div>

        </div>

        <div className="display-card-top-right">
          <SearchBar suggestions={suggestions} onSearch={handleSearch} />
          <FantasyPointsChart />
          <div style={{width: "80%", height: "2px", backgroundColor: "white"}}></div>
        </div>

        <div className="display-card-bottom-right">
          <div style={{display: "flex", width: "90%", height: "20%", justifyContent: "space-evenly"}}>
            <div className="quote-card-1"></div>
            <div className="quote-card-1"></div>
          </div>

          <div style={{border:"2px solid white", width: "80%", height: "70%"}}>

          </div>          

        </div>

        

      </div>
    );
  };

export default DisplayScreen;
