import smtplib
from email.message import EmailMessage


def create_message(To, From, Subject, Body):
    msg = EmailMessage()
    msg.set_content(Body)
    msg['Subject'] = Subject
    msg['From'] = From
    msg['To'] = To
    return msg


def send(message, username, password):
    with smtplib.SMTP('freeduck.dk', 25) as smtp:
        print("smtp")
        smtp.starttls()
        print("starttls")
        smtp.login(username,
                   password)
        print("login")
        smtp.send_message(message)
        print('You got mail')
