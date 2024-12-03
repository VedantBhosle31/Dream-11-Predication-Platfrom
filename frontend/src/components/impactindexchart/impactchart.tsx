// // import React from "react";
// // import {
// //   BarChart,
// //   Bar,
// //   XAxis,
// //   YAxis,
// //   CartesianGrid,
// //   Tooltip,
// //   Legend,
// //   ResponsiveContainer,
// // } from "recharts";

// // const data = [
// //   {
// //     name: "Strike Rate",
// //     values: [156.7, -188.5],
// //   },
// //   {
// //     name: "Boundaries",
// //     values: [7, -5],
// //   },
// //   {
// //     name: "Dismissals",
// //     values: [1, -3],
// //   },
// // ];

// // const ImpactChart: React.FC = () => {
// //   return (
// //     <div style={{width:"85%", height:"80%", alignContent:"center", alignItems:"center", justifyItems:"end"}}>
// //       {/* Title */}
// //       <div style={{ marginBottom: "20px", color: "white", height:"5%", textAlign:"center", fontSize:"20px" }}>
// //       vs Spin   vs Pace
// //       </div>
// //       {/* Chart */}
// //       <ResponsiveContainer width="85%" height="80%" >
// //         <BarChart
// //           data={data}
// //           layout="vertical"
// //           margin={{
// //             top: 20,
// //             right: 30,
// //             left: 50,
// //             bottom: 5,
// //           }}
// //         >
// //           {/* <CartesianGrid strokeDasharray="3 3" /> */}
// //           <XAxis type="number" hide domain={[-200, 200]} />
// //           <YAxis
// //             type="category"
// //             dataKey="name"
// //             color="white"
// //             style={{ fontSize: "15px", color: "white" }}
// //             axisLine={false}
// //             tickLine={false}
// //           />
// //           <Tooltip />
// //           {/* <Legend
// //             style={{ fontSize: "15px", color: "white" }}
// //             formatter={(value) =>
// //               value === "Spin"
// //                 ? "Vs Spin"
// //                 : value === "Pace"
// //                 ? "Vs Pace"
// //                 : value
// //             }
// //           /> */}
// //           <Bar dataKey="values" fill="#FA2433" barSize={20} />
// //           <Bar dataKey="values" fill="#FA2433" barSize={20} />
// //           <Bar dataKey="values" fill="#FA2433" barSize={20} />
// //           {/* <Bar dataKey="values" fill="#f3722c" barSize={20} /> */}
// //         </BarChart>
// //       </ResponsiveContainer>
// //     </div>
// //   );
// // };

// // export default ImpactChart;

// // import React from "react";
// // import {
// //   BarChart,
// //   Bar,
// //   XAxis,
// //   YAxis,
// //   CartesianGrid,
// //   Tooltip,
// //   Legend,
// //   ResponsiveContainer,
// // } from "recharts";

// // const data = [
// //     {
// //       name: "Strike Rate",
// //       values: [156.7, -188.5],
// //     },
// //     {
// //       name: "Boundaries",
// //       values: [7, -5],
// //     },
// //     {
// //       name: "Dismissals",
// //       values: [1, -3],
// //     },
// //   ];

// // const ImpactChart: React.FC = () => {
// //   return (
// //     <div style={{ width: "100%", textAlign: "center" }}>
// //       {/* Title */}
// //       {/* <h2 style={{ marginBottom: "20px", color: "#333" }}>
// //         Performance vs Spin and Pace
// //       </h2> */}
// //       {/* Chart */}
// //       <ResponsiveContainer width="80%" height={250}>
// //         <BarChart
// //         layout="vertical"
// //           data={data}
// //           margin={{
// //             top: 20,
// //             right: 50,
// //             left: 50,
// //             bottom: 20,
// //           }}
// //         >
// //           {/* <CartesianGrid strokeDasharray="3 3" /> */}
// //           <XAxis
// //           type="number"
// //             domain={[-200, 200]}
// //             tickFormatter={(value) => Math.abs(value).toString()}  hide/>
// //           <YAxis
// //           type="category"
// //           dataKey="name"
// //           tickLine={false}
// //           axisLine={false}
// //           width={100}
// //           tick={{ fontSize: 14 }}
// //           />
// //           <Tooltip />
// //           {/* <Legend
// //           formatter={(value) =>
// //             value === "Spin" ? "Vs Spin" : value === "Pace" ? "Vs Pace" : value
// //           }
// //           /> */}

