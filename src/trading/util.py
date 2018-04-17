from datetime import datetime

def print_start_end(record):
    print(record[0][0])
    print(datetime.fromtimestamp(record[0][0]))
    print(record[-1][0])
    print(datetime.fromtimestamp(record[-1][0]))

def toDate(epoc):
    return datetime.fromtimestamp(epoc)
