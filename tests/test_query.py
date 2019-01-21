import filecmp
import os.path
import tempfile
from datetime import datetime

import mock

import query


def test_str_from_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
        file.write("-- A comment followed by a blank line\n"
                   "\n"
                   "SELECT 'this is a test' -- inline comment\n"
                   "WHERE 1;\n"
                   "\n")
    assert query.str_from_file(file.name) == "SELECT 'this is a test' WHERE 1;"


@mock.patch("query.datetime")
def test_execute(mock_datetime):
    mock_datetime.now.side_effect = [
        datetime(2019, 2, 3, 14, 52, 54, 452000),
        datetime(2019, 2, 3, 14, 52, 55, 502000)
    ]

    # todo mock mysql connection provided

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
        file.write("SHOW DATABASES;\n")
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as expected_file:
        expected_file.write("SHOW DATABASES;\n"
                            "\n"
                            "-- START TIME: 2019-02-03T14:52:54.452\n"
                            "-- END TIME: 2019-02-03T14:52:55.502\n"
                            "-- DURATION: 1.050s\n"
                            "-- ROWS COUNT: 3\n"
                            "-- RESULT FILE: {}\n".format(os.path.splitext(file.name)[0] + ".csv"))

    results = query.execute(file.name)

    assert filecmp.cmp(file, expected_file)
    assert results == {
        "n_rows": 3,
        "headers": ['name'],
        "rows": ['information_schema', 'database_a', 'database_b']
    }
