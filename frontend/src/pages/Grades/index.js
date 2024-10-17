import React, { useEffect, useState } from "react";
import BarChartComponent from "../../components/BarChart";
import "./styles.css";

const BACKEND = process.env.BACKEND_URL;

const dummyGradeData = [
  { grade: "A+", percentage: 0 },
  { grade: "A", percentage: 0 },
  { grade: "A-", percentage: 0 },
  { grade: "B+", percentage: 0 },
  { grade: "B", percentage: 0 },
  { grade: "B-", percentage: 0 },
  { grade: "C+", percentage: 0 },
  { grade: "C", percentage: 0 },
  { grade: "C-", percentage: 0 },
  { grade: "D", percentage: 0 },
  { grade: "F", percentage: 0 },
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

  const handleChooseClass = () => {
    // fetch classes info when selected
    if (selectedCourse === "" || selectedInstructor === "Choose a class") {
      return;
    }
    fetch(
      `${BACKEND}/grades?course=${selectedCourse}&instructor=${selectedInstructor}`
    )
      .then((response) => response.json())
      .then((data) => {
        setCourseInfo(data.courseInfo);
      })
      .catch((error) => {
        console.error("Error fetching grades:", error);
      });
  };

  useEffect(() => {
    // initially get courses and set dummy grade data
    setGradeData(dummyGradeData);
    fetch(`${BACKEND}/courses`)
      .then((response) => response.json())
      .then((data) => {
        setCourses(data.courses);
      })
      .catch((error) => {
        console.error("Error fetching courses:", error);
      });
  }, []);

  useEffect(() => {
    // Fetch teachers based on selected course
    fetch(`${BACKEND}/teachers`)
      .then((response) => response.json())
      .then((data) => {
        setTeachers(data.teachers);
      })
      .catch((error) => {
        console.error("Error fetching teachers:", error);
      });
  }, [courseInfo]);

  useEffect(() => {
    //add grades to gradeData may need to do some manipuation here
    //setGradeData(courseInfo.grades);
    //calculate average and calculate it
    let new_average = "A+";
    setAverage(new_average)
  }, [courseInfo]);

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
          <button onClick={handleChooseClass}>Add Class</button>
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
          <p>{courseInfo.courseName}</p>
          <p>
            {courseInfo.term} | Instructor: {courseInfo.instructor}
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
