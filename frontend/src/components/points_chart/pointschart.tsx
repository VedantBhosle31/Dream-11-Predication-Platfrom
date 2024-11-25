// FantasyPointsChart.tsx
import React, { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart, Label } from "recharts";

interface ChartData {
    match: string;
    fantasyPoints: number;
    playerScore: number;
    runRate: number;
}

const data: ChartData[] = [
    {
        match: "vs AUS", fantasyPoints: 120,
        playerScore: 80,
        runRate: 169.2
    },
    {
        match: "vs SA", fantasyPoints: 140,
        playerScore: 100,
        runRate: 150
    },
    {
        match: "vs BAN", fantasyPoints: 110,
        playerScore: 90,
        runRate: 132.8
    },
    {
        match: "vs WI", fantasyPoints: 130,
        playerScore: 110,
        runRate: 120.8
    },
    {
        match: "vs PAK", fantasyPoints: 150,
        playerScore: 120,
        runRate: 167.9
    },
  ];

const FantasyPointsChart: React.FC = () => {
    const [selectedQuery, setSelectedQuery] = useState<string>("fantasyPoints");

    // Handle query change
    const handleQueryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      setSelectedQuery(event.target.value);
    };

    const queryColors: { [key: string]: string } = {
        fantasyPoints: "#3498db", // Blue for Fantasy Points
        playerScore: "#2ecc71",   // Green for Player Score
        runRate: "#e74c3c",       // Red for Run Rate
    };

  return (
    <div style={{ display: "flex", flexDirection: "column", width: "62%", height: "70%", marginTop: "20px", alignContent: "space-between" }}>

        {/* Dropdown for selecting the query */}
      <div style={{ display: "flex", marginBottom: "20px", width: "100%", height: "20px", fontSize: "20px", alignItems: "center", color: "black"}}>
        <select 
        value={selectedQuery} 
        onChange={handleQueryChange} 
        style={{
            width: "100%",
            height: "50px",
            fontSize: "35px",
            padding: "5px",
            borderRadius: "5px",
            backgroundColor: "transparent",
            border: "none",
            color: "white", // Selected value color
            appearance: "none", // Optional: For consistent cross-browser styling
            WebkitAppearance: "none",
            MozAppearance: "none",
            textAlign: "center",
            fontFamily: "Montserrat"
          }}
        >
          <option value="fantasyPoints" style={{color: "black",backgroundColor: "white",}}>Fantasy Points</option>
          <option value="playerScore" style={{color: "black",backgroundColor: "white",}}>Player Score</option>
          <option value="runRate" style={{color: "black",backgroundColor: "white",}}>Run Rate</option>
        </select>
      </div>

      <div style={{display: "flex", width: "100%", height: "65%", justifyContent: "center", alignItems: "center", marginTop: "20px"}}>
      <ResponsiveContainer width={"80%"} height={"100%"}>
        <AreaChart data={data}>
          <CartesianGrid stroke="none" strokeDasharray="0" />
          <XAxis dataKey="match" style={{fontSize: "8px"}}>
            <Label
            color="white"
            value="MATCHES"
            offset={-1}
            position="insideBottom"
            style={{ fontSize: "10px", fontWeight: "bold", color: "white", fontFamily: "Montserrat" }}
            />
          </XAxis>

          <YAxis style={{fontSize: "8px"}}>
            <Label
            value="FANTASY POINTS"
            angle={-90}
            // position="insideLeft"
            style={{ fontSize: "10px", fontWeight: "bold", color: "white", fontFamily: "Montserrat" }}
            />
          </YAxis>
          <Tooltip />
          {/* <Legend /> */}
          {/* <Line
            type="linear"
            dataKey={selectedQuery}
            stroke="#3498db"
            fill="#3498db"
            fillOpacity={0.3}
            dot={{ r: 5 }}
            // dot={false}
          /> */}
          <Area
            type="linear"
            dataKey={selectedQuery} // Dynamically change the dataKey based on selected query
            stroke={queryColors[selectedQuery]} // Line color
            fill="#3498db" // Area fill color
            fillOpacity={0.3} // Make the fill slightly transparent
            dot={true} // Show dots at data points
          />
        </AreaChart>
      </ResponsiveContainer>
      </div>
      
    </div>
  );
};

export default FantasyPointsChart;
