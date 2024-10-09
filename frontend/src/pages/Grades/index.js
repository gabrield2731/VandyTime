import React, { useState } from "react";
import BarChartComponent from "../../components/BarChart";

// Sample grade data (adjusted to match the chart in the image)
const gradeData = [
  { grade: "A+", percentage: 0 },
  { grade: "A", percentage: 45 },
  { grade: "A-", percentage: 15 },
  { grade: "B+", percentage: 10 },
  { grade: "B", percentage: 5 },
  { grade: "B-", percentage: 2 },
  { grade: "C+", percentage: 0 },
  { grade: "C", percentage: 2 },
  { grade: "C-", percentage: 1 },
  { grade: "D", percentage: 1 },
  { grade: "F", percentage: 0 },
  { grade: "P", percentage: 20 },
  { grade: "NP", percentage: 0 },
];

const courseInfo = {
  courseCode: "COMPSCI 168",
  courseName: "Introduction to the Internet: Architecture and Protocols",
  term: "Fall 2022",
  instructor: "RATNASAMY, S",
  courseAverage: "B+ (3.26)",
  sectionAverage: "A- (3.737)",
  percentile: "11th-19th Percentile",
};

const Grades = () => {
  const [selectedCourse, setSelectedCourse] = useState("COMPSCI 168");
  const [selectedInstructor, setSelectedInstructor] = useState("RATNASAMY, S");

  const handleCourseChange = (event) => {
    setSelectedCourse(event.target.value);
  };

  const handleInstructorChange = (event) => {
    setSelectedInstructor(event.target.value);
  };

  return (
    <div>
      {/* Input Section */}
      <div style={{ display: "flex", gap: "10px", padding: "20px" }}>
        {/* Course Selector */}
        <div>
          <label htmlFor="course-select">Course: </label>
          <select
            id="course-select"
            value={selectedCourse}
            onChange={handleCourseChange}
          >
            <option value="COMPSCI 168">COMPSCI 168</option>
            <option value="COMPSCI 161">COMPSCI 161</option>
            <option value="COMPSCI 162">COMPSCI 162</option>
            {/* Add more courses as needed */}
          </select>
        </div>

        {/* Instructor Selector */}
        <div>
          <label htmlFor="instructor-select">Instructor: </label>
          <select
            id="instructor-select"
            value={selectedInstructor}
            onChange={handleInstructorChange}
          >
            <option value="RATNASAMY, S">RATNASAMY, S</option>
            <option value="GARCIA, L">GARCIA, L</option>
            <option value="KUBITZ, N">KUBITZ, N</option>
            {/* Add more instructors as needed */}
          </select>
        </div>

        {/* Add Class Button */}
        <div>
          <button style={{ padding: "5px 15px", backgroundColor: "#007bff", color: "white", border: "none", borderRadius: "5px" }}>
            Add Class
          </button>
        </div>
      </div>

      {/* Course Information Section */}
      <div style={{ padding: "20px" }}>
        <h2>{courseInfo.courseCode}</h2>
        <p>{courseInfo.courseName}</p>
        <p>{courseInfo.term} | Instructor: {courseInfo.instructor}</p>
        <div>
          <p>
            <strong>Course Average: </strong> {courseInfo.courseAverage}
          </p>
          <p>
            <strong>Section Average: </strong> {courseInfo.sectionAverage}
          </p>
          <p>
            <strong>{courseInfo.percentile}</strong>
          </p>
        </div>
      </div>

      {/* Grades Distribution Bar Chart */}
      <div>
        <h3>Grade Distribution</h3>
        <BarChartComponent
          data={gradeData}
          xAxisKey="grade"
          barDataKey="percentage"
          barColor="#82ca9d"
        />
      </div>
    </div>
  );
};

export default Grades;
