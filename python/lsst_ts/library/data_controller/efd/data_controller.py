from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from lsst_ts.library.utils.date_interval import DateInterval
from pandas import DataFrame

if TYPE_CHECKING:
    from typing import List


class DataController(ABC):
    @abstractmethod
    async def get_topic_available(self) -> List[str]:
        pass

    @abstractmethod
    async def get_fields_available(self, topic: str) -> List[str]:
        pass

    @abstractmethod
    async def select_top_n(
        self, topic: str, fields: List[str], last_n: int
    ) -> "DataFrame":
        pass

    @abstractmethod
    async def select_interval(
        self, topic: str, fields: List[str], date_interval: DateInterval
    ) -> "DataFrame":
        pass

    @abstractmethod
    async def select_packed_interval(
        self, topic: str, fields: List[str], date_interval: DateInterval
    ) -> "DataFrame":
        pass
