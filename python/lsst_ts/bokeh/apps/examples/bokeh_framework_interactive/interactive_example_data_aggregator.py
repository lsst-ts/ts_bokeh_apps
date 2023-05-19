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

import asyncio
from itertools import chain
from typing import TYPE_CHECKING

import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.palettes import RdYlBu3
from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive import \
    interactive_example_layout
from lsst_ts.bokeh.utils.bokeh_framework.data_aggregator import DataAggregator
from typing_extensions import override

if TYPE_CHECKING:
    from typing import Any, List, Sequence, Union

    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout
    from numpy import dtype, ndarray

__all__ = ["InteractiveExampleDataAggregator"]


# function to concatenate 2 Sequence. It is a quick method to avoid errors on
# static analyzers but should be changed to a better solution
def concat(
    a: "Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]",
    b: "Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]",
) -> "List[Any]":
    return list(chain(a, b))


# child class that inherits from DataAggregator. has the responsibility of
# creating and interacting with plotting data
class InteractiveExampleDataAggregator(DataAggregator):
    """
    Data aggregator class for the app.
    """

    def __init__(self) -> None:
        super().__init__()
        # Attributes used by the class must be defined in the __init__ method.
        # Type is used to set the variable type, it has 2 uses:
        # .- Other readers can know which is the type value (without checking
        # through the code)
        # .- Static checker may be run to check is variables are correctly used
        # according to its type
        # Attributes by definition should be private hence '_' is needed
        self._iterator = 0  # type: int
        self._data_source = ColumnDataSource()  # type: ColumnDataSource

    # A decorator is used in order to advise that the method is override
    # from the base call. Override decorator really doesn't affect the method
    # execution

    @override
    # Method overriden from DataAggregator to set up the plotting data.
    # It may be empty like in this case.
    def setup(self, layout: 'Layout') -> None:
        """
        Setup the data used in the application
        :param layout: Layout instance
        """
        # force type layout also for typing purposes
        # To avoid circular import full module must be imported
        assert isinstance(layout, interactive_example_layout.InteractiveExampleLayout)

    # According to general OOP programming concepts, attributes should be
    # private and be accessible using a getter. In python concretely all
    # attributes are declared a 'private' beginning with "_" and use @property
    # decorator to create the getter to access the attribute
    @property
    def data_source(self) -> ColumnDataSource:
        """
        :return:
        """
        assert self._data_source is not None
        return self._data_source

    @data_source.setter
    def data_source(self, data_source: ColumnDataSource) -> None:
        """
        :param data_source:
        """
        assert self._data_source is not None
        self._data_source = data_source

    def retrieve_data(self) -> None:
        """
        Retrieve data.
        """
        asyncio.run(self._retrieve_data_async())

    async def _retrieve_data_async(self) -> None:
        """
        """
        assert self._data_source is not None
        new_data = (
            dict()
        )  # typing: Dict[str, Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]] # noqa: WA505
        new_data["x"] = concat(
            self._data_source.data["x"], [np.random.random() * 70 + 15]
        )
        new_data["y"] = concat(
            self._data_source.data["y"], [np.random.random() * 70 + 15]
        )
        new_data["text_color"] = concat(
            self._data_source.data["text_color"], [RdYlBu3[self._iterator % 3]]
        )
        new_data["text"] = concat(self._data_source.data["text"], [str(self._iterator)])

        self._data_source.data = new_data
        self._iterator += 1
