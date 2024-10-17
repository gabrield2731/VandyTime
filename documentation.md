## /student

**Endpoint:** `${process.env.REACT_APP_API_URL}/student`

**Method:** POST

**Description:** This endpoint is used to create a new student user in the database.

**Request Payload:**
- `email` (string): The email address of the student.
- `firebase_id` (string): The Firebase ID of the student.

**Response:**
- `data` (JSON): The response data containing information about the created student.

**Example Request:**
```javascript
const email = "student@vanderbilt.edu";
const f_id = "firebase_id_123";

fetch(`${process.env.REACT_APP_API_URL}/student`, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({
 email,
 firebase_id: f_id,
 }),
})
 .then(response => response.json())
 .then(data => console.log(data))
 .catch(error => console.error(error));
```
