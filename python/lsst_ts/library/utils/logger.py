import logging
import sys


_log_identifier = "ts_apps"
_log = logging.getLogger(_log_identifier)
_handler = logging.NullHandler()
_log.addHandler(_handler)
_log.setLevel(level=logging.INFO)

_formatter = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'

def get_logger(logger: str):
    logger_identifier = f"{_log_identifier}.{logger}"
    return logging.getLogger(logger_identifier)

def initialize_stream_logger():
    formatter = logging.Formatter(_formatter)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    _log.addHandler(handler)