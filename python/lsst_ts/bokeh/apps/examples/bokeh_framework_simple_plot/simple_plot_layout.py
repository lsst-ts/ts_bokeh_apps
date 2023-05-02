from bokeh.models import Row
from bokeh.plotting import figure
from typing_extensions import override

from lsst_ts.bokeh.apps.examples.bokeh_framework_simple_plot.simple_plot_data_aggregator import \
    SimplePlotDataAggregator
from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from bokeh.models.ui.ui_element import UIElement

class SimplePlotLayout(Layout):

    def __init__(self) -> None:
        super().__init__(data_aggregator=SimplePlotDataAggregator())
        self._plot = None # type: Optional[figure]

    @override
    def define(self) -> 'UIElement':
        self._plot = figure()
        return Row(children=[self._plot], name="SimplePlot")
    @property
    def plot(self) -> 'figure':
        assert(self._plot is not None)
        return self._plot