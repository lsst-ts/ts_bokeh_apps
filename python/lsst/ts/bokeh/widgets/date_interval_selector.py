import datetime
from bokeh.io import show # type: ignore
from bokeh.layouts import row # type: ignore
from bokeh.models import DatePicker, LayoutDOM  # type: ignore

from lsst.ts.library.utils.date_interval import DateInterval
from lsst.ts.library.pub_sub.observable import Observable


class DateIntervalSelector(Observable[DateInterval]):
    """
    Select a date interval with two date pickers
    """
    def __init__(self, name: str = "date_interval_selector"):
        super(DateIntervalSelector, self).__init__()
        self._name = name
        self._end_date = None
        self._initial_date = None

    def create(self) -> LayoutDOM:
        """
        Create the widget and return it to be placed in the doc
        :return: LayoutDOM
        """
        self._create_initial_date()
        self._create_end_date()
        return row(self._initial_date, self._end_date, name = self._name)

    def _create_initial_date(self):
        """
        :return:
        """
        self._initial_date = DatePicker()
        self._initial_date.value = datetime.date.today()
        self._initial_date.max_date = datetime.date.today()
        self._initial_date.on_change("value", self._initial_date_changed)

    def _create_end_date(self):
        self._end_date = DatePicker()
        self._end_date.value = datetime.date.today()
        self._end_date.max_date = datetime.date.today()
        self._end_date.on_change("value", self._end_date_changed)

    def _initial_date_changed(self, attr, old_value, new_value):
        if self._end_date.value:
            self._notify(DateInterval(new_value, self._end_date.value))

    def _end_date_changed(self, attr, old_value, new_value):
        if self._initial_date.value:
            self._notify(DateInterval(new_value, self._initial_date.value))

# Just to have a first view of the object
if __name__ == '__main__':
    date_selector = DateIntervalSelector()
    show(date_selector.create())
