import pickle
import pytest
import random


from simpledb.binary_tree import BinaryNode, BinaryTree, BinaryNodeRef, ValueRef


class StubStorage(object):
    def __init__(self):
        self.d = [0]
        self.locked = False

    def lock(self):
        if not self.locked:
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        pass

    def get_root_address(self):
        return 0

    def write(self, string):
        address = len(self.d)
        self.d.append(string)
        return address

    def read(self, address):
        return self.d[address]



@pytest.fixture
def tree():
    return BinaryTree(StubStorage())


def test_get_missing_key_raises_key_error(tree):
    with pytest.raises(KeyError):
        tree.get("Not A Key In The Tree")

def test_set_and_get_key(tree):
    tree.set("a", "b")
    assert tree.get("a") ==  "b"

def test_random_set_and_get_keys(tree):
    ten_k = list(range(10000))
    pairs = list(zip(random.sample(ten_k, 10), random.sample(ten_k, 10)))
    for i, (k, v) in enumerate(pairs, start=1):
        tree.set(k, v)
        assert len(tree) == i
    for k, v in pairs:
        assert tree.get(k) == v
    random.shuffle(pairs)
    for i, (k, v) in enumerate(pairs, start=1):
        tree.pop(k)
        assert len(tree) == len(pairs) - i

def test_overwrite_and_get_key(tree):
    tree.set("a", "b")
    tree.set("a", "c")
    assert tree.get("a") == "c"

def test_pop_non_existent_key(tree):
    with pytest.raises(KeyError):
        tree.pop("Not A Key In The Tree")

def test_del_leaf_key(tree):
    tree.set("b", "2")
    tree.pop("b")
    with pytest.raises(KeyError):
        tree.get("b")

def test_del_left_node_key(tree):
    tree.set("b", "2")
    tree.set("a", "1")
    tree.pop("b")
    with pytest.raises(KeyError):
        tree.get("b")
    tree.get("a")

def test_del_right_node_key(tree):
    tree.set("b", "2")
    tree.set("c", "3")
    tree.pop("b")
    with pytest.raises(KeyError):
        tree.get("b")
    tree.get("c")

def test_del_full_node_key(tree):
    tree.set("b", "2")
    tree.set("a", "1")
    tree.set("c", "3")
    tree.pop("b")
    with pytest.raises(KeyError):
        tree.get("b")
    tree.get("a")
    tree.get("c")


def test_to_string_leaf():
    n = BinaryNode(BinaryNodeRef(), "k", ValueRef(address=999), BinaryNodeRef(), 1)
    pickled = BinaryNodeRef.referent_to_string(n)
    d = pickle.loads(pickled)
    assert d["left"] == 0
    assert d["key"] == "k"
    assert d["value"] == 999
    assert d["right"] == 0

def test_to_string_nonleaf():
    left_ref = BinaryNodeRef(address=123)
    right_ref = BinaryNodeRef(address=321)
    n = BinaryNode(left_ref, "k", ValueRef(address=999), right_ref, 3)
    pickled = BinaryNodeRef.referent_to_string(n)
    d = pickle.loads(pickled)
    assert d["left"] == 123
    assert d["key"] == "k"
    assert d["value"] == 999
    assert d["right"] == 321
