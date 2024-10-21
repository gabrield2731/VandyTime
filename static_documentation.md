
# API Documentation

## Student Routes (`/student`)

- **GET /student/<student_id>**
  - Fetch a student by their ID.
  - Response: Returns the student data if found, else a 404 error.

- **GET /student/fid/<student_fid>**
  - Fetch a student by their faculty ID (FID).
  - Response: Returns the student data if found, else a 404 error.

- **POST /student/**
  - Create a new student.
  - Body: JSON containing the student data.
  - Response: Success message with the new student's ID.

- **PUT /student/<student_id>**
  - Update an existing student's information.
  - Body: JSON containing the updated data.
  - Response: Success or error message based on the update result.

- **DELETE /student/<student_id>**
  - Delete a student by their ID.
  - Response: Success or error message based on the deletion result.

---

## Grade Routes (`/grades`)

- **GET /grades/<grade_id>**
  - Fetch a grade by its ID.
  - Response: Returns the grade if found, else a 404 error.

- **POST /grades/**
  - Create a new grade.
  - Body: JSON containing the grade data.
  - Response: Success message with the new grade ID.

- **PUT /grades/<grade_id>**
  - Update an existing grade.
  - Body: JSON containing the updated data.
  - Response: Success or error message based on the update result.

- **DELETE /grades/<grade_id>**
  - Delete a grade by its ID.
  - Response: Success or error message based on the deletion result.

---

## Class Routes (`/class`)

- **GET /class/<class_id>**
  - Fetch a class by its ID.
  - Response: Returns the class data if found, else a 404 error.

- **POST /class/**
  - Create a new class.
  - Body: JSON containing the class details.
  - Response: Success message with the new class ID.

- **PUT /class/<class_id>**
  - Update a class.
  - Body: JSON containing the updated data.
  - Response: Success or error message based on the update result.

- **DELETE /class/<class_id>**
  - Delete a class by its ID.
  - Response: Success or error message based on the deletion result.

- **GET /class/**
  - Fetch all classes.
  - Response: Returns a list of all classes.

- **GET /class/<class_name>/teachers**
  - Fetch all teachers for a specific class by class name.
  - Response: Returns a list of teachers for the class.

- **GET /class/<class_name>/<teacher>**
  - Fetch a class by class name and teacher name.
  - Response: Returns the class if found, else a 404 error.

