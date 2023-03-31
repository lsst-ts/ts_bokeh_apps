from abc import ABC, abstractmethod
from typing import List

from pandas.core.interchange import dataframe

from lsst_ts.library.utils.date_interval import DateInterval


class DataController(ABC):

    @abstractmethod
    async def get_topic_available(self) -> List[str]:
        pass

    @abstractmethod
    async def get_fields_available(self, topic: str) -> List[str]:
        pass

    @abstractmethod
    async def select_top_n(self, topic: str, fields: List[str], last_n: int) -> dataframe:
        pass

    @abstractmethod
    async def select_interval(self, topic: str, fields: List[str], date_interval: DateInterval) -> dataframe:
        pass

    @abstractmethod
    async def select_packed_interval(self, topic: str, fields: List[str], date_interval: DateInterval) -> dataframe:
        pass
