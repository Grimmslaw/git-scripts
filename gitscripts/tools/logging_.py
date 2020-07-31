import logging

FORMAT = '[%(asctime)s] [%(module)15s] . [%(funcName)-22s:%(lineno)4s]   %(message)s'


def setup(lvl: int = logging.INFO, fmt: str = FORMAT):
    logging.basicConfig(format=fmt, level=lvl)
    gitpython_logger = logging.getLogger('git.cmd')
    gitpython_logger.setLevel(logging.CRITICAL)
