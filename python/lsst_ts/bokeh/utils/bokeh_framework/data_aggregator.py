import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from lsst_ts.library.utils.logger import get_logger

if TYPE_CHECKING:
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

_log = get_logger("bokeh_framework.data_aggregator")

class DataAggregator(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def setup(self, layout: 'Layout') -> None:
        """
        Abstract method provided to be overwritten by the
        framework user to define data available inside the application
        :param layout: Layout class with all the UIElements available
        :return: None
        """
        raise NotImplementedError()


class VoidDataAggregator(DataAggregator):

    def __init__(self) -> None:
        super().__init__()

    def setup(self, layout: 'Layout') -> None:
        """
        :param layout:
        :return:
        """
        _log.warning("No definition of Data Aggregation Available")
