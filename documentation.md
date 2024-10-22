## API Endpoints:

### `/class`
- **Method:** GET
- **Description:** Fetch a list of all classes.
- **Response:** Returns an array of class objects. Each class object should include at least the following fields: `name` (string), `code` (string), `semester` (string), and `teacher` (string).

### `/class/{courseName}/{instructorName}`
- **Method:** GET
- **Description:** Fetch detailed information about a specific class based on course name and instructor name.
- **Parameters:**
 - `{courseName}` (string): The name of the course (case-insensitive).
 - `{instructorName}` (string): The name of the instructor.
- **Response:** Returns a class object with the following fields: `code` (string), `name` (string), `description` (string), `semester` (string), `teacher` (string), and `grades` (array of grade IDs).

### `/grade/{gradeId}`
- **Method:** GET
- **Description:** Fetch details of a specific grade based on its ID.
- **Parameters:**
 - `{gradeId}` (string): The ID of the grade to fetch.
- **Response:** Returns a grade object with the following fields: `grade` (string - the letter grade), and any other relevant information.

### `/class/{courseName}/teachers`
- **Method:** GET
- **Description:** Fetch a list of teachers for a specific course.
- **Parameters:**
 - `{courseName}` (string): The name of the course (case-insensitive).
- **Response:** Returns an array of teacher names (strings) associated with the specified course.
