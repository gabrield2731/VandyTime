## /api-tests

**Endpoint:** https://api.example.com/api-tests

**Method:** POST

**Description:** Triggers API tests for a GitHub repository on push or pull request events.

**Request Payload:**
- `github_token` (string): A GitHub personal access token with repository access.
- `repository` (string): The full name of the GitHub repository (e.g., "owner/repo_name").
- `branch` (string): The branch to run tests against (optional, defaults to the main branch).

**Response:**
- `test_results` (object): An object containing test results and coverage data.
 - `success` (boolean): Indicates if all tests passed.
 - `coverage` (float): The code coverage percentage.
 - `report_url` (string): URL to the detailed test and coverage report.

**Example Curl Request:**
```bash
curl -X POST https://api.example.com/api-tests \
 -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
 -H "Content-Type: application/json" \
 -d '{
 "repository": "your_repo_owner/your_repo_name",
 "branch": "main"
 }'
```
