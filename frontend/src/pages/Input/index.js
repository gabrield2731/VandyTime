import React, { useState } from "react";
import { useAuth } from "../../stores/firebase"; // Make sure this path is correct
import "./styles.css";

// Dummy list of courses
const courses = ["CS 168", "CS 161", "CS 162", "CS 169"];

// Dummy list of professors for filtering
const professors = [
  "All",
  "RATNASAMY, S",
  "GARCIA, L",
  "KUBITZ, N",
  "LEE, H",
];

const grades = ["A", "B", "C", "D", "F"];

const Input = () => {
  const user = useAuth();
  // Add logic to see if user is not null

  const [selectedProfessor, setSelectedProfessor] = useState("All");
  const [selectedCourse, setSelectedCourse] = useState("All");
  const [selectedGrade, setSelectedGrade] = useState("All");
  const [inputValue, setInputValue] = useState("");

  const handleCourseChange = (event) => {
    setSelectedCourse(event.target.value);
    setSelectedProfessor("");
  };

  const handleProfessorChange = (event) => {
    setSelectedProfessor(event.target.value);
  };

  const handleGradeChange = (event) => {
    setSelectedGrade(event.target.value);
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = () => {
    console.log("User input submitted: ", inputValue);
  };

  return (
    <div className="container">
      <h1>Input</h1>
      <h3>Enter Your Class Data Below</h3>

      {/* Course Selector */}
      <div className="course-selector">
        <label htmlFor="course-select">Select Course: </label>
        <select
          id="course-select"
          value={selectedCourse}
          onChange={handleCourseChange}
        >
          {courses.map((course) => (
            <option key={course} value={course}>
              {course}
            </option>
          ))}
        </select>
      </div>

      {/* Professor Selector */}
      <div className="professor-selector">
        <label htmlFor="professor-select">Select Professor: </label>
        <select
          id="professor-select"
          value={selectedProfessor}
          onChange={handleProfessorChange}
        >
          {professors.map((professor) => (
            <option key={professor} value={professor}>
              {professor}
            </option>
          ))}
        </select>
      </div>

        {/* Grade Selector */}
        <div className="grade-selector">
        <label htmlFor="grade-select">Select Grade: </label>
        <select
          id="grade-select"
          value={selectedGrade}
          onChange={handleGradeChange}
        >
          {grades.map((grade) => (
            <option key={grade} value={grade}>
              {grade}
            </option>
          ))}
        </select>
      </div>

      {/* Review Box */}
      <div className="review-box">
        <textarea
          id="user-input"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter review"
          rows={5} // Start with multiple rows (adjust as needed)
        />
      </div>

      {/* Submit Button */}
      <div className="button-container">
        <button onClick={handleSubmit}>Submit</button>
      </div>
    </div>  
  );
};

export default Input;
