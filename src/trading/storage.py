
from sqlalchemy import MetaData, Table, Column, desc
from sqlalchemy.types import DateTime, Integer, PickleType
from sqlalchemy.sql import func, select
from os.path import expanduser, exists, dirname
from os import makedirs
from trading.sql import connect
import pickle
import logging


def save(topic, data, **kwargs):
    connection, topic_table = get_table(topic)
    logging.warn(topic_table)
    connection.execute(topic_table.insert().values(payload=pickle.dumps(data)))


def load(topic):
    connection, topic_table = get_table(topic)
    query = select([topic_table]).order_by(desc(topic_table.c['id']))
    message = connection.execute(query).fetchone()
    if message:
        message = pickle.loads(message['payload'])
    return message


def get_pickle_log_db():
    db_path = expanduser('~/.local/lib/trading/data/state.sqlite')
    db_dir = dirname(db_path)

    if not exists(db_dir):
        makedirs(db_dir)

    return connect('sqlite:///' + db_path)


def get_pickle_log_table_def(table_name, *, connection, **kwargs):
    metadata = MetaData()
    metadata.reflect(bind=connection)
    return metadata.tables[table_name]


def get_table(table_name):
    db_path = expanduser('~/.local/lib/trading/data/state.sqlite')
    db_dir = dirname(db_path)

    if not exists(db_dir):
        makedirs(db_dir)

    db = connect('sqlite:///' + db_path)

    metadata = MetaData()
    metadata.reflect(bind=db['connection'])

    if not db['connection'].dialect.has_table(db['connection'], table_name):
        orderlog_table = Table(table_name, metadata,
                               Column('id', Integer, primary_key=True),
                               Column('payload', PickleType, nullable=False),
                               Column('datetime', DateTime,
                                      server_default=func.now()))
        orderlog_table.create(db['connection'])
    else:
        orderlog_table = metadata.tables[table_name]

    return db['connection'], orderlog_table
