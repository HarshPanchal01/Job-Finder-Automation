import smtplib
import logging
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown

class EmailNotification:
    @staticmethod
    def markdown_to_html(markdown_text: str) -> str:
        # Email clients (notably Gmail) either don't support <details>/<summary>
        # or render markdown inside them poorly. Convert them into normal markdown
        # so python-markdown can render headings/lists/links properly.
        processed = re.sub(r"\s*<details>\s*", "\n\n", markdown_text)
        processed = re.sub(r"\s*</details>\s*", "\n\n", processed)
        processed = re.sub(
            r"<summary>(.*?)</summary>",
            lambda m: f"\n\n**{m.group(1).strip()}**\n\n",
            processed,
            flags=re.IGNORECASE | re.DOTALL,
        )

        return markdown.markdown(
            processed,
            extensions=[
                "tables",
                "fenced_code",
                "sane_lists",
            ],
        )

    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, receiver_emails, subject, body_file_path, github_issue_url: str | None = None):
        """
        Reads the content of the file at body_file_path and sends it to each email in receiver_emails.
        receiver_emails can be a string or a list of strings.
        """
        if not self.sender_email or not self.sender_password:
            logging.warning("Email credentials not provided. Skipping email notification.")
            return

        if not os.path.exists(body_file_path):
            logging.error(f"File to send not found: {body_file_path}")
            return

        try:
            with open(body_file_path, 'r', encoding='utf-8') as f:
                body_content = f.read()
        except Exception as e:
            logging.error(f"Failed to read file {body_file_path}: {e}")
            return

        if github_issue_url:
            body_content = f"[View on GitHub]({github_issue_url})\n\n" + body_content

        html_body = self.markdown_to_html(body_content)
        html_doc = (
            "<!doctype html>"
            "<html><head><meta charset='utf-8'></head><body>"
            f"{html_body}"
            "</body></html>"
        )

        # Normalize to list
        if isinstance(receiver_emails, str):
            receiver_emails = [receiver_emails]
        
        if not receiver_emails:
            logging.warning("No receiver emails provided. Skipping email notification.")
            return

        try:
            logging.info(f"Connecting to SMTP server {self.smtp_server}:{self.smtp_port}...")
            # Use SMTP_SSL if port 465, else use starttls
            if self.smtp_port == 465:
                 server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            
            server.login(self.sender_email, self.sender_password)

            for receiver_email in receiver_emails:
                msg = MIMEMultipart('alternative')
                msg['From'] = self.sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject

                msg.attach(MIMEText(body_content, 'plain', 'utf-8'))
                msg.attach(MIMEText(html_doc, 'html', 'utf-8'))
                
                text = msg.as_string()
                server.sendmail(self.sender_email, receiver_email, text)
                logging.info(f"Email sent successfully to {receiver_email}")
            
            server.quit()
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
