from datetime import date

import mock

import month


@mock.patch("month.date")
def test_previous_nominal_case(mock_date):
    mock_date.today.return_value = date(2016, 6, 24)
    assert month.previous() == date(2016, 5, 1)


@mock.patch("month.date")
def test_previous_january_case(mock_date):
    mock_date.today.return_value = date(2017, 1, 1)
    assert month.previous() == date(2016, 12, 1)


def test_from_str():
    assert month.from_str("201901") == date(2019, 1, 1)
