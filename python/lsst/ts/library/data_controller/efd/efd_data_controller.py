from typing import TYPE_CHECKING

from astropy.time import Time
from lsst_efd_client import EfdClient
from lsst.ts.library.utils.date_interval import DateInterval
from pandas import DataFrame

if TYPE_CHECKING:
    from typing import List, cast


class EFDDataController:
    """
    Controller to encapsulate the work with the EFD Database
    """

    def __init__(self, efd_client: str):
        self._efd_client = efd_client

    async def get_topic_available(self) -> List[str]:
        efd = EfdClient(self._efd_client)
        topics = await efd.get_topics()
        topics_cast = cast(List[str], topics)
        return topics_cast

    async def get_fields_available(self, topic: str) -> List[str]:
        efd = EfdClient(self._efd_client)
        fields = await efd.get_fields(topic)
        fields_cast = cast(List[str], fields)
        return fields_cast

    async def select_top_n(
        self, topic: str, fields: List[str], last_n: int
    ) -> "DataFrame":
        efd = EfdClient(self._efd_client)
        return await efd.select_top_n(topic, fields, last_n)

    async def select_interval(
        self, topic: str, fields: List[str], date_interval: DateInterval
    ) -> "DataFrame":
        efd = EfdClient(self._efd_client)
        begin_time, end_time = Time(
            [date_interval.begin, date_interval.end], format="datetime", scale="utc"
        )
        values = await efd.select_time_series(topic, fields, begin_time, end_time)
        values_cast = cast(DataFrame, values)
        return values_cast

    async def select_packed_interval(
        self, topic: str, fields: List[str], date_interval: DateInterval
    ) -> "DataFrame":
        efd = EfdClient(self._efd_client)
        begin_time, end_time = Time(
            [date_interval.begin, date_interval.end], format="datetime", scale="utc"
        )
        values = efd.select_packed_time_series(topic, fields, begin_time, end_time)
        values_cast = cast(DataFrame, values)
        return values_cast
