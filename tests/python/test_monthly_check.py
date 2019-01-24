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
        produced_directory = monthly_check(date(2019, 1, 1), source="test/assets", output=output)
        assert produced_directory == os.path.join(output, "2019-01-January")
        assert os.path.isdir(produced_directory)
        assert os.path.isdir(os.path.join(produced_directory, "select-star"))
        assert os.path.isdir(os.path.join(produced_directory, "show-databases"))
        assert os.path.isfile(os.path.join(produced_directory, "2019-01-January.md"))
    finally:
        shutil.rmtree(output)
