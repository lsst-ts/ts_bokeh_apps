# This file is part of ts_bokeh_apps.
#
# Developed for the Vera Rubin Observatory Telescope and Site.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import TYPE_CHECKING

import numpy as np
from bokeh.models import ColumnDataSource
from lsst_ts.bokeh.apps.examples.bokeh_framework_simple_plot import \
    simple_plot_layout
from lsst_ts.bokeh.utils.bokeh_framework.data_aggregator import DataAggregator
from typing_extensions import override

if TYPE_CHECKING:
    from typing import Optional  # noqa: F401

    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

__all__ = ["SimplePlotDataAggregator"]


# child class that inherits from DataAggregator. has the responsibility of
# creating and interacting with plotting data
class SimplePlotDataAggregator(DataAggregator):
    def __init__(self) -> None:
        super().__init__()
        # Attributes used by the class must be defined in the __init__ method.
        # Type is used to set the variable type, it has 2 uses:
        # .- Other readers can know which is the type value (without checking
        # through the code)
        # .- Static checker may be run to check is variables are correctly used
        # according to its type Attributes by definition should be private
        # hence '_' is needed
        self._plot_data = None  # type: Optional[ColumnDataSource]

    # A decorator is used in order to advise that the method is override from
    # the base call. Override decorator really doesn't affect the method
    # execution
    @override
    # Method overriden from DataAggregator to set up the plotting data.
    # It may be empty.
    def setup(self, layout: "Layout") -> None:
        # force type layout also for typing purposes
        assert isinstance(layout, simple_plot_layout.SimplePlotLayout)
        x = np.arange(0, 100, 0.01)
        cosine = np.cos(x)
        data = {"x": x, "y": cosine}
        self._plot_data = ColumnDataSource(data)
        layout.plot.line(source=data)
