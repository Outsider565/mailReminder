# The file contains function to send email to a specific user
import os
import smtplib
from email.message import EmailMessage


class Mail:
    def __init__(self, from_addr: str = None, password: str = None):
        """
        Use the email address and password to login to the email server(SMTP)
        If the email address and password are not provided, the function will try to get them from environment variables.
        from_addr: email address of the sender
        password: password of the sender
        """
        if from_addr == "":
            from_addr = os.environ.get("EMAIL_USER")
            assert from_addr is not None, "Please provide the email address of the sender"
        else:
            self.from_addr = from_addr
        if password == "":
            password = os.environ.get("EMAIL_PASS")
            assert password is not None, "Please provide the password of the sender"
        else:
            self.password = password

    def send_mail(self, to_addr: str, subject: str, message: str = ""):
        """
        Send email to a specific user
        to_addr: email address of the receiver
        subject: subject of the email
        message: message of the email, default is empty string
        """
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        msg.set_content(message)

        with smtplib.SMTP_SSL('smtp.163.com', 465) as smtp:
            reply = smtp.login(self.from_addr, self.password)
            if reply[0] == 235:
                err = smtp.send_message(msg)
                if err == {}:
                    return True
        return False
