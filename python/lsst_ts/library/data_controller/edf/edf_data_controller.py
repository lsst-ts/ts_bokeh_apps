from typing import List

from astropy.time import Time
from lsst_efd_client import EfdClient
from pandas.core.interchange import dataframe

from lsst_ts.library.utils.date_interval import DateInterval


class EDFDataController:
    """
    Controller to encapsulate the work with the EDF Database
    """

    def __init__(self, efd_client: str):
        self._efd = EfdClient(efd_client)

    async def get_topic_available(self) -> List[str]:
        return await self._efd.get_topics()

    async def get_fields_available(self, topic: str) -> List[str]:
        return await self._efd.get_fields(topic)

    async def select_top_n(self, topic: str, fields: List[str], last_n: int) -> dataframe:
        return self._efd.select_top_n(topic, fields, last_n)

    async def select_interval(self, topic: str, fields: List[str], date_interval: DateInterval) -> dataframe:
        begin_time, end_time = Time([date_interval.begin, date_interval.end], format='datetime', scale='utc')
        return self._efd.select_time_series(topic, fields, begin_time, end_time)

    async def select_packed_interval(self, topic: str, fields: List[str], date_interval: DateInterval) -> dataframe:
        begin_time, end_time = Time([date_interval.begin, date_interval.end], format='datetime', scale='utc')
        return self._efd.select_packed_time_series(topic, fields, begin_time, end_time)

