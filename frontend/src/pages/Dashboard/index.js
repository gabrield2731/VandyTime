import React, { useEffect, useState } from "react";
import { useAuth } from "../../stores/firebase"; // Make sure this path is correct
import "./styles.css"; // Link to your CSS file for styling

const BACKEND = process.env.REACT_APP_API_URL;

const gradeOptions = [
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

const Dashboard = () => {
  const user = useAuth();
  const [grades, setGrades] = useState([]);
  const [editingGrade, setEditingGrade] = useState(null);
  const [newGrade, setNewGrade] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (!user) throw new Error("User is not authenticated");

        setLoading(true);

        const res = await fetch(`${BACKEND}/student/fid/${user.uid}`);
        if (!res.ok) throw new Error("Failed to fetch courses");
        const data = await res.json();

        const gradePromises = data.grades.map(async (gradeId) => {
          const gradeRes = await fetch(`${BACKEND}/grade/${gradeId}`);
          if (!gradeRes.ok) throw new Error("Failed to fetch grade");
          const gradeData = await gradeRes.json();

          const courseRes = await fetch(
            `${BACKEND}/class/${gradeData.class_id}`
          );
          if (!courseRes.ok) throw new Error("Failed to fetch course");
          const courseData = await courseRes.json();

          return {
            _id: gradeData._id,
            course: courseData.name,
            professor: courseData.teacher,
            grade: gradeData.grade,
            year: gradeData.year,
            semester: gradeData.semester,
          };
        });

        // Wait for all grade promises to resolve
        const resolvedGrades = await Promise.all(gradePromises);

        // Sort and update the grades state
        setGrades(
          resolvedGrades.sort((a, b) => {
            if (a.year === b.year) {
              if (a.semester === b.semester) {
                if (a.professor === b.professor) {
                  return a.grade.localeCompare(b.grade);
                }
                return a.professor.localeCompare(b.professor);
              }
              return a.semester.localeCompare(b.semester);
            }
            return a.year - b.year;
          })
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false); // Always stop loading
      }
    };

    fetchData();
  }, [user]);

  const handleEditClick = (gradeId, currentGrade) => {
    setEditingGrade(gradeId);
    setNewGrade(currentGrade);
  };

  const handleSaveClick = async (gradeId) => {
    try {
      const response = await fetch(`${BACKEND}/grade/${gradeId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ grade: newGrade }),
      });
      if (!response.ok) throw new Error("Failed to update grade");

      setGrades((grades) =>
        grades.map((grade) =>
          grade._id === gradeId ? { ...grade, grade: newGrade } : grade
        )
      );
      setEditingGrade(null);
      setNewGrade("");
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteClick = async (gradeId) => {
    try {
      if (!window.confirm("Are you sure you want to delete this grade?")) {
        return;
      }
      const response = await fetch(`${BACKEND}/grade/${gradeId}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete grade");

      // Refresh the page after successful deletion
      window.location.reload();
    } catch (error) {
      console.error("Error deleting grade:", error);
    }
  };

  return (
    <>
      {user ? (
        user.emailVerified ? (
          <div className="container">
            <h1>Student Dashboard</h1>
            <div className="table-container">
              <table className="dashboard-table">
                <thead>
                  <tr>
                    <th>Course Name</th>
                    <th>Professor</th>
                    <th>Grade</th>
                    <th>Year</th>
                    <th>Semester</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan="6">Loading...</td>
                    </tr>
                  ) : (
                    grades.map((grade) => (
                      <tr key={grade._id}>
                        <td>{grade.course}</td>
                        <td>{grade.professor}</td>
                        <td>
                          {editingGrade === grade._id ? (
                            <select
                              value={newGrade}
                              onChange={(e) => setNewGrade(e.target.value)}>
                              {gradeOptions.map((option) => (
                                <option key={option} value={option}>
                                  {option}
                                </option>
                              ))}
                            </select>
                          ) : (
                            grade.grade
                          )}
                        </td>
                        <td>{grade.year}</td>
                        <td>{grade.semester.toUpperCase()}</td>
                        <td>
                          {editingGrade === grade._id ? (
                            <>
                              <button
                                onClick={() => handleSaveClick(grade._id)}>
                                Save
                              </button>
                              <button onClick={() => setEditingGrade(null)}>
                                Cancel
                              </button>
                            </>
                          ) : (
                            <>
                              <button
                                onClick={() =>
                                  handleEditClick(grade._id, grade.grade)
                                }>
                                Edit
                              </button>
                              <button
                                onClick={() => handleDeleteClick(grade._id)}>
                                Delete
                              </button>
                            </>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div
            style={{
              height: "100vh",
              display: "flex",
              justifyContent: "center",
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
            justifyContent: "center",
            padding: "20px",
          }}>
          <h1>Please log in to access this page</h1>
        </div>
      )}
    </>
  );
};

export default Dashboard;
