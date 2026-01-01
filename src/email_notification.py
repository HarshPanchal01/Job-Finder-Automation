import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotification:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, receiver_emails, subject, body_file_path):
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
                msg = MIMEMultipart()
                msg['From'] = self.sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body_content, 'plain'))
                
                text = msg.as_string()
                server.sendmail(self.sender_email, receiver_email, text)
                logging.info(f"Email sent successfully to {receiver_email}")
            
            server.quit()
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
