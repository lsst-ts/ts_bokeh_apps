from datetime import date, datetime
from bokeh.models import DatePicker, Row  # type: ignore
from bokeh.io import show
from lsst_ts.library.pub_sub.observable import Observable

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Optional  # noqa: F401
    from bokeh.models import UIElement  # type: ignore # noqa: F401


class DateSelector(Observable[date]):
    """
    """

    def __init__(self, name: str = "date_selector") -> None:
        super(DateSelector, self).__init__()
        self._name = name
        self._date_picker = None  # type: Optional[DatePicker]

    def create(self) -> UIElement:
        """
        Create the widget and return it to be placed in the doc
        :return: LayoutDOM
        """
        self._create_date()
        return Row(children=[self._date_picker], name=self._name)

    def _create_date(self) -> None:
        self._date_picker = DatePicker()
        self._date_picker.value = date.today()
        self._date_picker.max_date = date.today()
        self._date_picker.on_change("value", self._date_changed)

    def _date_changed(self, attr: 'Any', old_value: 'Any', new_value: 'Any') -> None:
        selected_datetime = datetime.strptime(new_value, "%Y-%m-%d")
        self._notify(selected_datetime.date())


# Just to have a first view of the object
if __name__ == '__main__':
    date_selector = DateSelector()
    show(date_selector.create())
