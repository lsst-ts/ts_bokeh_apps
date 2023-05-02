from abc import ABC, abstractmethod
import logging

from typing import TYPE_CHECKING

from lsst_ts.library.utils.logger import get_logger

if TYPE_CHECKING:
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

_log = get_logger("bokeh_framework.interaction")

class Interaction(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def setup(self, layout: 'Layout') -> None:
        """
        Abstract method provided to be overwritten
        by the framework user to define the application interaction
        :param layout: Layout class with all the UIElements available
        :return: None
        """
        pass


class VoidInteraction(Interaction):

    def setup(self, layout: 'Layout') -> None:
        _log.warning("No definition of Interaction Available")
