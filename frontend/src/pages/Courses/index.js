import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const BACKEND = process.env.REACT_APP_API_URL;

const Courses = () => {
  // Define use states
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProfessor, setSelectedProfessor] = useState("All");
  const [professors, setProfessors] = useState([]);
  const [courseList, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);

  // Handle changes in the search input
  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  // Handle changes in professor filter
  const handleProfessorChange = (event) => {
    setSelectedProfessor(event.target.value);
  };

  // Function to filter courses based on search term and professor
  useEffect(() => {
    const filterCourses = () => {
      let filtered = courseList;

      // Filter by search term (course code or course name)
      if (searchTerm) {
        filtered = filtered.filter(
          (course) =>
            course.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
            course.name.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }

      // Filter by selected professor (if not "All")
      if (selectedProfessor !== "All") {
        filtered = filtered.filter(
          (course) => course.teacher === selectedProfessor
        );
      }

      setFilteredCourses(filtered);
    };

    filterCourses();
  }, [searchTerm, selectedProfessor, courseList]);

  useEffect(() => {
    // Fetch the list of all classes from the backend and set courseList
    const fetchAllClasses = async () => {
      try {
        const response = await fetch(`${BACKEND}/class`);
        if (!response.ok) {
          throw new Error("Failed to fetch classes");
        }
        const data = await response.json();
        console.log(data);
        setCourses(data);
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };
    fetchAllClasses();

    // Fetch the list of all professors from the backend and set professors
    const fetchAllProfessors = async () => {
      try {
        const response = await fetch(`${BACKEND}/class/allTeachers`);
        if (!response.ok) {
          throw new Error("Failed to fetch professors");
        }
        const data = await response.json();
        setProfessors(["All", ...data]);
      } catch (error) {
        console.error("Error fetching professors:", error);
      }
    };
    fetchAllProfessors();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Course List</h1>

      {/* Search Bar */}
      <div style={{ marginBottom: "20px" }}>
      <label htmlFor="professor-select">Filter by Course: </label>
        <input
          type="text"
          placeholder="Search for a course by name or code"
          value={searchTerm}
          onChange={handleSearchChange}
          style={{
            padding: "10px",
            width: "300px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />
      </div>

      {/* Filters Section */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
        {/* Professor Filter */}
        <div>
          <label htmlFor="professor-select">Filter by Professor: </label>
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
      </div>

      {/* Course Cards */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {filteredCourses.length > 0 ? (
          filteredCourses.map((course) => (
            <div
              key={course._id}
              style={{
                border: "1px solid #ccc",
                borderRadius: "10px",
                padding: "20px",
                width: "300px",
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                backgroundColor: "#f9f9f9",
              }}
            >
              {/* TODO: Make it so the grades page has access to the courseCode and teacher so it can query when there */}
              <Link
                to="/grades"
                state={{ code: course.name, teacher: course.teacher }}
              >
                {course.code}
              </Link>
              <p>{course.name}</p>
              <p>
                <strong>Professor:</strong> {course.teacher}
              </p>
            </div>
          ))
        ) : (
          <p>No courses found.</p>
        )}
      </div>
    </div>
  );
};

export default Courses;
