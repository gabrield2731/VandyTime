import React, { useEffect, useState } from "react";
import { useAuth } from "../../stores/firebase"; // Make sure this path is correct
import "./styles.css";

const BACKEND = process.env.REACT_APP_API_URL;

// Dummy list of courses

// Dummy list of professors for filtering
const p = ["RATNASAMY, S", "GARCIA, L", "KUBITZ, N", "LEE, H"];

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
  const [professors, setProfessors] = useState(p);
  const [selectedProfessor, setSelectedProfessor] = useState("Select");
  const [selectedCourse, setSelectedCourse] = useState("Select");
  const [selectedGrade, setSelectedGrade] = useState("Select");
  const [review, setReview] = useState("");

  const handleSubmit = async () => {
    try {
      const res = await fetch(
        `${BACKEND}/class/${encodeURIComponent(
          selectedCourse
        )}/${encodeURIComponent(selectedProfessor)}`
      );

      if (!res.ok) {
        throw new Error("Failed to fetch grades");
      }

      const data = await res.json();
      const classId = data.id;

      const userRes = await fetch(`${BACKEND}/user/fid/${user.uid}`);
      if (!userRes.ok) {
        throw new Error("Failed to fetch user");
      }
      const userData = await userRes.json();
      const userId = userData.id;

      const gradeRes = await fetch(`${BACKEND}/grade`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          classId,
          userId,
          grade: selectedGrade,
          review,
        }),
      });

      if (!gradeRes.ok) {
        throw new Error("Failed to post grade");
      }
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

            {/* Review Box */}
            <div className="review-box">
              <textarea
                id="user-input"
                value={review}
                onChange={(event) => setReview(event.target.value)}
                placeholder="Enter review"
                rows={5} // Start with multiple rows (adjust as needed)
              />
            </div>

            {/* Submit Button */}
            <div className="button-container">
              <button onClick={handleSubmit}>Submit</button>
            </div>
          </div>
        ) : (
          <h1>Please verify your email to access this page</h1>
        )
      ) : (
        <h1>Please log in to access this page</h1>
      )}
    </>
  );
};

export default Input;