// //           {/* Bars for different metrics */}
// //           <Bar dataKey="values" fill="#f94144" barSize={20} name="Vs Spin" />
// //           {/* <Bar dataKey="Pace" fill="#f3722c" barSize={20} name="Vs Pace" /> */}
// //         </BarChart>
// //       </ResponsiveContainer>
// //     </div>
// //   );
// // };

// // export default ImpactChart;

// import * as React from 'react';
// import { BarChart } from '@mui/x-charts/BarChart';

// const seriesA = {
//   data: [2, 3, 1],
//   label: 'vs Spin',
// };
// const seriesB = {
//   data: [-3, -1, -4],
//   label: 'vs Pace',
// };
// const yLabels = ['Strike rate', 'Dismissals', 'Boundaries'];

// export default function BasicStacking() {
//   return (
//     <BarChart
//     layout='horizontal'
//       width={600}
//       height={300}
//       series={[
//         { ...seriesA, stack: 'total' },
//         { ...seriesB, stack: 'total' },
//       ]}
//       yAxis={}

//       // yAxis={}
//     />

//   );
// }

import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  LabelList,
  ReferenceLine,
} from "recharts";

// const data = [
//   { category: "Strike Rate", values:[156.7, -188.5 ] },
//   { category: "Boundaries", values:[7, -5 ]  },
//   { category: "Dismissals", values:[1, -3]},
// ];

interface ImpactChartProps {
  battingStats: any;
  filter: string;
}

