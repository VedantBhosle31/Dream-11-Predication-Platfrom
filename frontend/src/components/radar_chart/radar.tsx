import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import { BackendData } from "../../api/fetchData";
import { getSessionData, setSessionData } from "../../utils/sessionStorageUtils";
import { Numbers } from "@mui/icons-material";


interface RadarChartProps {
  numbers: number[];
}

const RadarChart: React.FC<RadarChartProps> = ({numbers}) => {


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
