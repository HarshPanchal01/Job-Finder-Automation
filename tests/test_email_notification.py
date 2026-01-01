import pytest
from unittest.mock import MagicMock, patch, mock_open
from email import message_from_string
from email_notification import EmailNotification

@pytest.fixture
def email_notifier():
    return EmailNotification("smtp.test.com", 587, "sender@test.com", "password")

def test_send_email_success(email_notifier):
    """Test successful email sending."""
    with (
        patch("builtins.open", mock_open(read_data="Test Body")),
        patch("smtplib.SMTP") as MockSMTP,
        patch("os.path.exists", return_value=True)
    ):
        
        mock_smtp_instance = MockSMTP.return_value
        
        email_notifier.send_email("receiver@test.com", "Subject", "test_file.md")
        
        MockSMTP.assert_called_with("smtp.test.com", 587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_with("sender@test.com", "password")
        mock_smtp_instance.sendmail.assert_called_once()

        sent_message = mock_smtp_instance.sendmail.call_args.args[2]
        parsed = message_from_string(sent_message)
        assert parsed.get_content_type() == "multipart/alternative"

        parts = parsed.get_payload()
        assert len(parts) == 2
        assert parts[0].get_content_type() == "text/plain"
        assert parts[1].get_content_type() == "text/html"

        html_bytes = parts[1].get_payload(decode=True)
        html_text = html_bytes.decode("utf-8")
        assert "<!doctype html>" in html_text
        assert "Test Body" in html_text
        mock_smtp_instance.quit.assert_called_once()

def test_send_email_ssl(email_notifier):
    """Test successful email sending using SSL (port 465)."""
    email_notifier.smtp_port = 465
    with (
        patch("builtins.open", mock_open(read_data="Test Body")),
        patch("smtplib.SMTP_SSL") as MockSMTP_SSL,
        patch("os.path.exists", return_value=True)
    ):
        
        mock_smtp_instance = MockSMTP_SSL.return_value
        
        email_notifier.send_email("receiver@test.com", "Subject", "test_file.md")
        
        MockSMTP_SSL.assert_called_with("smtp.test.com", 465)
        # starttls is not called for SSL
        mock_smtp_instance.login.assert_called_with("sender@test.com", "password")
        mock_smtp_instance.sendmail.assert_called_once()

        sent_message = mock_smtp_instance.sendmail.call_args.args[2]
        parsed = message_from_string(sent_message)
        assert parsed.get_content_type() == "multipart/alternative"

        parts = parsed.get_payload()
        assert len(parts) == 2
        assert parts[0].get_content_type() == "text/plain"
        assert parts[1].get_content_type() == "text/html"

        html_bytes = parts[1].get_payload(decode=True)
        html_text = html_bytes.decode("utf-8")
        assert "<!doctype html>" in html_text
        assert "Test Body" in html_text

def test_send_email_multiple_receivers(email_notifier):
    """Test sending email to multiple receivers."""
    receivers = ["rec1@test.com", "rec2@test.com"]
    with (
        patch("builtins.open", mock_open(read_data="Test Body")),
        patch("smtplib.SMTP") as MockSMTP,
        patch("os.path.exists", return_value=True)
    ):
        email_notifier.send_email(receivers, "Subject", "test_file.md")
        
        mock_smtp_instance = MockSMTP.return_value
        # sendmail should be called twice
        assert mock_smtp_instance.sendmail.call_count == 2
        
        calls = mock_smtp_instance.sendmail.call_args_list
        assert calls[0].args[1] == "rec1@test.com"
        assert calls[1].args[1] == "rec2@test.com"

        parsed_1 = message_from_string(calls[0].args[2])
        parsed_2 = message_from_string(calls[1].args[2])
        assert parsed_1.get_content_type() == "multipart/alternative"
        assert parsed_2.get_content_type() == "multipart/alternative"

        assert parsed_1.get_payload()[1].get_content_type() == "text/html"
        assert parsed_2.get_payload()[1].get_content_type() == "text/html"


def test_send_email_markdown_tables_render_to_html(email_notifier):
    """Ensure markdown tables become HTML tables for email clients like Gmail."""
    markdown_body = "# Title\n\n| a | b |\n| - | - |\n| 1 | 2 |\n"

    with (
        patch("builtins.open", mock_open(read_data=markdown_body)),
        patch("smtplib.SMTP") as MockSMTP,
        patch("os.path.exists", return_value=True)
    ):
        mock_smtp_instance = MockSMTP.return_value
        email_notifier.send_email("receiver@test.com", "Subject", "test_file.md")

        sent_message = mock_smtp_instance.sendmail.call_args.args[2]
        parsed = message_from_string(sent_message)
        html_part = parsed.get_payload()[1]
        assert html_part.get_content_type() == "text/html"

        html_bytes = html_part.get_payload(decode=True)
        html_text = html_bytes.decode("utf-8")
        assert "<table" in html_text


def test_send_email_details_summary_are_preprocessed(email_notifier):
    """<details>/<summary> blocks should not break markdown rendering in email HTML."""
    md = (
        "<details>\n"
        "<summary>Click to view 1 job</summary>\n\n"
        "#### Role\n"
        "- [**Apply Now**](https://example.com/apply)\n"
        "</details>\n"
    )

    with (
        patch("builtins.open", mock_open(read_data=md)),
        patch("smtplib.SMTP") as MockSMTP,
        patch("os.path.exists", return_value=True),
    ):
        mock_smtp_instance = MockSMTP.return_value
        email_notifier.send_email("receiver@test.com", "Subject", "test_file.md")

        sent_message = mock_smtp_instance.sendmail.call_args.args[2]
        parsed = message_from_string(sent_message)
        html_part = parsed.get_payload()[1]
        html_text = html_part.get_payload(decode=True).decode("utf-8")

        # Should render a real anchor with short text, not a raw URL or markdown.
        assert "<a" in html_text
        assert ">Apply Now<" in html_text
        assert "https://example.com/apply" in html_text


def test_send_email_includes_view_on_github_link(email_notifier):
    with (
        patch("builtins.open", mock_open(read_data="# Report\n")),
        patch("smtplib.SMTP") as MockSMTP,
        patch("os.path.exists", return_value=True),
    ):
        mock_smtp_instance = MockSMTP.return_value
        email_notifier.send_email(
            "receiver@test.com",
            "Subject",
            "test_file.md",
            github_issue_url="https://github.com/org/repo/issues/123",
        )

        sent_message = mock_smtp_instance.sendmail.call_args.args[2]
        parsed = message_from_string(sent_message)
        html_part = parsed.get_payload()[1]
        html_text = html_part.get_payload(decode=True).decode("utf-8")

        assert "View on GitHub" in html_text
        assert "https://github.com/org/repo/issues/123" in html_text

def test_send_email_missing_credentials():
    """Test that email is skipped if credentials are missing."""
    notifier = EmailNotification("smtp.test.com", 587, None, None)
    
    with patch("smtplib.SMTP") as MockSMTP:
        notifier.send_email("receiver@test.com", "Subject", "test_file.md")
        MockSMTP.assert_not_called()

def test_send_email_file_not_found(email_notifier):
    """Test handling of missing body file."""
    with (
        patch("os.path.exists", return_value=False),
        patch("smtplib.SMTP") as MockSMTP
    ):
        
        email_notifier.send_email("receiver@test.com", "Subject", "missing.md")
        
        MockSMTP.assert_not_called()

def test_send_email_connection_error(email_notifier):
    """Test handling of SMTP connection error."""
    with (
        patch("builtins.open", mock_open(read_data="Test Body")),
        patch("smtplib.SMTP", side_effect=Exception("Connection failed")),
        patch("os.path.exists", return_value=True)
    ):
        
        # Should catch exception and log error, not crash
        email_notifier.send_email("receiver@test.com", "Subject", "test_file.md")

