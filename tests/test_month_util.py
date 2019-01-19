from datetime import date

import mock

from sql_check import month_util


@mock.patch("sql_check.month_util.date")
def test_previous_month_nominal_case(mock_date):
    mock_date.today.return_value = date(2016, 6, 24)
    assert month_util.previous_month() == date(2016, 5, 1)


@mock.patch("sql_check.month_util.date")
def test_previous_month_january_case(mock_date):
    mock_date.today.return_value = date(2017, 1, 1)
    assert month_util.previous_month() == date(2016, 12, 1)


def test_month_from_str():
    assert month_util.month_from_str("201901") == date(2019, 1, 1)
