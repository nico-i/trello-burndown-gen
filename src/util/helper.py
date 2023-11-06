import argparse
import datetime

from src.util.constants import DATE_FORMAT


def truncate_txt(txt, max_len=10):
    """
    Truncate the txt and append '...' if it exceeds the maximum length
    :param txt: The txt to truncate
    :param max_len: The maximum length for the txt
    :return: The truncated txt
    """
    if len(txt) > max_len:
        return txt[:max_len] + '...'
    return txt


def valid_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, DATE_FORMAT)
    except ValueError:
        msg = f"Not a valid date: '{date_string}'."
        raise argparse.ArgumentTypeError(msg)
