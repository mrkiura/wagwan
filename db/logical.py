class LogicalBase(object):
    def get(self, key):
        """Retrieve value identified with key {key}.
        """
        if not self._storage.locked:
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref), key)

    def _refresh_tree_ref(self):
        """Syncs tree data with what is curently on disk.
        """
        self._tree_ref = self.node_ref_class(address=self._storage.get_root_address())
