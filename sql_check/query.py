#!/usr/bin/env python3
import argparse
import csv
import logging
import os.path
import re
from datetime import datetime

import yaml

import prefix
from CursorProvider import CursorProvider

log = logging.getLogger(__name__)


def str_from_file(file_path):
    """
    Get query contained within file as a single line query without indentation or comments.

    :param file_path: file containing a single SQL query
    :type file_path: str
    :return: The query from the file as a single line string
    """
    return re.sub(" +", " ",
                  ' '.join([
                      re.sub("--.*", "", line.strip())
                      for line in open(file_path)
                      if not line.strip().startswith('--') and line.strip()
                  ]))


def execute(file_path, directory=None):
    """
    Execute the query, append a report to the file (or his copy) (start & end time, duration, n rows and result file)
     and write results into a csv, if any, with the same name as the working file

    :param file_path: file containing a single SQL query
    :type file_path: str
    :param directory: where to create a copy of the file, prefixed with timestamp. No directory means no copy.
    :type directory: str
    :return: data queried from the database
    :rtype: {'name': str,'headers': list<str>, 'rows': list<tuple<any>>}
    """
    log.debug("ENTER execute({}, {})".format(file_path, directory))
    query_path = prefix.timestamp(file_path, directory) if directory else file_path

    cursor = CursorProvider().cursor()

    query = str_from_file(query_path)

    log.debug("Executing query: {}".format(query))
    start_time = datetime.now()
    cursor.execute(query)
    end_time = datetime.now()
    log.debug("Done executing query")

    rows = cursor.fetchall()
    log.debug("  With results: {}".format(rows))

    headers = [header[0] for header in cursor.description]
    result_path = os.path.splitext(query_path)[0] + ".csv"

    if rows:
        log.info("Writes results to {}".format(result_path))
        with open(result_path, "w") as result_file:
            csv_writer = csv.writer(result_file, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(headers)
            [csv_writer.writerow(row) for row in rows]

    log.info("Append results to {}".format(query_path))
    with open(query_path, "a+") as file:
        file.write("\n"
                   "-- START TIME: {start}\n"
                   "-- END TIME: {end}\n"
                   "-- DURATION: {duration}\n"
                   "-- ROWS COUNT: {count}\n"
                   "-- RESULT FILE: {file}\n".format(
                    start=start_time.isoformat(),
                    end=end_time.isoformat(),
                    duration=end_time - start_time,
                    count=len(rows),
                    file=os.path.basename(result_path) if rows else "N/A"
                    ))

    log.debug("EXIT execute({}, {})".format(file_path, directory))
    return {
        "name": os.path.basename(os.path.splitext(file_path)[0]),
        "headers": headers,
        "rows": rows
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs a SQL SELECT statement, append a report to the file "
                                                 "and export results, if any, to a csv file")

    parser.add_argument('file_path', help="A file containing a single SELECT statement")
    parser.add_argument('-d', '--directory', help="Where to create a timestamp prefixed copy  of the input file"
                                                  " and operate on it rather than the original")

    args = parser.parse_args()

    with open("application.yml", "r") as config_file:
        config = yaml.load(config_file)

    logging.basicConfig(level=config["logging"]["level"], format=config["logging"]["format"])

    execute(args.file_path, args.directory)
