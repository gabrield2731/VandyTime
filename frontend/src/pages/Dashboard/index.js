import React from 'react';
import "./styles.css"; // Link to your CSS file for styling

const Dashboard = () => {
  // Hard-coded sample data
  const courses = [
    { code: 'CS 4278', professor: 'SINGH, V', grade: 'B' },
    { code: 'CS 1101', professor: 'BAI, R', grade: 'A' },
    { code: 'CS 2212', professor: 'HASAN, MD', grade: 'C' }
  ];

  return (
    <div className="container">
      <h1>Student Dashboard</h1>
      <div className="table-container">
        <table className="dashboard-table">
          <thead>
            <tr>
              <th>Course Name</th>
              <th>Professor</th>
              <th>Grade</th>
            </tr>
          </thead>
          <tbody>
            {courses.map((course, index) => (
              <tr key={index}>
                <td>{course.code}</td>
                <td>{course.professor}</td>
                <td>{course.grade}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
