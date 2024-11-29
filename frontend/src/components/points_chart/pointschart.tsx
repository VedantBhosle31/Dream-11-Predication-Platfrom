import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart, Label } from "recharts";


type RunData = {
  Date: string; // ISO 8601 date string
  Previous_Runs: number; // Integer representing runs
};

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

    // // Handle query change
    // const handleQueryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    //   setSelectedQuery(event.target.value);
    // };

    const queryColors: { [key: string]: string } = {
        fantasyPoints: "#3498db", // Blue for Fantasy Points
        playerScore: "#2ecc71",   // Green for Player Score
        runRate: "#e74c3c",       // Red for Run Rate
    };


    const fetchData = async (): Promise<RunData[]> => {
      const response = await fetch("http://127.0.0.1:8000/graphs/get_player_points/1/");
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      console.log(response);
      return response.json();
    };
  
    useEffect(() => {
      const getData = async () => {
        try {
          const data = await fetchData();
          console.log("data: ",data);
        } catch (err: any) {
          console.log(err.message);
        }
      };
  
      getData();
    }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", width: "100%", height: "95%", alignContent: "space-between" }}>

      <div style={{display: "flex", width: "100%", height: "80%", justifyContent: "center", alignItems: "center", marginTop: "20px"}}>
      <ResponsiveContainer width={"80%"} height={"100%"}>
        <AreaChart data={data}>
          <CartesianGrid stroke="none" strokeDasharray="0" />
          <XAxis dataKey="match" style={{fontSize: "8px"}}>
            <Label
            color="white"
            value="NUMBER OF MATCHES"
            offset={-1}
            position="insideBottom"
            style={{ fontSize: "10px", fontWeight: "bold", color: "white", fontFamily: "Montserrat" }}
            />
          </XAxis>

          <YAxis style={{fontSize: "8px"}} axisLine={false}
                      tickLine={false}
                      tick={{ fill: "grey", fontSize: 7 }}
                      minTickGap={10}>
            <Label
            value="VPI"
            angle={-90}
            style={{ fontSize: "10px", fontWeight: "bold", color: "white", fontFamily: "Montserrat" }}
            />
          </YAxis>
          <Tooltip contentStyle={{color:"red", fontSize:"10px", backgroundColor:"black"}}/>
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
            dataKey={selectedQuery}
            stroke={"#9A89FF"}
            fill="#FA2433"
            fillOpacity={0.3}
            dot={true}
          />
        </AreaChart>
      </ResponsiveContainer>
      </div>
      
    </div>
  );
};

export default FantasyPointsChart;