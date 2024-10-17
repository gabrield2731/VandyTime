# API Endpoints Documentation

## Courses API

### Endpoint: /courses

- **GET:** Retrieve a list of all available courses.
 - Response: Array of Course objects.

### Endpoint: /courses/{courseId}

- **GET:** Fetch detailed information about a specific course.
 - Parameters:
 - courseId (string): The unique identifier of the course.
 - Response: Course object with detailed data.

### Endpoint: /courses/search

- **POST:** Search for courses based on various criteria.
 - Request Body:
 - searchQuery (string): Keyword or phrase to search for in course titles or descriptions.
 - category (string): Filter courses by category.
 - difficulty (string): Filter by course difficulty level.
 - Response: Array of Course objects matching the search criteria.

### Endpoint: /courses/enroll

- **POST:** Enroll a user in a specific course.
 - Request Body:
 - userId (number): The ID of the user enrolling.
 - courseId (string): The ID of the course to enroll in.
 - Response: Enrollment confirmation message and user's enrolled course data.

### Endpoint: /courses/reviews

- **GET:** Retrieve reviews and ratings for a specific course.
 - Parameters:
 - courseId (string): The unique identifier of the course.
 - Response: Array of Review objects for the course.

### Endpoint: /courses/reviews/submit

- **POST:** Submit a review and rating for a course.
 - Request Body:
 - userId (number): The ID of the user submitting the review.
 - courseId (string): The ID of the course being reviewed.
 - rating (number): Rating given by the user (e.g., 1-5).
 - reviewText (string): Written review content.
 - Response: Confirmation message and the submitted review data.
