import datetime
from typing import TYPE_CHECKING

from bokeh.io import show
from bokeh.models import DatePicker, LayoutDOM, Row  # type: ignore
from lsst_ts.library.pub_sub.observable import Observable
from lsst_ts.library.utils.date_interval import DateInterval

if TYPE_CHECKING:
    from typing import Any


class DateIntervalSelector(Observable[DateInterval]):
    """
    Select a date interval with two date pickers
    """

    def __init__(self, name: str = "date_interval_selector") -> None:
        super(DateIntervalSelector, self).__init__()
        self._name = name
        self._end_date = DatePicker()  # type: DatePicker
        self._initial_date = DatePicker()  # type: DatePicker

    def create(self) -> LayoutDOM:
        """
        Create the widget and return it to be placed in the doc
        :return: LayoutDOM
        """
        self._create_initial_date()
        self._create_end_date()
        return Row(name=self._name, children=[self._initial_date, self._end_date])

    def _create_initial_date(self) -> None:
        """
        :return:
        """
        self._initial_date = DatePicker()
        self._initial_date.value = datetime.date.today()
        self._initial_date.max_date = datetime.date.today()
        self._initial_date.on_change("value", self._initial_date_changed)

    def _create_end_date(self) -> None:
        self._end_date = DatePicker()
        self._end_date.value = datetime.date.today()
        self._end_date.max_date = datetime.date.today()
        self._end_date.on_change("value", self._end_date_changed)

    def _initial_date_changed(
        self, attr: "Any", old_value: "Any", new_value: "Any"
    ) -> None:
        if self._end_date.value:
            self._notify(DateInterval(new_value, self._end_date.value))

    def _end_date_changed(
        self, attr: "Any", old_value: "Any", new_value: "Any"
    ) -> None:
        if self._initial_date.value:
            self._notify(DateInterval(new_value, self._initial_date.value))


# Just to have a first view of the object
if __name__ == "__main__":
    date_selector = DateIntervalSelector()
    show(date_selector.create())
