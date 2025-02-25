from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.core.mail.backends.console import EmailBackend as ConsoleBackend
from django.core.mail import EmailMessage

class CustomEmailBackend:
    def __init__(self, *args, **kwargs):
        self.smtp_backend = SMTPBackend(*args, **kwargs)
        self.console_backend = ConsoleBackend()

    def send_messages(self, email_messages):
        # Send via SMTP
        smtp_sent = self.smtp_backend.send_messages(email_messages)

        # Log to console
        for message in email_messages:
            self.console_backend.send_messages([message])

        return smtp_sent