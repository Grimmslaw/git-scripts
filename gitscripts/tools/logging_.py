"""A module containing methods for setting up and retrieving a project's logger."""

import logging

FORMAT = '[%(asctime)s] [%(module)15s] . [%(funcName)-22s:%(lineno)4s]   %(message)s'


def setup(lvl: int = logging.INFO, fmt: str = FORMAT) -> None:
    """
    Sets up a logger at the given level using the given format.

    :param int lvl:
        the lowest level to log by default
    :param fmt:
        the format of the messages to be logged
    """
    logging.basicConfig(format=fmt, level=lvl)
    gitpython_logger = logging.getLogger('git.cmd')
    gitpython_logger.setLevel(logging.CRITICAL)
