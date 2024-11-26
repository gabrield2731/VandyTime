import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./styles.css"; // Import the CSS file

const BACKEND = process.env.REACT_APP_API_URL;

const Courses = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchProfessor, setSearchProfessor] = useState("");
  const [courseList, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  useEffect(() => {
    const filterCourses = () => {
      let filtered = courseList;

      if (searchTerm) {
        filtered = filtered.filter(
          (course) =>
            course.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
            course.name.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }

      if (searchProfessor) {
        filtered = filtered.filter((course) =>
          course.teacher.toLowerCase().includes(searchProfessor.toLowerCase())
        );
      }

      setFilteredCourses(filtered.sort((a, b) => a.code.localeCompare(b.code)));
    };

    filterCourses();
  }, [searchTerm, searchProfessor, courseList]);

  useEffect(() => {
    const fetchAllClasses = async () => {
      try {
        const response = await fetch(`${BACKEND}/class`);
        if (!response.ok) {
          throw new Error("Failed to fetch classes");
        }
        const data = await response.json();
        setCourses(data.sort((a, b) => a.code.localeCompare(b.code)));
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };
    fetchAllClasses();
  }, []);

  return (
    <div className="courses-container">
      <h1>Course List</h1>
      <div className="search-bar">
        <label htmlFor="course-search">Filter by Course: </label>
        <input
          id="course-search"
          type="text"
          placeholder="Search for a course by name or code"
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>
      <div className="search-bar">
        <label htmlFor="professor-search">Filter by Professor: </label>
        <input
          id="professor-search"
          type="text"
          placeholder="Search for a course by professor"
          value={searchProfessor}
          onChange={(e) => setSearchProfessor(e.target.value)}
        />
      </div>

      <div className="course-cards-container">
        {filteredCourses.length > 0 ? (
          filteredCourses.map((course) => (
            <div key={course._id} className="course-card">
              <Link
                to="/grades"
                state={{ code: course.name, teacher: course.teacher }}>
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
