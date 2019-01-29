import logging
import os.path
from datetime import datetime
from shutil import copyfile

log = logging.getLogger(__name__)


def timestamp(file_path, directory=None):
    """
    Create a copy of provided file prefixed with a timestamp

    :param file_path: file to create a copy of
    :type file_path: str
    :param directory: where to create the copy, default is next to the original file
    :type directory: str
    :return: absolute path to created copy
    """
    prefix = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    copy_path = os.path.join(
        directory if directory else os.path.dirname(file_path),
        prefix + "_" + os.path.basename(file_path)
    )

    log.info("Copy file {} to {}".format(file_path, copy_path))
    copyfile(file_path, copy_path)

    return copy_path
