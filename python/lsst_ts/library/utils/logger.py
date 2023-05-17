import logging
import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger

_log_identifier = "ts_apps"
_log = logging.getLogger(_log_identifier)
_handler = logging.NullHandler()
_log.addHandler(_handler)
_log.setLevel(level=logging.INFO)

_formatter = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'

def get_logger(logger: str) -> 'Logger':
    """
    :param logger:
    :return:
    """
    logger_identifier = f"{_log_identifier}.{logger}"
    return logging.getLogger(logger_identifier)

def initialize_stdout_logger() -> None:
    """
    :return:
    """
    formatter = logging.Formatter(_formatter)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    _log.addHandler(handler)

def initialize_file_logger(file: str) -> None:
    """
    :param file:
    :return:
    """
    formatter = logging.Formatter(_formatter)
    handler = logging.FileHandler(file)
    handler.setFormatter(formatter)
    _log.addHandler(handler)

def add_custom_handler(handler: logging.Handler):
    _log.addHandler(handler)


def set_log_level(level: int):
    _log.setLevel(level=level)