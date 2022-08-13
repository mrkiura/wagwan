import os
import tempfile
import pytest

from simpledb.storage import Storage


@pytest.fixture
def temp_file():
    return tempfile.NamedTemporaryFile()

@pytest.fixture
def storage(temp_file):
    st = Storage(temp_file)
    yield st
    st.close()


def _get_superblock_and_data(value):
    superblock = value[: Storage.SUPERBLOCK_SIZE]
    data = value[Storage.SUPERBLOCK_SIZE :]
    return superblock, data

def _get_file_contents(file_):
    file_.flush()
    with open(file_.name, "rb") as f:
        return f.read()

def test_init_ensures_superblock(temp_file, storage):
    EMPTY_SUPERBLOCK = (b"\x00" * Storage.SUPERBLOCK_SIZE)
    temp_file.seek(0, os.SEEK_END)
    value = _get_file_contents(temp_file)
    assert value == EMPTY_SUPERBLOCK

def test_write(temp_file, storage):
    storage.write(b"ABCDE")
    value = _get_file_contents(temp_file)
    _, data = _get_superblock_and_data(value)
    assert data == b"\x00\x00\x00\x00\x00\x00\x00\x05ABCDE"

def test_read(temp_file, storage):
    temp_file.seek(Storage.SUPERBLOCK_SIZE)
    temp_file.write(b"\x00\x00\x00\x00\x00\x00\x00\x0801234567")
    value = storage.read(Storage.SUPERBLOCK_SIZE)
    assert value == b"01234567"

def test_commit_root_address(temp_file, storage):
    storage.commit_root_address(257)
    root_bytes = _get_file_contents(temp_file)[:8]
    assert root_bytes == b"\x00\x00\x00\x00\x00\x00\x01\x01"

def test_get_root_address(temp_file, storage):
    temp_file.seek(0)
    temp_file.write(b"\x00\x00\x00\x00\x00\x00\x02\x02")
    root_address = storage.get_root_address()
    assert root_address == 514

def test_workflow(storage):
    a1 = storage.write(b"one")
    a2 = storage.write(b"two")
    storage.commit_root_address(a2)
    a3 = storage.write(b"three")
    assert storage.get_root_address() == a2
    a4 = storage.write(b"four")
    storage.commit_root_address(a4)
    assert storage.read(a1) == b"one"
    assert storage.read(a2) == b"two"
    assert storage.read(a3) == b"three"
    assert storage.read(a4) == b"four"
    assert storage.get_root_address() == a4
