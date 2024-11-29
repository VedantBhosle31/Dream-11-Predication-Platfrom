import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
  Label,
} from "recharts";
import {
  getSessionData,
  setSessionData,
} from "../../utils/sessionStorageUtils";
import { BackendData, fetchData } from "../../api/fetchData";

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
    match: "vs AUS",
    fantasyPoints: 120,
    playerScore: 80,
    runRate: 169.2,
  },
  {
    match: "vs SA",
    fantasyPoints: 140,
    playerScore: 100,
    runRate: 150,
  },
  {
    match: "vs BAN",
    fantasyPoints: 110,
    playerScore: 90,
    runRate: 132.8,
  },
  {
    match: "vs WI",
    fantasyPoints: 130,
    playerScore: 110,
    runRate: 120.8,
  },
  {
    match: "vs PAK",
    fantasyPoints: 150,
    playerScore: 120,
    runRate: 167.9,
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
    playerScore: "#2ecc71", // Green for Player Score
    runRate: "#e74c3c", // Red for Run Rate
  };

  type DataType = {
    Date: string;
    Previous_Runs: number;
  };

  const [somedata, setData] = useState<BackendData[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      const cachedData = getSessionData<BackendData[]>('runsData');
      console.log(cachedData);

      if (cachedData) {
        setData(cachedData);
        setLoading(false);
      } else {
        try {
          const fetchedData = await fetchData('http://127.0.0.1:8000/graphs/get_player_points/1/');
          setData(fetchedData);
          setSessionData('runsData', fetchedData);
          setLoading(false);
        } catch (err) {
          setError(err instanceof Error ? err.message : 'Unknown error');
          setLoading(false);
        }
      }
    };

    loadData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        height: "95%",
        alignContent: "space-between",
      }}
    >
      <div
        style={{
          display: "flex",
          width: "100%",
          height: "80%",
          justifyContent: "center",
          alignItems: "center",
          marginTop: "20px",
        }}
      >
        <ResponsiveContainer width={"80%"} height={"100%"}>
          <AreaChart data={data}>
            <CartesianGrid stroke="none" strokeDasharray="0" />
            <XAxis dataKey="match" style={{ fontSize: "8px" }}>
              <Label
                color="white"
                value="NUMBER OF MATCHES"
                offset={-1}
                position="insideBottom"
                style={{
                  fontSize: "10px",
                  fontWeight: "bold",
                  color: "white",
                  fontFamily: "Montserrat",
                }}
              />
            </XAxis>

            <YAxis
              style={{ fontSize: "8px" }}
              axisLine={false}
              tickLine={false}
              tick={{ fill: "grey", fontSize: 7 }}
              minTickGap={10}
            >
              <Label
                value="VPI"
                angle={-90}
                style={{
                  fontSize: "10px",
                  fontWeight: "bold",
                  color: "white",
                  fontFamily: "Montserrat",
                }}
              />
            </YAxis>
            <Tooltip
              contentStyle={{
                color: "red",
                fontSize: "10px",
                backgroundColor: "black",
              }}
            />
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
