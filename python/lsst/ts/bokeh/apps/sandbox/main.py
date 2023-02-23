import datetime
import random

from bokeh import plotting # type: ignore
from lsst.ts.bokeh.widgets.date_interval_selector import DateIntervalSelector
from lsst.ts.bokeh.widgets.combobox_selector import IntegerComboboxSelector

if __name__.startswith("bokeh_app_"):
    print("name: {}".format(__name__))
    doc = plotting.curdoc()
    doc.add_root(DateIntervalSelector("test_widget").create())
    integer_selector = IntegerComboboxSelector("integer_selector", label="SalIndex")
    doc.add_root(integer_selector.create())
    integer_selector.update_menu([("1", "1"), ("2", "2"), ("3", "3")])

