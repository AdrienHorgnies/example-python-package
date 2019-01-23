import os
import tempfile
from datetime import date, datetime

import mock

from monthly_check import monthly_check


@mock.patch("monthly_check.getpass.getuser")
@mock.patch("monthly_check.datetime")
def test_monthly_check(mock_datetime, mock_getuser):
    mock_datetime.return_value = datetime(2019, 1, 23, 10, 31, 54)
    mock_getuser.return_value = "aho"

    output = os.path.join(
        tempfile.gettempdir(),
        "test-reports"
    )
    if not os.path.isdir(output):
        os.mkdir(output)

    assert monthly_check(date(2019, 1, 1), source="test/assets", output=output)

    assert False
