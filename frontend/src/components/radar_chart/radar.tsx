import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import { fetchData } from "../../api/fetchData";
import { getSessionData, setSessionData } from "../../utils/sessionStorageUtils";



const RadarChart: React.FC = () => {
  const [numbers, setNumbers] = useState<number[]>([]);

  // const fetchData = async (): Promise<RunData[]> => {
  //   const response = await fetch(
  //     "http://127.0.0.1:8000/graphs/get_player_radar_chart/1/"
  //   );
  //   if (!response.ok) {
  //     throw new Error("Failed to fetch data");
  //   }
  //   console.log(response);

  //   const jsonData = await response.json();

  //   // Extracting only values from the JSON
  //   const values = Object.values(jsonData) as number[];

  //   setNumbers(values);

  //   return response.json();
  // };

  // useEffect(() => {
  //   const getData = async () => {
  //     try {
  //       const data = await fetchData();
  //       console.log("data: ", data);
  //     } catch (err: any) {
  //       console.log(err.message);
  //     }
  //   };

  //   getData();
  // }, []);

  const chartOptions: ApexOptions = {
    chart: {
      type: "radar",
      toolbar: {
        show: false,
      },
    },
    // title: {
    //   text: "Radar Chart - Vertex Point Up",
    // },
    xaxis: {
      categories: [
        "STRIKE RATE",
        "WICKETS",
        "ECONOMY",
        "MATCHUP",
        "FIELDING",
        "AVERAGE",
      ],
      labels: {
        style: {
          colors: [
            "#FA2433",
            "#FA2433",
            "#FA2433",
            "#FA2433",
            "#FA2433",
            "#FA2433",
          ],
          fontSize: "8px",
          fontFamily: "Montserrat",
          fontWeight: "bold",
        },
      },
    },
    plotOptions: {
      radar: {
        size: 80,
        polygons: {
          strokeColors: "#e9e9e9",
          connectorColors: "#e9e9e9",
          strokeWidth: "0.3px",
        },
      },
    },
    markers: {
      size: 4,
      colors: ["#FA2433"],
      strokeColors: "#8E1F27",
      strokeWidth: 1,
      fillOpacity: 0.8,
    },
    fill: {
      opacity: 0.8,
      colors: ["#8E1F27"],
    },
    tooltip: {
      enabled: true,
      theme: "dark",
      style: {
        fontSize: "10px",
        fontFamily: "Montserrat",
      },
    },
    dataLabels: {
      enabled: false,
    },
    yaxis: {
      show: false,
    },
  };

  const chartSeries = [
    {
      name: "Value",
      data: numbers,
    },
  ];

  return (
    <div>
      <Chart
        options={chartOptions}
        series={chartSeries}
        type="radar"
        height={300}
      />
    </div>
  );
};

export default RadarChart;
