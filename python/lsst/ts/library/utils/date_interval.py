from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Union

import pytz

@dataclass(frozen=True)
class DateInterval:
    begin: datetime
    end: datetime

    @staticmethod
    def from_date(begin_date: date, end_date: Union[date, timedelta]) -> 'DateInterval':
        """
        Create a Date Interval out of a date
        :param begin_date: begin date for the interval
        :param end_date: end date or timedelta to define the end date
        :return: a DateInterval instance
        """
        if isinstance(end_date, timedelta):
            end_date = begin_date + end_date
        begin_datetime = datetime.combine(begin_date, datetime.min.time(), tzinfo=pytz.UTC)
        end_datetime = datetime.combine(end_date, datetime.min.time(), tzinfo=pytz.UTC)
        return DateInterval(begin_datetime, end_datetime)

    def is_date_in_interval(self, dt: datetime) -> bool:
        """
        Checks if dt is inside the date interval defined in this instance
        :param dt: date to be checked
        :return: True if date is inside date interval else false
        """
        return self.begin < dt < self.end
