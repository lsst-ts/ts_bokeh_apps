from typing import List

from astropy.time import Time
from lsst_efd_client import EfdClient
from pandas.core.interchange import dataframe

from lsst_ts.library.utils.date_interval import DateInterval


class EFDDataController:
    """
    Controller to encapsulate the work with the EFD Database
    """

    def __init__(self, efd_client: str):
        self._efd_client = efd_client

    async def get_topic_available(self) -> List[str]:
        efd = EfdClient(self._efd_client)
        return await efd.get_topics()

    async def get_fields_available(self, topic: str) -> List[str]:
        efd = EfdClient(self._efd_client)
        return await efd.get_fields(topic)

    async def select_top_n(self, topic: str, fields: List[str], last_n: int) -> dataframe:
        efd = EfdClient(self._efd_client)
        return await efd.select_top_n(topic, fields, last_n)

    async def select_interval(self, topic: str, fields: List[str], date_interval: DateInterval) -> dataframe:
        efd = EfdClient(self._efd_client)
        begin_time, end_time = Time([date_interval.begin, date_interval.end], format='datetime', scale='utc')
        return await efd.select_time_series(topic, fields, begin_time, end_time)

    async def select_packed_interval(self, topic: str, fields: List[str], date_interval: DateInterval) -> dataframe:
        begin_time, end_time = Time([date_interval.begin, date_interval.end], format='datetime', scale='utc')
        return self._efd.select_packed_time_series(topic, fields, begin_time, end_time)

