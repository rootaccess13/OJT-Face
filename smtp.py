import smtplib, ssl
import os
from dotenv import load_dotenv
import logging as log
from datetime import datetime

log.basicConfig(filename="mail.log", level=log.INFO)
load_dotenv()

class SendEmail:
    def __init__(self):
        self.smtp_server = os.environ.get("SMTP_SERVER")
        self.port = os.environ.get("SMTP_PORT")
        self.sender_email = os.environ.get("SENDER_EMAIL")
        self.password = os.environ.get("SENDER_PASSWORD")
        self.context = ssl.create_default_context()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M:%S")
    def send(self, receiver_email, message):
        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.ehlo()  # Can be omitted
            server.starttls(context=self.context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message)
            if server:
                log.info("{0} - Email sent : {1} - {2}".format(self.time,receiver_email, self.today))
                print("Email sent")
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()

