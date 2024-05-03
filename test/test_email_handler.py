import os
import smtplib
from unittest.mock import patch

from email_handler import send_an_email


def test_app_password_env_variable():
    assert os.getenv("APP_PASSWORD") is not None


@patch("email_handler.smtplib.SMTP")
def test_send_an_email_successfully(mock_smtp):
    mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
    send_an_email("test@example.com", "This is a test newsletter message")
    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_once()
    mock_smtp_instance.send_message.assert_called_once()


@patch("email_handler.smtplib.SMTP")
def test_send_an_email_authentication_error(mock_smtp):
    mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
    mock_smtp_instance.login.side_effect = smtplib.SMTPAuthenticationError(
        535, "Authentication failed"
    )
    result = send_an_email("test@example.com", "This is a test newsletter message")
    assert result == "Email Authentication failed: (535, 'Authentication failed')"


@patch("email_handler.smtplib.SMTP")
def test_send_an_email_smtp_exception(mock_smtp):
    mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
    mock_smtp_instance.send_message.side_effect = smtplib.SMTPException("Error logs")
    result = send_an_email("test@example.com", "This is a test newsletter message")
    assert result == "An SMTP error occurred: Error logs"


@patch("email_handler.smtplib.SMTP")
def test_send_an_email_exception(mock_smtp):
    mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
    mock_smtp_instance.send_message.side_effect = Exception("Error logs")
    result = send_an_email("test@example.com", "This is a test newsletter message")
    assert result == "An error occurred: Error logs"
