# Job Finder Automation

A Python-based automation tool that scrapes job listings from Google Jobs via SerpApi, filters them based on your preferences (salary, date, keywords), and generates a weekly report. It runs automatically via GitHub Actions or can be run locally using Docker or Python.

## Features

- **Automated Search**: Fetches jobs for multiple queries and locations.
- **Smart Filtering**:
  - **Salary**: Filters out jobs below a minimum salary.
  - **Date**: Ignores jobs older than $X$ days.
  - **Keywords**: Excludes jobs with specific keywords in the title.
  - **Companies**: Blacklists specific companies.
  - **Sources**: Filters for reputable sources (e.g., LinkedIn, Indeed).
- **Deduplication**: Tracks job history to ensure you never see the same job twice.
- **Reporting**: Generates a Markdown summary and a JSON data file.
- **Email Notifications**: Sends a full "Weekly Jobs Report" directly to your inbox with timestamped subjects.
- **CI/CD Integration**: Runs weekly on GitHub Actions, sending emails and archiving results in GitHub Issues.
- **Dockerized**: Consistent environment for development and deployment.

---

## Configuration

The application is configured using environment variables.

| Variable              | Description                                                 | Default                                                              |
| :-------------------- | :---------------------------------------------------------- | :------------------------------------------------------------------- |
| `API_KEY`             | **Required**. Your [SerpApi](https://serpapi.com/) API Key. | `None`                                                               |
| `SEARCH_QUERIES`      | List of job titles to search for.                           | `["software developer"]`                                             |
| `LOCATIONS`           | List of locations to search in.                             | `["Toronto, Ontario, Canada"]`                                       |
| `MAX_PAGES`           | Max pages to fetch per query/location.                      | `5`                                                                  |
| `MIN_SALARY`          | Minimum annual salary.                                      | `50000`                                                              |
| `MAX_DAYS_OLD`        | Max age of job posting in days.                             | `7`                                                                  |
| `BLACKLIST_COMPANIES` | Companies to exclude.                                       | `[]`                                                                 |
| `EXCLUDE_KEYWORDS`    | Keywords to exclude from titles.                            | `[]`                                                                 |
| `SCHEDULE_TYPES`      | Allowed schedule types (e.g., Full-time).                   | `["Full-time"]`                                                      |
| `TRUSTED_DOMAINS`     | Allowed application sources.                                | `["linkedin", "glassdoor", "indeed", "ziprecruiter", "simplyhired"]` |
| `GOOGLE_DOMAIN`       | Google domain to use.                                       | `google.ca`                                                          |
| `GL`                  | Country code.                                               | `ca`                                                                 |
| `HL`                  | Language code.                                              | `en`                                                                 |
| `EMAIL_ADDRESS`       | Sender email address for notifications.                     | `None`                                                               |
| `EMAIL_PASSWORD`      | App password/Secret for the sender email.                   | `None`                                                               |
| `EMAIL_RECEIVER`      | List of recipient emails (JSON list or comma-separated).    | Defaults to `EMAIL_ADDRESS`                                          |
| `SMTP_SERVER`         | SMTP server for sending emails.                             | `smtp.gmail.com`                                                     |
| `SMTP_PORT`           | SMTP port (usually 587 for TLS or 465 for SSL).             | `587`                                                                |

---

## Local Development

### Option 1: Using Docker (Recommended)

Docker ensures you run in the exact same environment as the GitHub Action.

1.  **Prerequisites**: Install Docker Desktop.
2.  **Build the Image**:
    ```bash
    docker build -t job-finder .
    ```
3.  **Run the Container**:
    Create a `.env` file with your config, then run:

    ```bash
    # Windows (Command Prompt)
    docker run --rm -v "%cd%:/app" --env-file .env job-finder

    # Windows (PowerShell)
    docker run --rm -v "${PWD}:/app" --env-file .env job-finder

    # Linux/WSL/Mac
    docker run --rm -v "$(pwd):/app" --env-file .env job-finder
    ```

    _The `-v` flag mounts your current directory so `jobs.md` and `jobs.json` are saved to your computer._

### Option 2: Using Python Directly

1.  **Prerequisites**: Python 3.11+
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure**: Create a `.env` file in the root directory.
    ```env
    API_KEY=your_serpapi_key
    EMAIL_ADDRESS=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    SEARCH_QUERIES=["python developer", "backend engineer"]
    LOCATIONS=["New York, NY"]
    ```
4.  **Run**:
    ```bash
    python src/main.py
    ```

---

## GitHub Actions Workflow

The project includes a workflow (`.github/workflows/job_finder.yml`) that automates the job search.

### How it Works

1.  **Schedule**: Runs automatically every Saturday at 14:00 UTC.
2.  **Environment**: Builds a Docker container to ensure reproducibility.
3.  **Execution**:
    - Fetches job history from a dedicated orphan branch (`job-history-data`).
    - Runs the search script.
    - Filters out jobs seen in previous runs.
4.  **Artifacts**:
    - `jobs.json`: Raw data of found jobs.
    - `jobs.md`: Formatted report.
5.  **Notification**: 
    - Sends a **Weekly Jobs Report** email to your specified receivers.
    - Creates a **GitHub Issue** as an archive of the weekly search results.
6.  **History Update**: Commits the new job IDs back to the `job-history-data` branch to prevent duplicates next week.

### Setup

1.  Go to **Settings** > **Secrets and variables** > **Actions**.
2.  Add `API_KEY` and `EMAIL_PASSWORD` as **Repository Secrets**.
3.  Add `EMAIL_ADDRESS`, `EMAIL_RECEIVER`, and other config (e.g., `SEARCH_QUERIES`) as **Repository Variables**.

---

## Search Logic & API

### SerpApi

This project uses the [SerpApi Google Jobs API](https://serpapi.com/google-jobs-api).

- **Engine**: `google_jobs`
- **Limits**: Be aware of your SerpApi plan limits. Each page of results counts as 1 search.
  - _Formula_: `(Queries * Locations * Max_Pages) = Total API Calls`

### Deduplication & Filtering

1.  **Intra-run**: Removes duplicates found within the same search session.
2.  **Inter-run**: Checks `data/history.json` to ensure you don't see the same job ID from last week.
3.  **Quality Filters**:
    - **Regex Matching**: Ensures keywords like "lead" don't accidentally filter "Leading Company".
    - **Source Validation**: Prioritizes direct company sites or trusted boards (LinkedIn, Indeed) over spammy aggregators.

---

## Contribution

Contributions are welcome!

1.  **Fork** the repository.
2.  **Create a branch** (`git checkout -b feature/amazing-feature`).
3.  **Commit** your changes.
4.  **Push** to the branch.
5.  **Open a Pull Request**.

### Adding New Queries/Locations

You don't need to change code! Just update your `.env` file or GitHub Repository Variables.

---

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.
