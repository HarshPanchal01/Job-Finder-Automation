# Job-Finder-Automation

The goal of this repository is to fetch jobs from linkedin, glassdoor, indeed, based on parameters like job type, date posted, and more. The jobs should then be put into a list with their respective application links and sent through email.

## Configuration

You can configure the job search parameters using environment variables. This works for both local development (using a `.env` file) and GitHub Actions (using Repository Variables/Secrets).

| Variable        | Description                         | Default                    |
| --------------- | ----------------------------------- | -------------------------- |
| `API_KEY`       | **Required**. Your SerpApi API Key. | None                       |
| `SEARCH_QUERY`  | The search query for jobs.          | `new grad 2026 tech`       |
| `LOCATION`      | The location to search in.          | `Toronto, Ontario, Canada` |
| `GOOGLE_DOMAIN` | The Google domain to use.           | `google.ca`                |
| `GL`            | Country code for search results.    | `ca`                       |
| `HL`            | Language code for search results.   | `en`                       |

### Local Development

1. Create a `.env` file in the root directory.
2. Add your configuration:
   ```env
   API_KEY=your_api_key_here
   SEARCH_QUERY="software engineer intern"
   LOCATION="San Francisco, CA"
   ```

### GitHub Actions

1. Go to your repository settings -> **Secrets and variables** -> **Actions**.
2. Add `API_KEY` as a **Repository Secret**.
3. Add other parameters (e.g., `SEARCH_QUERY`, `LOCATION`) as **Repository Variables**.
