def main(argv):
    if not (4 <= len(argv) <= 5):
        usage()
        return BAD_ARGS