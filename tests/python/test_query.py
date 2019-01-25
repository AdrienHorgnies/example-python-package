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


@mock.patch("query.CursorProvider")
@mock.patch("query.datetime")
def test_execute(mock_datetime, mock_cp):
    mock_datetime.now.side_effect = [
        datetime(2019, 2, 3, 14, 52, 54, 452000),
        datetime(2019, 2, 3, 14, 52, 55, 502000)
    ]

    instance = mock_cp.return_value
    mock_cursor = mock.Mock()
    instance.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Adrien"),
        (2, "Simon")
    ]
    mock_cursor.description = [["id"], ["name"]]

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
        file.write("SELECT * FROM `person`;\n\n")
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as expected_file:
        expected_file.write("SELECT * FROM `person`;\n\n"
                            "-- START TIME: 2019-02-03T14:52:54.452000\n"
                            "-- END TIME: 2019-02-03T14:52:55.502000\n"
                            "-- DURATION: 0:00:01.050000\n"
                            "-- ROWS COUNT: 2\n"
                            "-- RESULT FILE: {}\n".format(os.path.splitext(file.name)[0] + ".csv"))

    results = query.execute(file.name)

    mock_cursor.execute.assert_called_once()
    assert mock_cursor.execute.call_args == mock.call("SELECT * FROM `person`;")
    assert [row for row in open(file.name)] == [row for row in open(expected_file.name)]
    assert results == {
        "headers": ["id", "name"],
        "rows": mock_cursor.fetchall.return_value
    }
