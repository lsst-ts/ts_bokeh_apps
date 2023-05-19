from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import pandas as pd
from lsst_ts.library.data_controller.efd.data_controller import DataController
from lsst_ts.library.data_controller.efd.simulated_data_controller import \
    SimulatedDataController
from lsst_ts.library.utils.date_interval import DateInterval

if TYPE_CHECKING:
    from pandas import DataFrame


class EfdLogController:
    _SAL_INDEX_TP_N_RETURN = 10
    _LOG_TOPIC = "lsst.sal.Script.logevent_logMessage"

    def __init__(self, data_controller: DataController) -> None:
        self._data_controller = data_controller

    async def get_logs_last_n(self, n: int = _SAL_INDEX_TP_N_RETURN) -> "DataFrame":
        """
        Returns datetime and sal_index for all messages
        which date is inside the interval selected
        :param n:
        :param date_interval: date interval that messages should belong to
        :return: List with tuples values containing datetime and sal_index
        """
        values = await self._data_controller.select_top_n(
            EfdLogController._LOG_TOPIC, ["ScriptID", "salIndex", "message"], n
        )
        return values

    async def get_logs_by_interval(self, date_interval: DateInterval) -> "DataFrame":
        """
        Search the message associated with the
        sal_index and the time
        :param date_interval:
        :param sal_index: int with the sal index information
        :param search_dt: datetime of the message
        :return: string with the messages or raise exception if not found
        """
        values = await self._data_controller.select_interval(
            EfdLogController._LOG_TOPIC,
            ["ScriptID", "message", "salIndex", "traceback"],
            date_interval,
        )
        return values

    async def get_n_logs_by_date(
        self, begin_date: datetime, minimum_return_values: int = 0
    ) -> "DataFrame":
        """
        Search the message associated with the sal_index and the time
        :param begin_date:
        :param minimum_return_values:
        :return: string with the messages or raise exception if not found
        """
        saved_dataframes = []  # type: DataFrame
        registers_available = 0
        date_interval = DateInterval.from_date(begin_date, timedelta(hours=-12))
        while registers_available < minimum_return_values:
            values = await self.get_logs_by_interval(date_interval)
            registers_available += len(values)
            saved_dataframes.insert(0, values)
            end_time = date_interval.begin
            date_interval = DateInterval.from_date(end_time, timedelta(hours=-12))
        return pd.concat(saved_dataframes)


if __name__ == "__main__":
    data_controller_example = SimulatedDataController()
    efd_log_controller = EfdLogController(data_controller_example)
    # date_interval = DateInterval.from_date(datetime.today(),
    # timedelta(hours = 1))
    # response = await efd_log_controller.
    # get_n_logs_by_date(datetime.today(), 10)
    # print(response)
