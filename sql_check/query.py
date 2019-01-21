import re
from datetime import datetime

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


def execute(file_path):
    """
    Execute the query, append a report to the file (start & end time, duration, n rows and result file) and copy results
    next to the original file with the same file name but the extension being csv.

    :param file_path: file containing a single SQL query
    :type file_path: str
    :return: data queried from the database
    :rtype: {'headers': [str], 'rows': [[any]]}
    """

    cursor = CursorProvider().cursor()

    cursor.execute(str_from_file(file_path))

    start_time = datetime.now()
    cursor.fetchall()
    start_end = datetime.now()

    return None
