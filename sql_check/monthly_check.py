import os

import query as runner
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

    if not os.path.isdir(source):
        raise FileNotFoundError(source)

    queries = os.listdir(source)
    for query in queries:
        query_src = os.path.join(source, query)
        query_dir = os.path.join(report_directory, os.path.splitext(query)[0])
        os.mkdir(query_dir)
        runner.execute(query_src, query_dir)

    with open(os.path.join(report_directory, month.strftime("%Y-%m-%B") + "-report.md"), "w") as report_file:
        report_file.write("# Monthly Report for {month}\n"
                          .format(month=month.strftime("%B %Y")))

    return report_directory
