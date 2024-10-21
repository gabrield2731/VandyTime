import React, { useEffect, useState } from "react";
import BarChartComponent from "../../components/BarChart";
import "./styles.css";

const BACKEND = process.env.REACT_APP_API_URL;

const dummyGradeData = [
  { grade: "A+", percentage: 2 },
  { grade: "A", percentage: 5 },
  { grade: "A-", percentage: 8 },
  { grade: "B+", percentage: 7 },
  { grade: "B", percentage: 6 },
  { grade: "B-", percentage: 4 },
  { grade: "C+", percentage: 0 },
  { grade: "C", percentage: 2 },
  { grade: "C-", percentage: 1 },
  { grade: "D", percentage: 0 },
  { grade: "F", percentage: 1 },
  { grade: "P", percentage: 0 },
  { grade: "NP", percentage: 0 },
];

const dummyCourseInfo = {
  courseCode: "CS 4278",
  courseName: "Principles of Software Engineering",
  description:
    "The nature of software. The object-oriented paradigm. Software life-cycle models. Requirements, specification, design, implementation, documentation, and testing of software. Object-oriented analysis and design. Software maintenance.",
  term: "Fall 2024",
  instructor: "SINGH, V",
  grades: [],
};

const Grades = () => {
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedInstructor, setSelectedInstructor] =
    useState("Choose a class");
  const [courseInfo, setCourseInfo] = useState(dummyCourseInfo);
  const [gradeData, setGradeData] = useState([]);
  const [courses, setCourses] = useState([
    "CS 1101",
    "CS 2201",
    "CS 3281",
    "CS 4278",
  ]);
  const [teachers, setTeachers] = useState(["Choose a class"]);
  const [average, setAverage] = useState("A+");

  const handleCourseChange = (event) => {
    setSelectedCourse(event.target.value);
  };

  const handleInstructorChange = (event) => {
    setSelectedInstructor(event.target.value);
  };

  const handleChooseClass = async () => {
    // Ensure that a course and instructor are selected
    if (selectedCourse === "" || selectedInstructor === "Choose a class") {
      return;
    }

    try {
      // Fetch class information based on selected course and instructor
      const response = await fetch(
        `${BACKEND}/class/${encodeURIComponent(
          selectedCourse
        )}/${encodeURIComponent(selectedInstructor)}`
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

      let totalGrades = 0;

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
          totalGrades++;
        }
      }

      // Calculate the percentage for each grade in the fixed-length array
      const consolidatedGrades = gradesArray.map((g) => ({
        grade: g.grade,
        percentage: totalGrades > 0 ? (g.count / totalGrades) * 100 : 0,
      }));

      // Update the grade data state
      setGradeData(consolidatedGrades);
    } catch (error) {
      console.error("Error fetching grades:", error);
    }
  };

  useEffect(() => {
    // Fetch initial data for courses and set dummy grade data
    const fetchInitialData = async () => {
      setGradeData(dummyGradeData);
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
            // Normalize to lowercase (or another consistent format) to avoid case duplicates
            coursesSet.add(course.name.trim().toLowerCase());
          }
        });

        // Convert set back to an array and format class names if needed (e.g., capitalize)
        const sorted = Array.from(coursesSet)
          .map((name) => name.toUpperCase()) // Example formatting
          .sort();

        setCourses(sorted);
        setSelectedCourse(sorted[0]);
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };

    fetchInitialData();
  }, []);

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

    // Calculate the numerical values of valid grades
    const numericalGrades = gradeData
      .map(getGradeValue) // Convert each grade to its numerical value
      .filter((value) => value !== null); // Filter out unrecognized grades (null values)

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
            onChange={handleCourseChange}>
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
            onChange={handleInstructorChange}>
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
              barDataKey="percentage"
              barColor="#c4a55e"
            />
          </div>
        </div>

        {/* Course Information Section - Moved to the right */}
        <div className="course-info">
          <h2>{courseInfo.courseCode}</h2>
          <p>{courseInfo.name}</p>
          <p>
            {courseInfo.term} | Instructor: {courseInfo.teacher}
          </p>
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
