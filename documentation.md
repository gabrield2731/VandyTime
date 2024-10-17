## API Endpoints for Class Management:

### 1. Get Class by ID:
- Endpoint: `/<class_id>`
- Method: `GET`
- Parameters:
 - `class_id` (str): The ID of the class to retrieve.
- Response:
 - Returns a JSON object containing class information on success with a 200 status code.
 - Returns a JSON error message with a 404 status code if the class is not found.

### 2. Create a New Class:
- Endpoint: `/`
- Method: `POST`
- Request Body:
 - `class_data` (JSON): Data for the new class, including relevant details.
- Response:
 - Returns a JSON message with the ID of the created class and a 201 status code on successful creation.
 - Note: The current implementation is broken and needs to be fixed in the `create_class` function.

### 3. Update Class Details:
- Endpoint: `/<class_id>`
- Method: `PUT`
- Parameters:
 - `class_id` (str): The ID of the class to update.
- Request Body:
 - `update_data` (JSON): Updated class details.
- Response:
 - Returns a JSON success message with a 200 status code if the class is updated.
 - Returns a JSON error message with a 400 status code if no changes are made.
 - Note: The current implementation is broken and needs to be fixed in the `update_class` function.

### 4. Delete a Class:
- Endpoint: `/<class_id>`
- Method: `DELETE`
- Parameters:
 - `class_id` (str): The ID of the class to delete.
- Response:
 - Returns a JSON success message with a 200 status code if the class is deleted.
 - Returns a JSON error message with a 404 status code if the class is not found.
 - Note: The current implementation is broken and needs to be fixed in the `delete_class` function.
