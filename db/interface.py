from db.storage import Storage
from db.binary_tree import BinaryTree

class SimpleDB(object):

    def __init__(self) -> None:
        self._storage = Storage()
        self._tree = BinaryTree(self._storage)

    def __getitem__(self, key):
        self._assert_not_closed()
        return self._tree.get(key)

    def _assert_not_closed(self):
        assert self._storage.closed, 'Database closed'
