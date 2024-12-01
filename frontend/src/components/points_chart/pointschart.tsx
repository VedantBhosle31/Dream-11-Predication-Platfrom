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
  ReferenceLine,
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
  venue: number;
  opposition: number;
  form: number;
  id: number;
}

const data: ChartData[] = [
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

interface VenueGraphProps {
  selected: string;
}

const getFillColor = (value: number) => {
  // If the data point is above the reference line, use green
  if (value > 70) {
    return "#4CAF50"; // Green for above reference line
  }
  // If the data point is below the reference line, use red
  return "#FF5722"; // Red for below reference line
};

const VenueGraph: React.FC<VenueGraphProps> = ({ selected }) => {
  // const [selectedQuery, setSelectedQuery] = useState<string>(selected);

  // // Handle query change
  // const handleQueryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  //   setSelectedQuery(event.target.value);
  // };

  const queryColors: { [key: string]: string } = {
    venuescore: "#3498db", // Blue for Fantasy Points
    playerScore: "#2ecc71", // Green for Player Score
    runRate: "#e74c3c", // Red for Run Rate
  };

  const minY = Math.min(
    ...data.map((item) => item[selected as keyof ChartData] as number)
  );
  console.log(minY);
  const maxY = Math.max(
    ...data.map((item) => item[selected as keyof ChartData] as number)
  );
  console.log(maxY);

  // type DataType = {
  //   Date: string;
  //   Previous_Runs: number;
  // };

  // const [somedata, setData] = useState<BackendData[] | null>(null);
  // const [loading, setLoading] = useState(true);
  // const [error, setError] = useState<string | null>(null);

  // useEffect(() => {
  //   const loadData = async () => {
  //     const cachedData = getSessionData<BackendData[]>('runsData');
  //     console.log(cachedData);

  //     if (cachedData) {
  //       setData(cachedData);
  //       setLoading(false);
  //     } else {
  //       try {
  //         const fetchedData = await fetchData('http://127.0.0.1:8000/graphs/get_player_points/1/');
  //         setData(fetchedData);
  //         setSessionData('runsData', fetchedData);
  //         setLoading(false);
  //       } catch (err) {
  //         setError(err instanceof Error ? err.message : 'Unknown error');
  //         setLoading(false);
  //       }
  //     }
  //   };

  //   loadData();
  // }, []);

  // if (loading) return <div>Loading...</div>;
  // if (error) return <div>Error: {error}</div>;

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
            {/* <defs>
              {/* Solid color stops for above and below the reference line */}
              {/* Solid color for above and below the reference line */}
              {/* <clipPath id="splitColor" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="0%"
                  stopColor="#4CAF50" // Green above reference line
                  // stopOpacity={0.8}
                />
                <stop
                  offset="100%"
                  stopColor="#FF5722" // Red below reference line
                  // stopOpacity={0.8}
                />
              </clipPath> */}
            {/* </defs> } */}

            <CartesianGrid stroke="none" strokeDasharray="0" />
            <XAxis
              style={{ fontSize: "8px" }}
              domain={[10, "dataMax"]}
              interval={0}
              dataKey="id"
            >
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
                value={selected}
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

            {/* Add Horizontal Line */}
            <ReferenceLine
              y={70} // Specify the Y-axis value for the line
              stroke="red" // Line color
              // strokeDasharray="3 3" // Optional: Dashed line
              label={{
                value: "Average",
                position: "insideTopRight",
                // fill: "red",
                fontSize: "10px",
              }} // Optional label for the line
            />

            {/* <Area
              type="linear"
              dataKey={selected}
              stroke={"#9A89FF"}
              fill="#FA2433"
              // fill="url(#splitColor)"
              fillOpacity={0.3}
              dot={true}
              data={data.map((point) => ({
                ...point,
                [selected]: (point[selected as keyof ChartData] as number) > 70
          ? point[selected as keyof ChartData]
          : 70,
              }))}
            />

            <Area
              type="linear"
              dataKey={selected}
              // stroke={"#9A89FF"}
              fill="green"
              // fill="url(#splitColor)"
              // fillOpacity={0.3}
              dot={true}
              data={data.map((point) => ({
                ...point,
                [selected]: (point[selected as keyof ChartData] as number) < 70
          ? point[selected as keyof ChartData]
          : 70,
              }))}
            /> */}

            {/* Area Chart with Gradient */}
            <Area
              type="linear"
              dataKey={selected}
              stroke={"#9A89FF"}
              // fill="url(#splitColor)"
              // fill=" ${{(entry) => getFillColor(entry.form)}}"
              fillOpacity={0.3}
              dot={true}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default VenueGraph;
