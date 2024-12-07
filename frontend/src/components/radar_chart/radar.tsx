import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

interface RadarChartProps {
  numbers: number[];
}

const RadarChart: React.FC<RadarChartProps> = ({numbers}) => {

  const minValues = [0,0,0,0, 0, 0];
  const maxValues = [1,1,1,1, 1, 1];

  const normalizedNumbers = numbers.map((value, index) => {
    const min = minValues[index];
    const max = maxValues[index];
    return (value - min) / (max - min); // Normalize to range [0, 1]
  });

  const chartOptions: ApexOptions = {
    chart: {
      type: "radar",
      toolbar: {
        show: false,
      },
    },
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
        // size: 80,
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
      data: normalizedNumbers,
    },
  ];

  return (
    <div>
      <Chart
        options={chartOptions}
        series={chartSeries}
        type="radar"
        height={250}
      />
    </div>
  );
};

export default RadarChart;
