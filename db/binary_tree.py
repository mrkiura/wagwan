import pickle
from db.logical import LogicalBase, ValueRef


class BinaryTree(LogicalBase):
    def _get(self, node, key):
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif node.key < key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def _insert(self, node, key, value_ref):
        if node is None:
            new_node = BinaryNode(self.node_ref_class(), key, value_ref, self.node_ref_class(), 1)
        elif key < node.key:
            new_node = BinaryNode.from_node(node, left_ref=self._insert(
                self._follow(node.left_ref),
                key,
                value_ref
            ))

        elif node.key < key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(self.follow(node.right_ref), key, value_ref)
            )
        else:
            new_node = BinaryNode.from_node(node, value_ref=value_ref)

        return self.node_ref_class(referent=new_node)


class BinaryNodeRef(ValueRef):
    def prepare_to_store(self, storage):
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_string(referent):
        return pickle.dumps({
            'left': referent.left_ref.address,
            'right': referent.right_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'length': referent.length
        })

class BinaryNode:

    @classmethod
    def from_node(cls, node, **kwargs):
        length = node.length
        if 'left_ref' in kwargs:
            length += kwargs['left_ref'].length - node.left_ref.length

        if 'right_ref' in kwargs:
            length += kwargs['right_ref'].length - node.right_ref.length

        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            length=length
        )

    def __init__(self, left_ref, key, value_ref, right_ref, length) -> None:
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.length = length


    def store_refs(self, storage):
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)
