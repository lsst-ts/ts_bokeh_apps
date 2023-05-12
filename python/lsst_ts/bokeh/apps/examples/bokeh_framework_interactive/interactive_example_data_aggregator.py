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
import asyncio
import numpy as np

# CPIO Example comment:  Installed and python default selected component imports. Alphabetical order
from bokeh.palettes import RdYlBu3
from bokeh.models import ColumnDataSource
from itertools import chain
from typing_extensions import override

# CPIO Example comment: Own library imports. Alphabetical order
from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive import interactive_example_layout
from lsst_ts.bokeh.utils.bokeh_framework.data_aggregator import DataAggregator

# CPIO Example comment: Type checking imports (optional). Alphabetical order
from typing import TYPE_CHECKING

# CPIO Example comment: If Variables are only for type checking they may be declared inside this conditional
# but is optional to have it inside
if TYPE_CHECKING:
    from numpy import ndarray, dtype
    from typing import Union, Sequence, Any, List, Dict
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

__all__ = ['InteractiveExampleDataAggregator']

# CPIO Example comment: function to concatenate 2 Sequence. It is a quick method to avoid errors on
# static analyzers but should be changed to a better solution
def concat(a: 'Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]',
           b: 'Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]') -> 'List[Any]':
    return list(chain(a, b))


# CPIO Example comment: child class that inherits from DataAggregator. has the responsibility of creating and
# interacting with plotting data
class InteractiveExampleDataAggregator(DataAggregator):
    """
    Data aggregator class for the app.
    """

    def __init__(self) -> None:
        super().__init__()
        # CPIO Example comment: Attributes used by the class must be defined in the __init__ method.
        # Type is used to set the variable type, it has 2 uses:
        # .- Other readers can know which is the type value (without checking through the code)
        # .- Static checker may be run to check is variables are correctly used according to its type
        # Attributes by definition should be private hence '_' is needed
        self._iterator = 0 # type: int
        self._data_source = ColumnDataSource() # type: ColumnDataSource

    # CPIO Example comment: A decorator is used in order to advise that the method is override  from the
    # base call. Override decorator really doesn't affect the method execution
    @override
    # CPIO Example comment: Method overriden from DataAggregator to set up the plotting data.
    # It may be empty like in this case.
    def setup(self, layout: 'Layout') -> None:
        # force type layout also for typing purposes
        # To avoid circular import full module must be imported
        assert (isinstance(layout, interactive_example_layout.InteractiveExampleLayout))

    # CPIO Example comment: According to general OOP programming concepts, attributes should be private
    # and be accessible using a getter. In python concretely all attributes are declared a 'private' beginning
    # with "_" and use @property decorator to create the getter to access the attribute
    @property
    def data_source(self) -> ColumnDataSource:
        assert(self._data_source is not None)
        return self._data_source

    @data_source.setter
    def data_source(self, data_source: ColumnDataSource) -> None:
        assert (self._data_source is not None)
        self._data_source = data_source

    def retrieve_data(self) -> None:
        """Retrieve data."""
        asyncio.run(self._retrieve_data_async())

    async def _retrieve_data_async(self) -> None:
        """
        Testing async methods in apps.
        """
        assert(self._data_source is not None)
        new_data = dict()  # type: Dict[str, Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]]
        new_data["x"] = concat(self._data_source.data["x"],
                                [np.random.random() * 70 + 15])
        new_data["y"] = concat(self._data_source.data["y"],
                                [np.random.random() * 70 + 15])
        new_data["text_color"] = concat(self._data_source.data["text_color"],
                                         [RdYlBu3[self._iterator % 3]])
        new_data["text"] = concat(self._data_source.data["text"], [str(self._iterator)])

        self._data_source.data = new_data
        self._iterator += 1