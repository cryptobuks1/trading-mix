import smtplib
from toml import load
from os.path import expanduser
from email.message import EmailMessage
# import email


def test_send_mail():
    conf = load(expanduser('~/trading.toml'))
    msg = EmailMessage()
    msg.set_content("Sell")
    msg['Subject'] = 'advice'
    msg['From'] = 'kristian@freeduck.dk'
    msg['To'] = 'kristian.n.jensen@gmail.com'
    with smtplib.SMTP('freeduck.dk', 25) as smtp:
        print("smtp")
        smtp.starttls()
        print("starttls")
        smtp.login(conf['mail']['username'],
                   conf['mail']['password'])
        print("login")
        smtp.send_message(msg)
        print('You got mail')
