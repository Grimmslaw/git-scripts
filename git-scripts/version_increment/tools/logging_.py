import logging

# TODO: the format
FORMAT = ''


def setup(lvl: int = logging.INFO, fmt: str = FORMAT):
    logging.basicConfig(format=fmt, level=lvl)
