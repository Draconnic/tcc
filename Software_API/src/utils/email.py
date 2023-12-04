import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError

from werkzeug.exceptions import InternalServerError


class Email:
    def __init__(self, sender_email, sender_password, smtp_server, smtp_port):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self._sender = None
        self._subject = None
        self._body = None
        self.message = MIMEMultipart()

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, to):
        self._sender = to
        self.message["To"] = to

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject):
        self._subject = subject
        self.message["Subject"] = subject

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body
        self.message.attach(MIMEText(body, "plain"))

    def send_email(self):
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(self.sender_email, self.sender_password)
                smtp_server.send_message(self.message)
            return 200
        except SMTPAuthenticationError:
            raise InternalServerError(description="PostgreSQL server unavailable")
