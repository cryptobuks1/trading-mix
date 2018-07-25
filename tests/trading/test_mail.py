from trading.mail import send, create_message
from toml import load
from os.path import expanduser
# import email


def test_send_mail():
    msg = create_message('kristian.n.jensen@gmail.com',
                         'kristian@freeduck.dk',
                         'Advice',
                         'Buy')
    conf = load(expanduser('~/trading.toml'))
    send(msg,
         conf['mail']['username'],
         conf['mail']['password'])
