## API Endpoints:

### `/class`
- **Method:** GET
- **Description:** Fetch a list of all classes.
- **Response:** Returns an array of class objects.

### `/class/{course}/{instructor}`
- **Method:** GET
- **Description:** Fetch information about a specific class based on course and instructor.
- **Parameters:**
 - `{course}`: String - The course code or name.
 - `{instructor}`: String - The instructor's name.
- **Response:** Returns an object containing class information, including grades.

### `/grade/{gradeId}`
- **Method:** GET
- **Description:** Fetch details of a specific grade by its ID.
- **Parameters:**
 - `{gradeId}`: String - The ID of the grade.
- **Response:** Returns an object containing grade details.

### `/class/{course}/teachers`
- **Method:** GET
- **Description:** Fetch a list of teachers for a specific course.
- **Parameters:**
 - `{course}`: String - The course code or name.
- **Response:** Returns an array of teacher names.
