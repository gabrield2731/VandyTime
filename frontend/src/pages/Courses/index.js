import React, { useEffect, useState } from "react";

// const user = useAuth(); // This will give you the current Firebase user
const classList = [
  {
    courseCode: "CS 1101",
    courseName: "Introduction to the Internet: Architecture and Protocols",
    professor: "Elena",
  },
  {
    courseCode: "CS 2201",
    courseName: "Data Structures and Algorithms",
    professor: "Bob",
  },
  {
    courseCode: "CS 3251",
    courseName: "Operating Systems and System Programming",
    professor: "Dave",
  },
  {
    courseCode: "CS 3270",
    courseName: "Software Engineering",
    professor: "Stuart",
  },
];

const Courses = () => {
  // define use states
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProfessor, setSelectedProfessor] = useState("All");
  const [professors, setProfessors] = useState([
    "All",
    "Elena",
    "Bob",
    "Dave",
    "Stuart",
  ]);
  const [courseList, setCourses] = useState(classList);

  // Handle changes in the search input
  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  // Handle changes in professor and department filters
  const handleProfessorChange = (event) => {
    setSelectedProfessor(event.target.value);
  };

  // Filter the courses based on the search term, professor, and department
  const filteredCourses = courseList.filter((course) => {
    const matchesSearch =
      course.courseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      course.courseCode.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesProfessor =
      selectedProfessor === "All" || course.professor === selectedProfessor;

    return matchesSearch && matchesProfessor;
  });

  useEffect(() => {
    // TODO:
    // Fetch the list of all classes from the backend and set classLis to this value (may need to format data to fit current format)
    setCourses(classList);
    // TODO:
    // Fetch the list of all professors from the backend and set professors to this value
    setProfessors(["All", "Elena", "Bob", "Dave", "Stuart"]);
  } , []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Course List</h1>

      {/* Search Bar */}
      <div style={{ marginBottom: "20px" }}>
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
              key={course.courseCode}
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
              <a href="/grades" style={{color: "#0000EE"}}>{course.courseCode}</a>
              <p>{course.courseName}</p>
              <p>
                <strong>Professor:</strong> {course.professor}
              </p>
            </div>
          ))
        ) : (
          <p>No courses found</p>
        )}
      </div>
    </div>
  );
};

export default Courses;