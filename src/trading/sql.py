import sqlite3
from sqlalchemy import MetaData, create_engine, func
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker


def connect(connect_string):
    connection = create_engine(connect_string)
    return {"connection": connection,
            "meta_data": meta(connection),
            "session": sessionmaker(bind=connection)()}


def meta(connection, **kwargs):
    '''
    Bind to database and returns reflection
    :returns sqlalchemy.Metadata:
    '''
    meta = MetaData()
    meta.reflect(bind=connection)
    return meta
    # return Table('orders', meta, autoload=True, autoload_with=connection)


def window(cursor,
           start,
           end,
           time_column='time',
           table='ohlc',
           connection=None,
           meta_data=None,
           **kwargs):
    start = int(start)
    end = int(end)
    if not connection:
        cursor.execute("""SELECT {0}, open
        FROM {1}
        WHERE {0} >= ? AND {0} < ? """.format(time_column,
                                              table), (start,
                                                       end))
        result = cursor.fetchall()
    else:

        table = meta(connection).tables[table]
        s = select([table.c[time_column],
                    table.c.open]).where(table.c[time_column].between(start,
                                                                      end))
        result = connection.execute(s).fetchall()
    return result


def memdb():
    return connect('sqlite://')



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
        result = session.query(func.max(orders_tables.columns[time_column]),
                               func.min(orders_tables.columns[time_column]))
        end = int(result.all()[0][0])
        start = int(result.all()[0][1])
    return start, end


def latest(connection, meta_data, table_name='ohlc', time_column='time',
           **kwargs):
    db = kwargs.copy()
    db.update({'connection': connection,
               'meta_data': meta_data,
               'table': table_name,
               'time_column': time_column})
    start, end = time_range(**db)
    print(end)
    table = meta_data.tables[table_name]
    # time_range returns int
    query = select([table])
    result = connection.execute(query).fetchall()
    print(result)
    return result[0]
    # start, end = time_range(cur, time_column, table)
    # cur.execute("SELECT * from {}, open ")
