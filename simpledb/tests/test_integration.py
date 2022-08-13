import os
import os.path
import pytest
import shutil
import subprocess
import tempfile

import simpledb.tool


@pytest.fixture
def db_paths():
    working_dir = tempfile.mkdtemp()
    new_db_path = os.path.join(working_dir, "new.db")
    current_db_path = os.path.join(working_dir, "current.db")
    yield {
        'new': new_db_path,
        'current': current_db_path
    }
    shutil.rmtree(working_dir, ignore_errors=True)


@pytest.fixture
def tempfile_name():
    with tempfile.NamedTemporaryFile(delete=False) as temp_f:
        temp_name = temp_f.name
        yield temp_name
        os.remove(temp_name)


def simpledb_tool(tempfile_name, *args):
    return subprocess.check_output(
        ['python', '-m', 'simpledb.tool', tempfile_name] + list(args),
        stderr=subprocess.STDOUT
    )


def test_new_database_file(db_paths):
    db = simpledb.connect(db_paths['new'])
    db["year"] = "2022"
    db.commit()
    db.close()


def test_persistence(db_paths):
    db = simpledb.connect(db_paths['current'])
    db["artist"] = "Key Glock"
    db["song"] = "proud"
    db["year"] = "2022"
    db.commit()
    db["label"] = "pre"
    assert len(db) == 4
    db.close()
    db = simpledb.connect(db_paths['current'])
    assert db["artist"] == "Key Glock"
    assert db["song"] == "proud"
    assert db["year"] == "2022"
    with pytest.raises(KeyError):
        db["label"]
    assert len(db) == 3
    db.close()


def test_get_non_existent(tempfile_name):
    simpledb_tool(tempfile_name, "set", "foo", b"bar")
    simpledb_tool(tempfile_name, "delete", "foo")
    with pytest.raises(subprocess.CalledProcessError) as raised:
        simpledb_tool(tempfile_name, "get", "foo")
    assert raised.type == subprocess.CalledProcessError
    assert raised.value.output == b'Key not found\n'
    assert raised.value.args[0] == simpledb.tool.BAD_KEY


def test_tool(tempfile_name):
    expected = b"b"
    simpledb_tool(tempfile_name, "set", "a", expected)
    actual = simpledb_tool(tempfile_name, "get", "a")
    assert actual == expected
