import smtplib
from email.mime.text import MIMEText
from typing import List

subject = "Invalid connections"
sender = "sender@email.com" #provide sender email
recipients = ["recipent@email.com"] #provide list of recipents
password = "password" #provide smtp gmail password


def initializeAndSendEmail(subject: str, body: str, sender: str, recipients: List[str], password: str) -> None:
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())


def sendErrorMessage(message: str):
    initializeAndSendEmail(subject, message, sender, recipients, password)