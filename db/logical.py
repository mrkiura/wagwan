class LogicalBase(object):
    def get(self, key):
        """Retrieve value identified with key {key}.
        """
        if not self._storage.locked:
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref), key)

    def set(self, key, value):
        if self._storage.lock():
            self._refresh_tree_ref()
        self._tree_ref = self._insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value)
        )

    def _refresh_tree_ref(self):
        """Syncs tree data with what is curently on disk.
        """
        self._tree_ref = self.node_ref_class(address=self._storage.get_root_address())

    def commit(self):
        self._tree_ref.store(self._storage)
        self._storage.commit_root_address(self._tree_ref.address)


class ValueRef:
    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_string(self._referent))

    def store(self, storage):
        if self._referent is not None and self._address:
            self.prepare_to_store(storage)
            self.address = storage.write(self._referent_to_string(self._referent))

class BinaryNodeRef(ValueRef):
    def prepare_to_store(self, storage):
        if self._referent:
            self._referent.store_refs(storage)



class BinaryNode:
    def store_refs(self, storage):
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)