const ImpactChart: React.FC<ImpactChartProps> = ({ battingStats, filter }) => {
  var tbaHs_economy_avg = 0;
  var tbaHp_economy_avg = 0;
  var tbaHs_4s_avg = 0;
  var tbaHs_6s_avg = 0;
  var tbaHp_4s_avg = 0;
  var tbaHp_6s_avg = 0;
  var tbaHs_dismissals_avg = 0;
  var tbaHp_dismissals_avg = 0;

  const calculateAverage = (values: number[]) => {
    const sum = values.reduce((total, value) => total + value, 0);
    return sum / values.length;
  };

  if (filter === "Overall") {
    // Calculate averages for required metrics
    tbaHs_economy_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_economy_agg"])
    );
    tbaHp_economy_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_economy_agg"])
    );
    tbaHs_4s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_4s_agg"])
    );
    tbaHs_6s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_6s_agg"])
    );
    tbaHp_4s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_4s_agg"])
    );
    tbaHp_6s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_6s_agg"])
    );
    tbaHs_dismissals_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_dismissals_agg"])
    );
    tbaHp_dismissals_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_dismissals_agg"])
    );
  }
  if (filter === "Powerplay") {
    // Calculate averages for required metrics
    tbaHs_economy_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_economy_1"])
    );
    tbaHp_economy_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_economy_1"])
    );
    tbaHs_4s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_4s_1"])
    );
    tbaHs_6s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_6s_1"])
    );
    tbaHp_4s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_4s_1"])
    );
    tbaHp_6s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_6s_1"])
    );
    tbaHs_dismissals_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_dismissals_1"])
    );
    tbaHp_dismissals_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_dismissals_1"])
    );
  }
  if (filter === "Middle") {
    // Calculate averages for required metrics
    tbaHs_economy_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_economy_2"])
    );
    tbaHp_economy_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_economy_2"])
    );
    tbaHs_4s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_4s_2"])
    );
    tbaHs_6s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_6s_2"])
    );
    tbaHp_4s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_4s_2"])
    );
    tbaHp_6s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_6s_2"])
    );
    tbaHs_dismissals_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_dismissals_2"])
    );
    tbaHp_dismissals_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_dismissals_2"])
    );
  }
  if (filter === "Death") {
    // Calculate averages for required metrics
    tbaHs_economy_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_economy_3"])
    );
    tbaHp_economy_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_economy_3"])
    );
    tbaHs_4s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_4s_3"])
    );
    tbaHs_6s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_6s_3"])
    );
    tbaHp_4s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_4s_3"])
    );
    tbaHp_6s_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_6s_3"])
    );
    tbaHs_dismissals_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahs_dismissals_3"])
    );
    tbaHp_dismissals_avg = calculateAverage(
      battingStats.map((item: any) => item["tbahp_dismissals_3"])
    );
  }

  // Calculate data for the chart
  const calculatedData = [
    {
      category: "Strike Rate",
      values: [
        -1 * (tbaHs_economy_avg * 100), // vs Spin
        tbaHp_economy_avg * 100, // vs Pace
      ],
    },
    {
      category: "Boundaries",
      values: [
        -1 * (tbaHs_4s_avg + tbaHs_6s_avg), // vs Spin
        tbaHp_4s_avg + tbaHp_6s_avg, // vs Pace
      ],
    },
    {
      category: "Dismissals",
      values: [
        -1 * tbaHs_dismissals_avg, // vs Spin
        tbaHp_dismissals_avg, // vs Pace
      ],
    },
  ];

  console.log("calculateddata", calculatedData);

  return (
    <div
      style={{
        backgroundColor: "#1C1C1C",
        padding: "20px",
        borderRadius: "10px",
      }}
    >
      <h3 style={{ color: "#FFFFFF", textAlign: "center", fontSize: "10px" }}>
        vs Spin vs Pace
      </h3>
      <ResponsiveContainer width="80%" height={200}>
        <BarChart
          data={calculatedData}
          layout="vertical"
          margin={{ top: 20, right: 40, left: 40, bottom: 20 }}
        >
          {/* <CartesianGrid strokeDasharray="3 3" horizontal={false} /> */}
          <XAxis
            type="number"
            // hide
            tick={{ fill: "#FFFFFF" }}
            fontSize={15}
            // domain={[-200, 200]} // Adjust this based on your data
            tickFormatter={(value) => Math.abs(value).toString()} // Show positive values on both sides
          />
          <YAxis
            type="category"
            dataKey="category"
            tick={{ fill: "#FFFFFF" }}
            fontSize={15}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            wrapperStyle={{
              backgroundColor: "#333",
              border: "none",
              borderRadius: "5px",
              padding: "5px",
              fontSize: "10px", // Decrease font size
            }}
            contentStyle={{
              color: "black",
              padding: "5px", // Decrease padding inside the tooltip
            }}
            // formatter={(value) => {
            //   // const numericValue = parseFloat(value as string); // Try converting the value to a number
            //   // if (!isNaN(numericValue)) {
            //   //   return numericValue.toFixed(2); // Format to 2 decimal places if it's a valid number
            //   // }
            //   return value; // Return the original value if it's not a number
            // }}
            // formatter={(value: number) => Math.abs(value)} // Display absolute values
            labelStyle={{ color: "#black", fontSize: "10px" }} // Customize label styling
          />
          {/* <Legend
            wrapperStyle={{ color: "#FFFFFF" }}
            formatter={(value) =>
              value === "vsSpin" ? "vs Spin (Right)" : "vs Pace (Left)"
            }
          /> */}

          <Bar dataKey="values" fill="#FA2433" />
          {/* <Bar dataKey="vsPace" fill="#A00000" name="vs Pace" /> */}

          <ReferenceLine
            x={0} // Specify the Y-axis value for the line
            stroke="white" // Line color
            // strokeDasharray="3 3" // Optional: Dashed line
            label={{
              // value: "Average",
              position: "top",
              fill: "white",
              fontSize: "10px",
            }} // Optional label for the line
          />

          <LabelList
            dataKey="values"
            position="top"
            // formatter={(value: any) => {
            //   const numericValue = parseFloat(value); // Convert value to number
            //   // if (!isNaN(numericValue)) {
            //   //   return Math.abs(numericValue).toFixed(2); // Format to 2 decimal places
            //   // }
            //   return (Math.abs(numericValue)).toFixed(2); // Return original value if not a number
            // }}
            formatter={(value: any) => {
              const numericValue = Math.abs(parseFloat(value)); // Get the absolute value
              return numericValue.toFixed(2); // Format to 2 decimal places
            }}
            fill="black"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ImpactChart;
