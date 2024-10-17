import React, { useState } from "react";


  // const user = useAuth(); // This will give you the current Firebase user
  const courseList = [
    {
      courseCode: "COMPSCI 168",
      courseName: "Introduction to the Internet: Architecture and Protocols",
      professor:"Elena",
      department:"Computer Science"
    },
    { courseCode: "COMPSCI 161", 
      courseName: "Data Structures and Algorithms" ,
      professor: "Bob",
      department:"Computer Science"},
    {
      courseCode: "COMPSCI 162",
      courseName: "Operating Systems and System Programming",
      professor: "Dave",
      department:"Computer Science"
    },
    { courseCode: "COMPSCI 169", 
      courseName: "Software Engineering" ,
      professor: "Stuart",
      department:"Computer Science"
    },
    {
      courseCode: "PHYS 1600",
      courseName: "Introductory Physics 1",
      professor:"Elena",
      department:"Physics"
    },
    {
      courseCode: "PHYS 1700",
      courseName: "Introductory Physics 2",
      professor:"Dave",
      department:"Physics"
    },
    {
      courseCode: "PHYS 1800",
      courseName: "Int Physics 3",
      professor:"Stuart",
      department:"Physics"
    },
    {
      courseCode: "PHYS 1900",
      courseName: "Advanced Physics 4",
      professor:"Bob",
      department:"Physics"
    }
  ];

    const departments = ["All", "Computer Science", "Mathematics", "Physics"];
    const professors = ["All", "RATNASAMY, S", "GARCIA, L", "KUBITZ, N", "LEE, H"];
    
const Courses = () => {    
  // define use states
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProfessor, setSelectedProfessor] = useState("All");
  const [selectedDepartment, setSelectedDepartment] = useState("All");

  const departments = ["All", "Computer Science", "Mathematics", "Physics"];
  const professors = ["All", "RATNASAMY, S", "GARCIA, L", "KUBITZ, N", "LEE, H"];
  
  // Handle changes in the search input
  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  // Handle changes in professor and department filters
  const handleProfessorChange = (event) => {
    setSelectedProfessor(event.target.value);
  };

  const handleDepartmentChange = (event) => {
    setSelectedDepartment(event.target.value);
  };

   // Filter the courses based on the search term, professor, and department
   const filteredCourses = courseList.filter((course) => {
    const matchesSearch = course.courseName.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          course.courseCode.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesProfessor = selectedProfessor === "All" || course.professor === selectedProfessor;
    const matchesDepartment = selectedDepartment === "All" || course.department === selectedDepartment;

    return matchesSearch && matchesProfessor && matchesDepartment;
  });
  
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
          style={{ padding: "10px", width: "300px", borderRadius: "5px", border: "1px solid #ccc" }}
        />
      </div>

      {/* Filters Section */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
        {/* Professor Filter */}
        <div>
          <label htmlFor="professor-select">Filter by Professor: </label>
          <select id="professor-select" value={selectedProfessor} onChange={handleProfessorChange}>
            {professors.map((professor) => (
              <option key={professor} value={professor}>
                {professor}
              </option>
            ))}
          </select>
        </div>

        {/* Department Filter */}
        <div>
          <label htmlFor="department-select">Filter by Department: </label>
          <select id="department-select" value={selectedDepartment} onChange={handleDepartmentChange}>
            {departments.map((department) => (
              <option key={department} value={department}>
                {department}
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
              
              <a href="/grades" >{course.courseCode}</a>
              <p>{course.courseName}</p>
              <p><strong>Professor:</strong> {course.professor}</p>
              <p><strong>Department:</strong> {course.department}</p>
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