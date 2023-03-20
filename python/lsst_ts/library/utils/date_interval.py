from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Union

import pytz

@dataclass(frozen=True)
class DateInterval:
    begin: datetime
    end: datetime

    @staticmethod
    def from_date(begin_date:  Union[date, datetime], end_date: Union[datetime, timedelta]) -> 'DateInterval':
        """
        Create a Date Interval out of a date
        :param begin_date: begin date for the interval
        :param end_date: end date or timedelta to define the end date
        :return: a DateInterval instance
        """
        if not isinstance(begin_date, datetime):
            begin_date = datetime.combine(begin_date, datetime.max.time(), tzinfo=pytz.UTC)
        if isinstance(end_date, timedelta):
            end_date = begin_date + end_date
        if begin_date > end_date:
            begin_date , end_date = end_date, begin_date
        return DateInterval(begin_date, end_date)

    @staticmethod
    def from_central_date(begin_date: Union[date, datetime], previous_date: timedelta, post_date: timedelta) -> 'DateInterval':
        """
        :param begin_date:
        :param previous_date:
        :param post_date:
        :return:
        """
        real_begin_date = begin_date - previous_date
        real_end_date = begin_date + post_date
        return DateInterval(real_begin_date, real_end_date)

    def is_date_in_interval(self, dt: datetime) -> bool:
        """
        Checks if dt is inside the date interval defined in this instance
        :param dt: date to be checked
        :return: True if date is inside date interval else false
        """
        return self.begin < dt < self.end


if __name__ == "__main__":
    date_interval = DateInterval.from_date(datetime.today(), timedelta(hours = -12))
    print(date_interval)
    new_date = date_interval.begin
    print(new_date)
    date_interval = DateInterval.from_date(new_date, timedelta(hours=-12))
    print(date_interval)
