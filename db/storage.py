import portalocker


class Storage(object):

    def __init__(self) -> None:
        self._file = None

    def lock(self):
        if not self.locked:
            portalocker.lock(self._file, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False
