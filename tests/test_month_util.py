from datetime import date

import month_util


def test_previous_month_nominal_case():
    assert month_util.previous_month() == date(2016, 5, 1)


def test_previous_month_january_case():
    assert month_util.previous_month() == date(2016, 12, 1)


def test_month_from_str():
    assert month_util.month_from_str("201901") == date(2019, 1, 1)
