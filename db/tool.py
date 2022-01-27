import sys
from constants import BAD_ARGS, SUPPORTED_VERBS, BAD_VERB, OK
from db.constants import BAD_KEY


def usage():
    pass


def main(argv):
    if not (4 <= len(argv) <= 5):
        usage()
        return BAD_ARGS
    dbname, verb, key, value = (argv[1:] + [None])[:4]
    if verb not in SUPPORTED_VERBS:
        usage()
        return BAD_VERB
    db = db.connect(dbname)

    try:
        if verb == 'get':
            sys.stdout.write(db[key])

        elif verb == 'set':
            db[key] = value
            db.commit()

    except KeyError as error:
        print('Key not found', file=sys.stderr)
        return BAD_KEY

    return OK