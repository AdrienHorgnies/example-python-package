import os
import tempfile
from datetime import date, datetime

import mock

from monthly_check import monthly_check


@mock.patch("monthly_check.getuser")
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

    produced_directory = monthly_check(date(2019, 1, 1), source="test/assets", output=output)

    try:
        assert produced_directory == os.path.join(output, "2019-01-January")
        assert os.path.isdir(produced_directory)
    finally:
        os.removedirs(output)

    assert False
