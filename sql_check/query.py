import csv
import os.path
import re
from datetime import datetime

import prefix
from CursorProvider import CursorProvider


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
    :rtype: {'headers': list<str>, 'rows': list<tuple<any>>}
    """
    query_path = prefix.timestamp(file_path, directory) if directory else file_path

    cursor = CursorProvider().cursor()

    start_time = datetime.now()
    cursor.execute(str_from_file(query_path))
    end_time = datetime.now()

    rows = cursor.fetchall()
    headers = [header[0] for header in cursor.description]

    if rows:
        result_path = os.path.splitext(query_path)[0] + ".csv"

        with open(result_path, "w") as result_file:
            csv_writer = csv.writer(result_file, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(headers)
            [csv_writer.writerow(row) for row in rows]

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
                    file=result_path if rows else "N/A"
                    ))

    return {
        "headers": headers,
        "rows": rows
    }
