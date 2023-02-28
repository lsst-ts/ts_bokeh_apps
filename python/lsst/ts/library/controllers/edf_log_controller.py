from datetime import datetime
from typing import Tuple, List

from lsst.ts.library.utils.date_interval import DateInterval
from lsst.ts.library.data_controller.edf_data_controller import EDFDataController


class EdfLogController:
    _SAL_INDEX_TP_N_RETURN = 10
    _LOG_TOPIC = "lsst.sal.Script.logevent_logMessage"

    def __init__(self, data_controller: EDFDataController):
        self._data_controller = data_controller

    def get_last_n_sal_index(self, n: int = _SAL_INDEX_TP_N_RETURN) -> List[Tuple[datetime, int]]:
        """
        Returns datetime and sal_index for all messages which date is inside the interval selected
        :param date_interval: date interval that messages should belong to
        :return: List with tuples values containing datetime and sal_index
        """
        values = await self._data_controller.select_top_n(EdfLogController._LOG_TOPIC, ["salIndex"], n)
        return values

    def get_sal_index_by_interval(self, date_interval: DateInterval) -> List[Tuple[datetime, int]]:
        """
        Returns datetime and sal_index for all messages which date is inside the interval selected in dumped DB
        :param date_interval: date interval that messages should belong to
        :return: List with tuples values containing datetime and sal_index
        """
        values = await self._data_controller.select_interval(EdfLogController._LOG_TOPIC, ["salIndex"], None)
        return values

    def get_log_information(self, sal_index: int, search_dt: datetime) -> str:
        """
        Search the message associated with the sal_index and the time in dumped DB
        :param sal_index: int with the sal index information
        :param search_dt: datetime of the message
        :return: string with the messages or raise exception if not found
        """
        pass
