import os
from simpledb.interface import SimpleDB


def connect(dbname):
    try:
        file_ = open(dbname, 'r+b')
    except IOError:
        file_descriptor = os.open(dbname, os.O_RDWR | os.O_CREAT)
        file_ = os.fdopen(file_descriptor, 'r+b')
    return SimpleDB(file_)
