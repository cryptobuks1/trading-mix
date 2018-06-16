import sqlite3
from sqlalchemy import MetaData, create_engine, func
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

def connect(connect_string):
    connection = create_engine(connect_string)
    return {"connection": connection,
            "cursor": connection,
            "meta_data": meta(connection),
            "session": sessionmaker(bind=connection)()}


def meta(connection):
    meta = MetaData()
    meta.reflect(bind=connection)
    return meta
    # return Table('orders', meta, autoload=True, autoload_with=connection)


def window(cur, start, end, time_column='time', table='ohlc'):
    start = int(start)
    end = int(end)
    cur.execute("""SELECT {0}, open
    FROM {1}
    WHERE {0} >= ? AND {0} < ? """.format(time_column, table), (start, end))
    result = cur.fetchall()
    return result


def memdb():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    return con, cur


def time_range(cur=None, time_column='time', table='ohlc', **kwargs):
    if 'connection' not in kwargs:
        cur.execute("SELECT min({}) FROM {}".format(time_column, table))
        start = int(cur.fetchall()[0][0])
        cur.execute("SELECT max({}) FROM {}".format(time_column, table))
        end = int(cur.fetchall()[0][0])
    else:
        session = kwargs['session']
        meta_data = meta(kwargs['connection'])
        orders_tables = meta_data.tables[table]
        print(orders_tables.columns)
        result = session.query(func.max(orders_tables.columns[time_column]),
                               func.min(orders_tables.columns[time_column]))
        end = int(result.all()[0][0])
        start = int(result.all()[0][1])
    return start, end


def latest(cur, time_column='time', table='ohlc'):
    start, end = time_range(cur, time_column, table)
    return cur.execute("SELECT {0}, open ")
