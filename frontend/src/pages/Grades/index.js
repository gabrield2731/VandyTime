import React, { useEffect, useState } from "react";
import BarChartComponent from "../../components/BarChart";
import "./styles.css";
import { useLocation } from "react-router-dom";

const BACKEND = process.env.REACT_APP_API_URL;

const dummyGradeData = [
  { grade: "A+", count: 2 },
  { grade: "A", count: 5 },
  { grade: "A-", count: 8 },
  { grade: "B+", count: 7 },
  { grade: "B", count: 6 },
  { grade: "B-", count: 4 },
  { grade: "C+", count: 0 },
  { grade: "C", count: 2 },
  { grade: "C-", count: 1 },
  { grade: "D", count: 0 },
  { grade: "F", count: 1 },
  { grade: "P", count: 0 },
  { grade: "NP", count: 0 },
];

const dummyCourseInfo = {
  code: "CS 4278",
  name: "Principles of Software Engineering",
  description:
    "The nature of software. The object-oriented paradigm. Software life-cycle models. Requirements, specification, design, implementation, documentation, and testing of software. Object-oriented analysis and design. Software maintenance.",
  teacher: "SINGH, V",
  grades: [],
};

const Grades = () => {
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedInstructor, setSelectedInstructor] =
    useState("Choose a class");
  const [courseInfo, setCourseInfo] = useState(dummyCourseInfo);
  const [gradeData, setGradeData] = useState(dummyGradeData);
  const [courses, setCourses] = useState(["Select a class"]);
  const [teachers, setTeachers] = useState(["Select a teacher"]);
  const [average, setAverage] = useState("A+");

  const location = useLocation();
  const { code, teacher } = location.state || {};

  const handleCourseChange = (event) => {
    setSelectedCourse(event.target.value);
  };

  const handleInstructorChange = (event) => {
    setSelectedInstructor(event.target.value);
  };

  const handleGetClasses = async (course, instructor) => {
    try {
      // Fetch class information based on selected course and instructor
      console.log("in" + course + " " + instructor);
      console.log(
        `${BACKEND}/class/${encodeURIComponent(course)}/${encodeURIComponent(
          instructor
        )}`
      );
      const response = await fetch(
        `${BACKEND}/class/${encodeURIComponent(course)}/${encodeURIComponent(
          instructor
        )}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch grades");
      }
      const data = await response.json();
      setCourseInfo(data);

      const gradeIds = data.grades;

      // Initialize the fixed-length array with all grades set to zero count
      const gradesArray = [
        { grade: "A+", count: 0 },
        { grade: "A", count: 0 },
        { grade: "A-", count: 0 },
        { grade: "B+", count: 0 },
        { grade: "B", count: 0 },
        { grade: "B-", count: 0 },
        { grade: "C+", count: 0 },
        { grade: "C", count: 0 },
        { grade: "C-", count: 0 },
        { grade: "D", count: 0 },
        { grade: "F", count: 0 },
        { grade: "P", count: 0 },
        { grade: "NP", count: 0 },
      ];

      // Fetch each grade based on the IDs and update the count in the array directly
      for (let i = 0; i < gradeIds.length; i++) {
        const response = await fetch(`${BACKEND}/grade/${gradeIds[i]}`);
        if (!response.ok) {
          throw new Error("Failed to fetch grade");
        }
        const grade = await response.json();

        // Find the grade object in the array and increment its count
        const gradeObj = gradesArray.find((g) => g.grade === grade.grade);
        if (gradeObj) {
          gradeObj.count++;
        }
      }

      setGradeData(gradesArray);
    } catch (error) {
      console.error("Error fetching grades:", error);
    }
  };

  const handleChooseClass = async () => {
    // Ensure that a course and instructor are selected
    if (selectedCourse === "" || selectedInstructor === "Choose a class") {
      return;
    }
    handleGetClasses(selectedCourse, selectedInstructor);
  };

  useEffect(() => {
    // Fetch initial data for courses and set dummy grade data
    const fetchInitialData = async () => {
      if (code && teacher) {
        console.log(code + " " + teacher);
        handleGetClasses(code, teacher);
      }
      try {
        const response = await fetch(`${BACKEND}/class`);
        if (!response.ok) {
          throw new Error("Failed to fetch classes");
        }
        const data = await response.json();

        // Use a Set to ensure unique values and normalize class names to lowercase
        let coursesSet = new Set();
        data.forEach((course) => {
          if (course.name && course.name.trim() !== "") {
            coursesSet.add(course.name.trim());
          }
        });

        // Convert set back to an array and format class names if needed (e.g., capitalize)
        const sorted = Array.from(coursesSet).sort();

        setCourses(sorted);
        setSelectedCourse(sorted[0]);
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };

    fetchInitialData();
  }, [code, teacher]);

  useEffect(() => {
    //TODO: Fetch teachers based on selected course
    // fix this fetch and make it match the format of the variables
    if (!selectedCourse) return;

    const fetchTeachers = async () => {
      try {
        const response = await fetch(
          `${BACKEND}/class/${encodeURIComponent(
            selectedCourse.toLowerCase()
          )}/teachers`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch teachers");
        }

        const data = await response.json();
        const sorted = data.sort();
        setTeachers(sorted);
        setSelectedInstructor(sorted[0]);
      } catch (error) {
        console.error("Error fetching teachers:", error);
      }
    };

    fetchTeachers();
  }, [selectedCourse]);

  useEffect(() => {
    // Function to convert letter grades to numerical values
    const getGradeValue = (grade) => {
      switch (grade) {
        case "A+":
          return 4.3;
        case "A":
          return 4.0;
        case "A-":
          return 3.7;
        case "B+":
          return 3.3;
        case "B":
          return 3.0;
        case "B-":
          return 2.7;
        case "C+":
          return 2.3;
        case "C":
          return 2.0;
        case "C-":
          return 1.7;
        case "D":
          return 1.0;
        case "F":
          return 0.0;
        default:
          return null; // Handle unrecognized grades
      }
    };

    // Function to convert average numerical values to letter grades
    const getLetterGrade = (avg) => {
      if (avg >= 4.15) return "A+";
      if (avg >= 3.85) return "A";
      if (avg >= 3.5) return "A-";
      if (avg >= 3.15) return "B+";
      if (avg >= 2.85) return "B";
      if (avg >= 2.5) return "B-";
      if (avg >= 2.15) return "C+";
      if (avg >= 1.85) return "C";
      if (avg >= 1.5) return "C-";
      if (avg >= 0.5) return "D";
      return "F";
    };

    const numericalGrades = gradeData.flatMap((gradeObj) => {
      const gradeValue = getGradeValue(gradeObj.grade);
      if (gradeValue !== null) {
        // Create an array of length `count` filled with the gradeValue
        return Array(gradeObj.count).fill(gradeValue);
      }
      return []; // If gradeValue is null, return an empty array (no grades)
    });

    // If there are no valid numerical grades, set average to "N/A"
    if (numericalGrades.length === 0) {
      setAverage("N/A");
      return;
    }

    // Calculate the average numerical value
    const averageValue =
      numericalGrades.reduce((acc, val) => acc + val, 0) /
      numericalGrades.length;

    // Get the corresponding letter grade for the average value
    const newAverage = getLetterGrade(averageValue);

    // Set the calculated average
    setAverage(newAverage);
  }, [gradeData]);

  return (
    <div className="container">
      {/* Input Section */}
      <div className="input-section">
        {/* Course Selector */}
        <div>
          <label htmlFor="course-select">Course: </label>
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

        {/* Instructor Selector */}
        <div>
          <label htmlFor="instructor-select">Instructor: </label>
          <select
            id="instructor-select"
            value={selectedInstructor}
            onChange={handleInstructorChange}
          >
            {teachers.map((teacher) => (
              <option key={teacher} value={teacher}>
                {teacher}
              </option>
            ))}
          </select>
        </div>
        <div>
          <button onClick={handleChooseClass}>Check Class</button>
        </div>
      </div>

      {/* Flex container to organize layout */}
      <div className="main-content">
        {/* Grades Distribution Bar Chart */}
        <div className="grade-distribution">
          <h3>Grade Distribution</h3>
          <div className="chart-container">
            <BarChartComponent
              data={gradeData}
              xAxisKey="grade"
              barDataKey="count"
              barColor="#c4a55e"
            />
          </div>
        </div>

        {/* Course Information Section - Moved to the right */}
        <div className="course-info">
          <h2>{courseInfo.code}</h2>
          <p>{courseInfo.name}</p>
          <p>Instructor: {courseInfo.teacher}</p>
          <p className="description">{courseInfo.description}</p>
          <div>
            <p className="course-average">
              <strong>Course Average: </strong> {average}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Grades;
