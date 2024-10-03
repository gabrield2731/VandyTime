import React from "react";
import BarChartComponent from "../../components/BarChart";

const data = [
  { name: "Jan", score: 4000 },
  { name: "Feb", score: 3000 },
  { name: "Mar", score: 2000 },
  { name: "Apr", score: 2780 },
  { name: "May", score: 1890 },
];

const Grades = () => {
  return (
    <div>
      <h1>Grades</h1>
      <BarChartComponent
        data={data}
        xAxisKey="name"
        barDataKey="score"
        barColor="#82ca9d"
      />
    </div>
  );
};

export default Grades;
