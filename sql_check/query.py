import re


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
