# API Endpoints

## /document

**Endpoint:** https://docubot-two.vercel.app/document

**Method:** POST

**Description:** This endpoint is used to generate documentation for changed files in a GitHub repository.

**Request Payload:**
- `repo_owner` (string): The owner of the GitHub repository.
- `repo` (string): The name of the GitHub repository.
- `files_changed` (array): A list of filenames that have changed in the repository.

**Response:**
- `updated_doc` (string): The updated documentation content.

**Example Curl Request:**
```bash
curl -X POST https://docubot-two.vercel.app/document \
 -H "Content-Type: application/json" \
 -d '{
 "repo_owner": "your_repo_owner",
 "repo": "your_repo_name",
 "files_changed": ["file1.txt", "file2.md"]
 }'
```
