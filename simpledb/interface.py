from simpledb.binary_tree import BinaryTree
from simpledb.storage import Storage


class SimpleDB(object):
    """
    SimpleDB is a simple key-value database using a binary tree data structure and a storage system for persisting data.
    """
    def __init__(self, f):
        """
        Initialize the SimpleDB with a file object for storage.
        """
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        """
        Check if the database is closed and raise a ValueError if it is.
        """
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        """
        Close the storage and, in turn, the database.
        """
        self._storage.close()

    def commit(self):
        """
        Commit the changes in the binary tree to the storage.
        """
        self._assert_not_closed()
        self._tree.commit()

    def __getitem__(self, key):
        """
        Retrieve a value associated with a key from the binary tree.
        """
        self._assert_not_closed()
        return self._tree.get(key)

    def __setitem__(self, key, value):
        """
        Set a value for a given key in the binary tree.
        """
        self._assert_not_closed()
        return self._tree.set(key, value)

    def __delitem__(self, key):
        """
        Remove a key-value pair from the binary tree.
        """
        self._assert_not_closed()
        return self._tree.pop(key)

    def __contains__(self, key):
        """
        Check if a key exists in the binary tree.
        """
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __len__(self):
        """
        Return the number of key-value pairs in the binary tree.
        """
        return len(self._tree)
