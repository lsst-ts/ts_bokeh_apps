from datetime import date, timedelta, datetime
from typing import Union

from bokeh import plotting # type: ignore

from lsst.ts.bokeh.widgets.date_selector import DateSelector
from lsst.ts.bokeh.widgets.combobox_selector import ComboboxSelector
from lsst.ts.bokeh.widgets.log_viewer import LogViewer
from lsst.ts.library.controllers.simulated_log_controller import SimulatedLogController
from lsst.ts.library.utils.date_interval import DateInterval


class LogViewerApplication:

    def __init__(self):
        self._log_controller = SimulatedLogController()
        self._exception_viewer = None
        self._salindex_selector = None
        self._date_selector = None
        self._log_viewer = None
        self._doc = plotting.curdoc()

    def deploy(self) -> None:
        """
        Deploy log viewer application
        """
        self._date_selector = DateSelector("date_selector")
        self._date_selector.attach_callable(self._date_changed)
        self._doc.add_root(self._date_selector.create())
        self._salindex_selector = ComboboxSelector("salindex_selector")
        self._doc.add_root(self._salindex_selector.create())
        self._log_viewer = LogViewer(name = "log_viewer")
        self._doc.add_root(self._log_viewer.create())
        self._salindex_selector.attach_callable(self._salindex_changed)

    def initialize(self):
        """
        :return:
        """
        self._date_changed(date.today())

    def _salindex_changed(self, new_index: str) -> None:
        """
        Callback method to be executed when the sal index selection is changed
        :param new_index: sal index selected
        """
        print("new_index: {}".format(new_index))
        sal_index_str, date_str = new_index.split('@')
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f%z')
        log_information = self._log_controller.get_log_information(int(sal_index_str), dt)
        self._log_viewer.update(log_information)

    def _date_changed(self, date_selected: Union[date, DateInterval]):
        """
        Callback method to be executed when the data selection is changed
        :param date_selected: Date or date interval with the dates selected
        """
        if isinstance(date_selected, date):
            one_day_delta = timedelta(1)
            date_interval = DateInterval.from_date(date_selected, one_day_delta)
        values = self._log_controller.get_sal_index_by_interval(date_interval)
        values_str = ["{0:08d}@{1}".format(salindex, datetime.strftime(sdate, '%Y-%m-%d %H:%M:%S.%f%z')) for sdate, salindex in values]
        self._salindex_selector.update(values_str)


if __name__.startswith("bokeh_app_"):
    print("name: {}".format(__name__))
    app = LogViewerApplication()
    app.deploy()
    #pp.initialize()

if __name__ == '__main__':
    widget = LogViewerApplication()
    widget.deploy()
    widget.initialize()

