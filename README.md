# Job-Finder-Automation

The goal of this repository is to fetch jobs from google search based on parameters like job type, date posted, and more. The jobs should then be put into a list with their respective application links and sent through email.

## Configuration

You can configure the job search parameters using environment variables. This works for both local development (using a `.env` file) and GitHub Actions (using Repository Variables/Secrets).

| Variable              | Description                                                                                                           | Default                    |
| --------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `API_KEY`             | **Required**. Your SerpApi API Key.                                                                                   | None                       |
| `SEARCH_QUERIES`      | List of search queries (JSON list or comma-separated).                                                                | `["software developer"]`   |
| `LOCATIONS`           | A JSON list of locations or a single string. e.g. `["Toronto, Ontario, Canada", "New York, New York, United States"]` | `Toronto, Ontario, Canada` |
| `MAX_PAGES`           | Maximum number of pages to fetch per location.                                                                        | `5`                        |
| `MIN_SALARY`          | Minimum annual salary to filter jobs. Jobs with unknown salary are kept.                                              | `50000`                    |
| `MAX_DAYS_OLD`        | Maximum age of job postings in days. Jobs older than this will be filtered out.                                       | `7`                        |
| `BLACKLIST_COMPANIES` | List of companies to exclude (JSON list or comma-separated).                                                          | `[]`                       |
| `EXCLUDE_KEYWORDS`    | List of keywords to exclude from job titles (JSON list or comma-separated).                                           | `[]`                       |
| `SCHEDULE_TYPES`      | List of allowed schedule types (JSON list or comma-separated). e.g. `["Full-time", "Part-time"]`                      | `["Full-time"]`            |
| `GOOGLE_DOMAIN`       | The Google domain to use.                                                                                             | `google.ca`                |
| `GL`                  | Country code for search results.                                                                                      | `ca`                       |
| `HL`                  | Language code for search results.                                                                                     | `en`                       |

### Local Development

1. Create a `.env` file in the root directory.
2. Add your configuration:
   ```env
   API_KEY=your_api_key_here
   SEARCH_QUERIES=["software engineer intern", "backend developer"]
   LOCATIONS=["San Francisco, California, United States", "New York, New York, United States"]
   MAX_PAGES=3
   ```

### GitHub Actions

1. Go to your repository settings -> **Secrets and variables** -> **Actions**.
2. Add `API_KEY` as a **Repository Secret**.
3. Add other parameters (e.g., `SEARCH_QUERIES`, `LOCATIONS`) as **Repository Variables**.
   - For `LOCATIONS`, you can enter a JSON array like `["City A, State, Country", "City B, State, Country"]`.
