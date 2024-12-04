import React from "react";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
  Label,
  ReferenceLine,
} from "recharts";


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
  maindata:ChartData[];
}


const VenueGraph: React.FC<VenueGraphProps> = ({ selected, maindata }) => {

  const queryColors: { [key: string]: string } = {
    venuescore: "#3498db", // Blue for Fantasy Points
    playerScore: "#2ecc71", // Green for Player Score
    runRate: "#e74c3c", // Red for Run Rate
  };


  // Calculate the average of the selected filter
  const calculateAverage = (data: ChartData[], filter: string): number => {
    const filteredValues = data.map((item) => item[filter as keyof ChartData]);
    const sum = filteredValues.reduce((acc, val) => (acc as number) + (val as number), 0);
    return (sum as number/ filteredValues.length);
  };

  // Get the average for the selected filter
  const average = calculateAverage(maindata, selected);

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
          <AreaChart data={maindata}>
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
            <ReferenceLine
              y={average} // Specify the Y-axis value for the line
              stroke="red" // Line color
              label={{
                value: "Average",
                position: "insideTopRight",
                fill: "red",
                fontSize: "10px",
              }} // Optional label for the line
            />

            {/* Area Chart with Gradient */}
            <Area
              type="linear"
              dataKey={selected}
              stroke={"#9A89FF"}
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
