from db.storage import Storage
from db.binary_tree import BinaryTree

class SimpleDB(object):

    def __init__(self) -> None:
        self._storage = Storage()
        self._tree = BinaryTree(self._storage)
