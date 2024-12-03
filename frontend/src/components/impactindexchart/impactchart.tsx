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
} from "recharts";

const data = [
  { category: "Strike Rate", values:[156.7, -188.5 ] },
  { category: "Boundaries", values:[7, -5 ]  },
  { category: "Dismissals", values:[1, -3]},
];

const ImpactChart: React.FC = () => {
  return (
    <div style={{ backgroundColor: "#1C1C1C", padding: "20px", borderRadius: "10px" }}>
      <h3 style={{ color: "#FFFFFF", textAlign: "center", fontSize:"10px" }}>vs Spin vs Pace</h3>
      <ResponsiveContainer width="80%" height={200}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 20, right: 40, left: 40, bottom: 20 }}
        >
          {/* <CartesianGrid strokeDasharray="3 3" horizontal={false} /> */}
          <XAxis
            type="number"
            hide
            tick={{ fill: "#FFFFFF" }}
            fontSize={15}
            domain={[-200, 200]} // Adjust this based on your data
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
          {/* <Tooltip
            // wrapperStyle={{ backgroundColor: "#333", border: "none" }}
            // formatter={(value: number) => Math.abs(value)} // Display absolute values in tooltips
          /> */}
          {/* <Legend
            wrapperStyle={{ color: "#FFFFFF" }}
            formatter={(value) =>
              value === "vsSpin" ? "vs Spin (Right)" : "vs Pace (Left)"
            }
          /> */}
          <Bar dataKey="values" fill="#FF4D4D" />
          {/* <Bar dataKey="vsPace" fill="#A00000" name="vs Pace" /> */}
          <LabelList
              dataKey="values"
              position="top"
              // formatter={(value: number) => value.toString()}
              fill="#FFFFFF"
            />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ImpactChart;

