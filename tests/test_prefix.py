import filecmp
import os
import tempfile
from datetime import datetime

import mock

import prefix


@mock.patch("prefix.datetime")
def test_timestamp_no_dir(mock_datetime):
    mock_datetime.now.return_value = datetime(2019, 4, 2, 10, 20, 33)

    path = os.path.join(tempfile.gettempdir(), "tmp-test-file.sql")
    with open(path, "w") as file:
        file.write("SELECT 'This is a test';")

    copy_path = prefix.timestamp(path)

    assert os.path.isfile(copy_path)
    assert os.path.dirname(copy_path) == os.path.dirname(path)
    assert os.path.basename(copy_path) == "2019-04-02T10-20-33_tmp-test-file.sql"
    assert filecmp.cmp(copy_path, path)


@mock.patch("prefix.datetime")
def test_timestamp_with_dir(mock_datetime):
    mock_datetime.now.return_value = datetime(2019, 4, 2, 10, 20, 33)

    directory = tempfile.gettempdir()
    path = os.path.join(tempfile.gettempdir(), "tmp-test-file.sql")

    with open(path, "w") as file:
        file.write("SELECT 'This is a test';")

    copy_path = prefix.timestamp(path, directory=directory)

    assert os.path.isfile(copy_path)
    assert os.path.dirname(copy_path) == directory
    assert os.path.basename(copy_path) == "2019-04-02T10-20-33_tmp-test-file.sql"
    assert filecmp.cmp(copy_path, path)
