#!/usr/bin/env python3
import argparse
import logging
import os
from datetime import datetime
from getpass import getuser

import yaml

import month as month_date
import query as runner


def monthly_check(month=None, source=None, output=None):
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

    if not os.path.isdir(source):
        raise FileNotFoundError(source)

    if os.path.exists(report_directory):
        raise FileExistsError(report_directory)

    os.mkdir(report_directory)

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
    :type report_directory: str | os.PathLike
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


if __name__ == "__main__":
    with open("application.yml", "r") as config_file:
        config = yaml.load(config_file)

    desc = "Runs all SQL statements from source directory, " \
           "writes results and reports in the output directory" \
           " in a sub directory corresponding to the month"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-s', '--source', default=config["monthly_check"]["source"],
                        help="directory where to find SQL SELECT statements,"
                             " one single statement per file. Can be configured with monthly_check.source")
    parser.add_argument('-o', '--output', default=config["monthly_check"]["output"],
                        help="Where to write the report. Can be configured with monthly_check.output.")
    parser.add_argument('-m', '--month', default=month_date.previous(), type=month_date.from_str,
                        help="6 digits, 4 for the year then 2 for the month (ex.: 201901 is Jan 2019)")

    args = parser.parse_args()

    logging.basicConfig(level=config["logging"]["level"], format=config["logging"]["format"])

    monthly_check(args.month, args.source, args.output)
