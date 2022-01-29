import os
from db.interface import SimpleDB


def connect(dbname):
    try:
        f = open(dbname, 'r+b')
    except IOError:
        file_descriptor = os.open(dbname, os.O_RDWR | os.O_CREAT)
        file_ = os.fdopen(file_descriptor, 'r+b')
    return SimpleDB(file_)
