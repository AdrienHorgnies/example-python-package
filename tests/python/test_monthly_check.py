import os
import shutil
import tempfile
from datetime import date

from monthly_check import monthly_check


def test_monthly_check():
    output = os.path.join(
        tempfile.gettempdir(),
        "test-reports"
    )
    os.mkdir(output)

    try:
        report_dir = monthly_check(date(2019, 1, 1), source="../resources/sql", output=output)

        assert report_dir == os.path.join(output, "2019-01-January")
        assert os.path.isdir(report_dir)

        assert os.path.isdir(os.path.join(report_dir, "select-star"))
        assert os.path.isdir(os.path.join(report_dir, "show-columns"))
        assert os.path.isfile(os.path.join(report_dir, "2019-01-January-report.md"))

        expected_report_dir = "../resources/select-star/expected_monthly_check_report/2019-01-January"

        star_query = os.path.join(report_dir, "select-star/2019-01-23T10-31-54_select-star.sql")
        expected_star_query = os.path.join(expected_report_dir, "select-star/2019-01-23T10-31-54_select-star.sql")
        assert os.path.isfile(star_query)
        assert [row for row in open(star_query)] == [row for row in open(expected_star_query)]

        show_query = os.path.join(report_dir, "show-columns/2019-01-23T10-31-55_show-columns.sql")
        show_csv = os.path.join(report_dir, "show-columns/2019-01-23T10-31-55_show-columns.csv")
        expected_show_query = os.path.join(expected_report_dir, "show-columns/2019-01-23T10-31-55_show-columns.sql")
        expected_show_csv = os.path.join(expected_report_dir, "show-columns/2019-01-23T10-31-55_show-columns.csv")
        assert os.path.isfile(show_query)
        assert os.path.isfile(show_csv)
        assert [row for row in open(show_query)] == [row for row in open(expected_show_query)]
        assert [row for row in open(show_csv)] == [row for row in open(expected_show_csv)]
    finally:
        shutil.rmtree(output)
