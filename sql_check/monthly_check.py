import os
from datetime import datetime
from getpass import getuser

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

    results = []
    for query in os.listdir(source):
        query_src = os.path.join(source, query)
        query_name = os.path.splitext(query)[0]
        query_dir = os.path.join(report_directory, query_name)
        os.mkdir(query_dir)

        result = runner.execute(query_src, query_dir)
        results.append(result)

    write_report(month, results, report_directory)

    return report_directory


def write_report(month, results, report_directory):
    """
    Write a report crunching the results in a nice markdown readable format

    :param month: period the report is about
    :type month: date
    :param results: list queries's results
    :type results: {'name': str,'headers': list<str>, 'rows': list<tuple<any>>}
    :param report_directory: where the report must be written
    :type report_directory: str
    """
    positives = [query for query in results if query["rows"]]
    opening = "# Monthly Report for {month}\n" \
              "\n" \
              "- produced at: {date}\n" \
              "- produced by: {user}\n" \
              "- result: {result}\n".format(
                month=month.strftime("%B %Y"),
                date=datetime.today().replace(microsecond=0).isoformat(),
                user=getuser(),
                result="positive" if positives else "negative")

    brief = "## Positive Queries\n" + "".join(["- {}\n".format(query["name"]) for query in positives])

    names = [query["name"] for query in results]
    counts = [len(query["rows"]) for query in results]
    name_pad_size = max(len(max(names, key=len)), len("query"))
    count_pad_size = max(len(str(max(counts))), len("count"))

    table_header = "| {query} | {count} |\n".format(
        query="query".ljust(name_pad_size, " "),
        count="count".rjust(count_pad_size, " "))
    table_def = "|-{query}-|-{count}:|\n".format(
        query="-" * name_pad_size,
        count="-" * count_pad_size)
    table_body = "".join([
        "| {query} | {count} |\n".format(
            query=query["name"].ljust(name_pad_size, " "),
            count=str(len(query["rows"])).rjust(count_pad_size, " "))
        for query in results])

    summary = "## Summary\n" + table_header + table_def + table_body

    with open(os.path.join(report_directory, month.strftime("%Y-%m-%B") + "-report.md"), "w") as report_file:
        report_file.write(opening + "\n" + brief + "\n" + summary)
