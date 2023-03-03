from datetime import date
from typing import Dict

from lsst_ts.library.data_controller.butler_data_controller import ButlerDataController


class ExposureController:

    def __init__(self, butler):
        self._butler = butler

    def get_exposition_information(self, sequence_number: int, obs_day: date) -> Dict[str, any]:
        """
        :param sequence_number:
        :param obs_day:
        :return:
        """
        obs_day_str = f"{obs_day.year}{obs_day.month}{obs_day.day}"
        record = self._butler.query_record("exposure", f"exposure.day_obs = {obs_day_str} and exposure.seq_num = {sequence_number}")
        if len(record) != 1:
            raise Exception("Only one record should be returned for this query")
        return record[0].toDict()

