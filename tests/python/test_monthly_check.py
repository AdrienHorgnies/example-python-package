from datetime import date
from os.path import join, exists, isfile, isdir

import mock

from monthly_check import monthly_check


@mock.patch("monthly_check.getuser")
@mock.patch("monthly_check.datetime")
@mock.patch("monthly_check.runner.datetime")
@mock.patch("monthly_check.runner.prefix.datetime")
@mock.patch("monthly_check.runner.CursorProvider")
def test_monthly_check(mock_cp, mock_prefix_dt, mock_runner_dt, mock_dt, mock_getuser, out_dir, star, show, report):
    mock_prefix_dt.now.side_effect = [
        show["prefix_dt"],  # show-columns
        star["prefix_dt"],  # select-star
    ]

    mock_runner_dt.now.side_effect = show["start_end_dt"] + star["start_end_dt"]

    mock_dt.today.return_value = star["prefix_dt"]

    instance = mock_cp.return_value

    mock_cursor_show = mock.Mock()
    mock_cursor_show.fetchall.return_value = show["rows"]
    mock_cursor_show.description = show["description"]

    mock_cursor_star = mock.Mock()
    mock_cursor_star.fetchall.return_value = star["rows"]
    mock_cursor_star.description = star["description"]

    instance.cursor.side_effect = [
        mock_cursor_show,
        mock_cursor_star
    ]

    mock_getuser.return_value = "aho"

    report_dir = monthly_check(date(2019, 1, 1), source="../resources/sql", output=out_dir)

    assert report_dir == join(out_dir, "2019-01-January")
    assert isdir(report_dir)

    assert isdir(join(report_dir, "select-star"))
    assert isdir(join(report_dir, "show-columns"))
    assert isfile(join(report_dir, "2019-01-January-report.md"))

    star_report = join(report_dir, "select-star", star["report_name"])
    star_csv = join(report_dir, "select-star", star["csv_name"])
    assert isfile(star_report)
    assert not exists(star_csv)
    assert [row for row in open(star_report)] == [row for row in open(star["report"])]

    show_report = join(report_dir, "show-columns", show["report_name"])
    show_csv = join(report_dir, "show-columns", show["csv_name"])
    assert isfile(show_report)
    assert isfile(show_csv)
    assert [row for row in open(show_report)] == [row for row in open(show["report"])]
    assert [row for row in open(show_csv)] == [row for row in open(show["csv"])]

    actual_monthly_report = [row for row in open(join(report_dir, "2019-01-January-report.md"))]
    assert actual_monthly_report == report
