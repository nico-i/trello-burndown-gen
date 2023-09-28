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
