import React from "react";
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

const RadarChart: React.FC = () => {
  const chartOptions: ApexOptions = {
    chart: {
      type: "radar",
      toolbar: {
        show: false, // Disables the toolbar (removes download options)
      },
    },
    // title: {
    //   text: "Radar Chart - Vertex Point Up",
    // },
    xaxis: {
      categories: ["STRIKE RATE", "WICKETS", "ECONOMY", "MATCHUP", "FIELDING", "AVERAGE"],
      labels: {
        style: {
          colors: ["white", "white", "white", "white", "white", "white"],
          fontSize: "8px",
          fontFamily: "Montserrat",
          fontWeight: "bold", // Make it bold
        },
      },
    },
    plotOptions: {
      radar: {
        size: 110,
        polygons: {
          strokeColors: "#e9e9e9",
          connectorColors: "#e9e9e9",
          strokeWidth: "0.3px",
        },
      },
    },
    markers: {
      size: 4,
      colors: ["white"],
      strokeColors: "white",
      strokeWidth: 1,
      fillOpacity: 0.3
    },
    fill: {
      opacity: 0.5,
      colors: ["white"],
    },
    tooltip: {
      enabled: true,
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
      data: [10, 20, 30, 40, 50, 60], // Rearranged to match the rotated categories
    },
  ];

  return (
    <div>
      <Chart
        options={chartOptions}
        series={chartSeries}
        type="radar"
        height={270}
      />
    </div>
  );
};

export default RadarChart;
