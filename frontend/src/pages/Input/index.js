import React, { useEffect, useState } from "react";
import { useAuth } from "../../stores/firebase"; // Make sure this path is correct
import "./styles.css";

const BACKEND = process.env.REACT_APP_API_URL;

const grades = [
  "A+",
  "A",
  "A-",
  "B+",
  "B",
  "B-",
  "C+",
  "C",
  "C-",
  "D",
  "F",
  "P",
  "NP",
];

const Input = () => {
  const user = useAuth();

  const [courses, setCourses] = useState([]);
  const [professors, setProfessors] = useState([]);
  const [selectedProfessor, setSelectedProfessor] = useState("Select");
  const [selectedCourse, setSelectedCourse] = useState("Select");
  const [selectedGrade, setSelectedGrade] = useState("A+");
  const [year, setYear] = useState("2024");
  const [semester, setSemester] = useState("Fall");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const res = await fetch(
        `${BACKEND}/class/${encodeURIComponent(
          selectedCourse
        )}/${encodeURIComponent(selectedProfessor)}`
      );

      if (!res.ok) {
        throw new Error("Failed to fetch grades");
      }

      const data = await res.json();
      const classId = data._id;

      const userRes = await fetch(`${BACKEND}/student/fid/${user.uid}`);
      if (!userRes.ok) {
        throw new Error("Failed to fetch user");
      }
      const userData = await userRes.json();
      const userId = userData._id;

      if (userData.class_ids.includes(classId)) {
        window.alert("You have already submitted a grade for this class");
        setLoading(false);
        return;
      }

      const gradeRes = await fetch(`${BACKEND}/grade`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          class_id: classId,
          student_id: userId,
          grade: selectedGrade,
          year: year,
          semester: semester.toLowerCase(),
        }),
      });

      if (!gradeRes.ok) {
        throw new Error("Failed to post grade");
      }

      const gradeData = await gradeRes.json();
      console.log("Grade posted:", gradeData);
      setLoading(false);

      window.location.reload();
    } catch (error) {
      console.error("Error posting grade:", error);
    }
  };

  useEffect(() => {
    // Fetch initial data for courses and set dummy grade data
    const fetchInitialData = async () => {
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
    if (selectedCourse === "Select") return;

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
        setProfessors(sorted);
        setSelectedProfessor(sorted[0]);
      } catch (error) {
        console.error("Error fetching teachers:", error);
      }
    };

    fetchTeachers();
  }, [selectedCourse]);

  return (
    <>
      {user ? (
        user.emailVerified ? (
          <div className="container">
            <h1>Input</h1>
            <h3>Enter Your Class Data Below</h3>

            {/* Course Selector */}
            <div className="course-selector">
              <label htmlFor="course-select">Select Course: </label>
              <select
                id="course-select"
                value={selectedCourse}
                onChange={(event) => {
                  setSelectedCourse(event.target.value);
                  setSelectedProfessor("");
                }}>
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
                onChange={(event) => setSelectedProfessor(event.target.value)}>
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
                onChange={(event) => setSelectedGrade(event.target.value)}>
                {grades.map((grade) => (
                  <option key={grade} value={grade}>
                    {grade}
                  </option>
                ))}
              </select>
            </div>

            {/* Year Selector */}
            <div className="grade-selector">
              <label htmlFor="year-select">Year: </label>
              <select
                id="year-select"
                value={year}
                onChange={(e) => setYear(e.target.value)}>
                {Array.from(
                  { length: 10 },
                  (_, i) => new Date().getFullYear() - i
                ).map((yr) => (
                  <option key={yr} value={yr}>
                    {yr}
                  </option>
                ))}
              </select>
            </div>

            {/* Semester Selector */}
            <div className="grade-selector">
              <label htmlFor="semester-select">Semester: </label>
              <select
                id="semester-select"
                value={semester}
                onChange={(e) => setSemester(e.target.value)}>
                {["Fall", "Spring"].map((sem) => (
                  <option key={sem} value={sem}>
                    {sem}
                  </option>
                ))}
              </select>
            </div>

            {/* Submit Button */}
            <div className="button-container">
              <button onClick={handleSubmit} disabled={loading}>
                {loading ? "Loading..." : "Submit"}
              </button>
            </div>
          </div>
        ) : (
          <div
            style={{
              height: "100vh",
              display: "flex",
              "justify-content": "center",
              padding: "20px",
            }}>
            <h1>Please verify your email to access this page</h1>
          </div>
        )
      ) : (
        <div
          style={{
            height: "100vh",
            display: "flex",
            "justify-content": "center",
            padding: "20px",
          }}>
          <h1>Please log in to access this page</h1>
        </div>
      )}
    </>
  );
};

export default Input;
