from datetime import date, datetime
from bokeh.io import show # type: ignore
from bokeh.layouts import row # type: ignore
from bokeh.models import DatePicker # type: ignore

from lsst_ts.library.pub_sub.observable import Observable


class DateSelector(Observable[date]):
    """
    """
    def __init__(self, name: str = "date_selector"):
        super(DateSelector, self).__init__()
        self._name = name
        self._date_picker = None

    def create(self):
        """
        Create the widget and return it to be placed in the doc
        :return: LayoutDOM
        """
        self._create_date()
        return row(self._date_picker, name = self._name)

    def _create_date(self):
        self._date_picker = DatePicker()
        self._date_picker.value = date.today()
        self._date_picker.max_date = date.today()
        self._date_picker.on_change("value", self._date_changed)

    def _date_changed(self, attr, old_value, new_value):
        selected_datetime = datetime.strptime(new_value, "%Y-%m-%d")
        self._notify(selected_datetime.date())

# Just to have a first view of the object
if __name__ == '__main__':
    date_selector = DateSelector()
    show(date_selector.create())
