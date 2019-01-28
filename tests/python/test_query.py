from os.path import join

import mock

import query


def test_str_from_file(star):
    assert query.str_from_file(star["src"]) == "SELECT * FROM `some_table`;"


@mock.patch("query.CursorProvider")
@mock.patch("query.datetime")
@mock.patch("query.prefix.datetime")
def test_execute(mock_prefix_dt, mock_dt, mock_cp, out_dir, show):
    mock_prefix_dt.now.return_value = show["prefix_dt"]

    mock_dt.now.side_effect = show["start_end_dt"]

    instance = mock_cp.return_value
    mock_cursor = mock.Mock()
    instance.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = show["rows"]
    mock_cursor.description = show["description"]

    results = query.execute(show["src"], directory=out_dir)

    mock_cursor.execute.assert_called_once()
    assert mock_cursor.execute.call_args == mock.call(show["str"])
    assert [row for row in open(join(out_dir, show["report_name"]))] == [row for row in open(show["report"])]
    assert [row for row in open(join(out_dir, show["csv_name"]))] == [row for row in open(show["csv"])]
    assert results == {
        "name": "show-columns",
        "headers": show["headers"],
        "rows": show["rows"]
    }
