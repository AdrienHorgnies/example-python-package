import csv
from os.path import join

import pytest

RSRC = join("..", "resources")
X_REPORT_DIR = join(RSRC, "expected_monthly_check", "2019-01-January")
TMP_STAR = "2019-01-23T10-31-54_select-star"
TMP_SHOW = "2019-01-23T10-31-55_show-columns"


@pytest.fixture()
def star():
    return {
        "in_sql": join(RSRC, "sql", "select-star.sql"),
        "out_sql": join(X_REPORT_DIR, "select-star", TMP_STAR + ".sql"),
        "rows": [],
        "description": []
    }


@pytest.fixture()
def show():
    show_csv = join(X_REPORT_DIR, "show-columns", TMP_SHOW + ".csv")

    with open(show_csv) as show_csv_file:
        reader = csv.reader(show_csv_file)
        csv_content = list(reader)
        show_result = csv_content[1:]
        show_description = csv_content[:1]

    return {
        "show_sql": join(X_REPORT_DIR, "show-columns", TMP_SHOW + ".sql"),
        "show_csv": show_csv,
        "show_result": show_result,
        "show_description": show_description,
    }
