from __future__ import print_function
import sys

from constants import BAD_ARGS, SUPPORTED_VERBS, BAD_VERB
import simpledb


OK = 0
BAD_ARGS = 1
BAD_VERB = 2
BAD_KEY = 3


def usage():
    print('Usage:', file=sys.stderr)
    print('\tpython -m db.tool DBNAME get KEY', file=sys.stderr)
    print('\tpython -m db.tool DBNAME set KEY VALUE', file=sys.stderr)
    print('\tpython -m db.tool DBNAME delete KEY', file=sys.stderr)


def main(argv):
    if not (4 <= len(argv) <= 5):
        usage()
        return BAD_ARGS
    dbname, verb, key, value = (argv[1:] + [None])[:4]
    if verb not in SUPPORTED_VERBS:
        usage()
        return BAD_VERB
    db = simpledb.connect(dbname)
    try:
        if verb == 'get':
            sys.stdout.write(db[key])
        elif verb == 'set':
            db[key] = value
            db.commit()
        else:
            del db[key]
            db.commit()
    except KeyError:
        print('Key not found', file=sys.stderr)
        return BAD_KEY
    return OK


if __name__ == '__main__':
    sys.exit(main(sys.argv))
