import os

from month import previous


def monthly_check(month=previous(), source=None, output=None):
    """
    Create a sub directory inside the output directory named after the month (YYYY-mm)
    Inside this directory, create a sub directory for each query from the source directory
    Create and run a timestamped copy of each query, write results next to them and append result to the copy
    Write a report at the monthly named directory level with count of each query

    :param month: we are running the check for
    :type month: Date
    :param source: a directory containing sql files, each containing a single SELECT statement, can configured from yml
    :type source: str | os.PathLike
    :param output: a directory where to write results and reports, can configured from yml
    :type output: str | os.PathLike
    :return: the path to the report directory
    :rtype: str | os.PathLike
    """

    report_directory = os.path.join(
        output,
        month.strftime("%Y-%m-%B")
    )

    if os.path.exists(report_directory):
        raise FileExistsError(report_directory)

    os.mkdir(report_directory)

    return report_directory
