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

# CPIO Example comment: Installed and python default imports. Alphabetical order
import numpy as np


from bokeh.models import ColumnDataSource
from typing_extensions import override

# CPIO Example comment: Own library imports. Alphabetical order
from lsst_ts.bokeh.utils.bokeh_framework.data_aggregator import DataAggregator
from lsst_ts.bokeh.apps.examples.bokeh_framework_simple_plot import simple_plot_layout

# CPIO Example comment: Type checking imports (optional). Alphabetical order
from typing import TYPE_CHECKING

# CPIO Example comment: If Variables are only for type checking they may be declared inside this conditional
# but is optional to have it inside
if TYPE_CHECKING:
    from typing import Optional
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

__all__ = ['SimplePlotDataAggregator']

# CPIO Example comment: child class that inherits from DataAggregator. has the responsibility of creating and
# interacting with plotting data
class SimplePlotDataAggregator(DataAggregator):

    def __init__(self) -> None:
        super().__init__()
        # CPIO Example comment: Attributes used by the class must be defined in the __init__ method.
        # Type is used to set the variable type, it has 2 uses:
        # .- Other readers can know which is the type value (without checking through the code)
        # .- Static checker may be run to check is variables are correctly used according to its type
        # Attributes by definition should be private hence '_' is needed
        self._plot_data = None # type: Optional[ColumnDataSource]

    # CPIO Example comment: A decorator is used in order to advise that the method is override  from the
    # base call. Override decorator really doesn't affect the method execution
    @override
    # CPIO Example comment: Method overriden from DataAggregator to set up the plotting data.
    # It may be empty.
    def setup(self, layout: 'Layout') -> None:
        # force type layout also for typing purposes
        assert (isinstance(layout, simple_plot_layout.SimplePlotLayout))
        x = np.arange(0, 100, 0.01)
        cosine = np.cos(x)
        data = {'x': x, 'y': cosine}
        self._plot_data = ColumnDataSource(data)
        layout.plot.line(source=data)