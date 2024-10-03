# API Endpoints Documentation

## /document

**Endpoint:** `POST https://docubot-two.vercel.app/document`

**Description:** This endpoint is used to generate documentation for changed files in a GitHub repository. It takes a JSON payload as input and returns an updated documentation string.

**Request Payload:**
- `repo_owner` (string): The owner of the GitHub repository.
- `repo` (string): The name of the repository.
- `files_changed` (array): A list of filenames that have changed in the repository.

**Response:**
- `updated_doc` (string): The generated documentation content for the changed files.

**Example Curl Request:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
 "repo_owner": "your_repo_owner",
 "repo": "your_repo_name",
 "files_changed": ["file1.txt", "file2.md"]
}' https://docubot-two.vercel.app/document
```
