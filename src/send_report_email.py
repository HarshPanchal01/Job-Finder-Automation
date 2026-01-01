import logging
import os
from datetime import datetime

from email_notification import EmailNotification


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def main() -> None:
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    receivers = os.getenv("EMAIL_RECEIVER", "")
    receiver_emails = [r.strip() for r in receivers.split(",") if r.strip()]

    github_issue_url = os.getenv("GITHUB_ISSUE_URL")

    report_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"Weekly Jobs Report - {report_date}"

    notifier = EmailNotification(
        smtp_server,
        smtp_port,
        sender_email,
        sender_password,
    )

    notifier.send_email(receiver_emails, subject, "jobs.md", github_issue_url=github_issue_url)


if __name__ == "__main__":
    main()
