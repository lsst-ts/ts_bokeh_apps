import numpy as np
from bokeh.models import ColumnDataSource
from typing_extensions import override

from lsst_ts.bokeh.utils.bokeh_framework.data_aggregator import DataAggregator
from lsst_ts.bokeh.apps.examples.bokeh_framework_simple_plot import simple_plot_layout

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

class SimplePlotDataAggregator(DataAggregator):

    def __init__(self) -> None:
        super().__init__()
        self._plot_data = None # type: Optional[ColumnDataSource]

    @override
    def setup(self, layout: 'Layout') -> None:
        assert (isinstance(layout, simple_plot_layout.SimplePlotLayout))
        x = np.arange(0, 100, 0.01)
        cosine = np.cos(x)
        data = {'x': x, 'y': cosine}
        self._plot_data = ColumnDataSource(data)
        layout.plot.line(source=data)