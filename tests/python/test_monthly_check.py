import shutil
import tempfile
from datetime import date, datetime
from os import mkdir
from os.path import join, exists, isfile, isdir

import mock
import pytest

from monthly_check import monthly_check

X_REPORT_DIR = "../resources/expected_monthly_check_report/2019-01-January"
STAR = "2019-01-23T10-31-54_select-star"
SHOW = "2019-01-23T10-31-55_show-columns"


@pytest.fixture(scope="function")
def out_dir():
    output = join(
        tempfile.gettempdir(),
        "test-reports"
    )
    mkdir(output)

    yield output

    shutil.rmtree(output)


@pytest.fixture(scope="module")
def expected():
    return {
        "star_sql": join(X_REPORT_DIR, "select-star", STAR + ".sql"),
        "show_sql": join(X_REPORT_DIR, "show-columns", SHOW + ".sql"),
        "show_csv": join(X_REPORT_DIR, "show-columns", SHOW + ".csv")
    }


@mock.patch("monthly_check.runner.prefix.datetime")
@mock.patch("monthly_check.runner.CursorProvider")
def test_monthly_check(mock_cp, mock_prefix_dt, out_dir, expected):
    mock_prefix_dt.now.side_effect = [
        datetime(2019, 1, 23, 10, 31, 55),  # show-columns
        datetime(2019, 1, 23, 10, 31, 54),  # select-star
    ]

    report_dir = monthly_check(date(2019, 1, 1), source="../resources/sql", output=out_dir)

    assert report_dir == join(out_dir, "2019-01-January")
    assert isdir(report_dir)

    assert isdir(join(report_dir, "select-star"))
    assert isdir(join(report_dir, "show-columns"))
    assert isfile(join(report_dir, "2019-01-January-report.md"))

    star_query = join(report_dir, "select-star/2019-01-23T10-31-54_select-star.sql")
    star_csv = join(report_dir, "select-star/2019-01-23T10-31-54_select-star.csv")
    assert not exists(star_csv)
    assert isfile(star_query)
    assert [row for row in open(star_query)] == [row for row in open(expected["star_sql"])]

    show_query = join(report_dir, "show-columns/2019-01-23T10-31-55_show-columns.sql")
    show_csv = join(report_dir, "show-columns/2019-01-23T10-31-55_show-columns.csv")
    assert isfile(show_query)
    assert isfile(show_csv)
    assert [row for row in open(show_query)] == [row for row in open(expected["show_sql"])]
    assert [row for row in open(show_csv)] == [row for row in open(expected["show_csv"])]
