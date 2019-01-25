import csv
import tempfile
from datetime import datetime
from os import mkdir
from os.path import join
from shutil import rmtree

import pytest

RSRC = join("..", "resources")
X_REPORT_DIR = join(RSRC, "expected_monthly_check_report", "2019-01-January")


@pytest.fixture(scope="function")
def out_dir():
    output = join(
        tempfile.gettempdir(),
        "pytest_working_dir"
    )
    mkdir(output)

    yield output

    rmtree(output)


@pytest.fixture()
def star():
    return {
        "src": join(RSRC, "sql", "select-star.sql"),
        "report": join(X_REPORT_DIR, "select-star", "2019-01-23T10-31-54_select-star.sql"),
        "report_name": "2019-01-23T10-31-54_select-star.sql",
        "csv_name": "2019-01-23T10-31-54_select-star.csv",
        "str": "SELECT * FROM `some_table`;",
        "rows": [],
        "description": [],
        "prefix_dt": datetime(2019, 1, 23, 10, 31, 54),
        "start_end_dt": [
            datetime(2019, 1, 23, 10, 31, 54, 450265),
            datetime(2019, 1, 23, 10, 31, 54, 999999)
        ]
    }


@pytest.fixture()
def show():
    out_csv = join(X_REPORT_DIR, "show-columns", "2019-01-23T10-31-55_show-columns.csv")

    with open(out_csv) as show_csv_file:
        reader = csv.reader(show_csv_file)
        csv_content = list(reader)
        rows = csv_content[1:]
        headers = csv_content[:1][0]
        description = [(header,) for header in headers]

    return {
        "src": join(RSRC, "sql", "show-columns.sql"),
        "report": join(X_REPORT_DIR, "show-columns", "2019-01-23T10-31-55_show-columns.sql"),
        "report_name": "2019-01-23T10-31-55_show-columns.sql",
        "str": "SELECT `TABLE_SCHEMA`,`TABLE_NAME`,`COLUMN_NAME`,`ORDINAL_POSITION`"
                   " FROM `information_schema`.`COLUMNS`"
                   " WHERE `TABLE_SCHEMA` = \"information_schema\" AND `TABLE_NAME` = \"COLUMNS\""
                   " ORDER BY `ORDINAL_POSITION` ASC"
                   " LIMIT 25;",
        "csv": out_csv,
        "csv_name": "2019-01-23T10-31-55_show-columns.csv",
        "rows": rows,
        "description": description,
        "headers": headers,
        "prefix_dt": datetime(2019, 1, 23, 10, 31, 55),
        "start_end_dt": [
            datetime(2019, 1, 23, 10, 31, 55, 1),
            datetime(2019, 1, 23, 10, 31, 55, 2)
        ]
    }
