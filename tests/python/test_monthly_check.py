from datetime import date, datetime
from os.path import join, exists, isfile, isdir

import mock

from monthly_check import monthly_check


@mock.patch("monthly_check.runner.datetime")
@mock.patch("monthly_check.runner.prefix.datetime")
@mock.patch("monthly_check.runner.CursorProvider")
def test_monthly_check(mock_cp, mock_prefix_dt, mock_dt, out_dir, expected):
    mock_prefix_dt.now.side_effect = [
        datetime(2019, 1, 23, 10, 31, 55),  # show-columns
        datetime(2019, 1, 23, 10, 31, 54),  # select-star
    ]

    mock_dt.now.side_effect = [
        datetime(2019, 1, 23, 10, 31, 55, 1),  # show-columns
        datetime(2019, 1, 23, 10, 31, 55, 2),  # show-columns
        datetime(2019, 1, 23, 10, 31, 54, 450265),  # select-star
        datetime(2019, 1, 23, 10, 31, 54, 999999),  # select-star
    ]

    instance = mock_cp.return_value

    mock_cursor_show = mock.Mock()
    mock_cursor_show.fetchall.return_value = expected["show_result"]
    mock_cursor_show.description = expected["show_description"]

    mock_cursor_star = mock.Mock()
    mock_cursor_star.fetchall.return_value = expected["star_result"]
    mock_cursor_star.description = expected["star_description"]

    instance.cursor.side_effect = [
        mock_cursor_show,
        mock_cursor_star
    ]

    report_dir = monthly_check(date(2019, 1, 1), source="../resources/sql", output=out_dir)

    assert report_dir == join(out_dir, "2019-01-January")
    assert isdir(report_dir)

    assert isdir(join(report_dir, "select-star"))
    assert isdir(join(report_dir, "show-columns"))
    assert isfile(join(report_dir, "2019-01-January-report.md"))

    star_query = join(report_dir, "select-star/2019-01-23T10-31-54_select-star.sql")
    star_csv = join(report_dir, "select-star/2019-01-23T10-31-54_select-star.csv")
    assert isfile(star_query)
    assert not exists(star_csv)
    assert [row for row in open(star_query)] == [row for row in open(expected["star_sql"])]

    show_query = join(report_dir, "show-columns/2019-01-23T10-31-55_show-columns.sql")
    show_csv = join(report_dir, "show-columns/2019-01-23T10-31-55_show-columns.csv")
    assert isfile(show_query)
    assert isfile(show_csv)
    assert [row for row in open(show_query)] == [row for row in open(expected["show_sql"])]
    assert [row for row in open(show_csv)] == [row for row in open(expected["show_csv"])]
