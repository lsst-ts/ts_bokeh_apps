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
from itertools import chain

import numpy
import asyncio
from bokeh.palettes import RdYlBu3
from bokeh.models import ColumnDataSource
from typing_extensions import override

from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive import interactive_example_layout
from lsst_ts.bokeh.utils.bokeh_framework.data_aggregator import DataAggregator

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy import ndarray, dtype
    from typing import Union, Sequence, Any, List, Optional, Dict
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout


def concat(a: 'Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]',
           b: 'Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]') -> 'List[Any]':
    return list(chain(a, b))


class InteractiveExampleDataAggregator(DataAggregator):
    """
    Data aggregator class for the app.
    """

    def __init__(self) -> None:
        super().__init__()
        self._iterator = 0
        self._data_source = ColumnDataSource() # type: ColumnDataSource

    @override
    def setup(self, layout: 'Layout') -> None:
        # force type layout also for typing purposes
        assert (isinstance(layout, interactive_example_layout.InteractiveExampleLayout))

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
                                [numpy.random.random() * 70 + 15])
        new_data["y"] = concat(self._data_source.data["y"],
                                [numpy.random.random() * 70 + 15])
        new_data["text_color"] = concat(self._data_source.data["text_color"],
                                         [RdYlBu3[self._iterator % 3]])
        new_data["text"] = concat(self._data_source.data["text"], [str(self._iterator)])

        self._data_source.data = new_data
        self._iterator += 1
        # logging.info("Waiting 1s before generating data...")
        # new_data = dict()  # type: Dict[str, Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]]
        # new_data["x"] = concat()
        # new_data["y"] = concat(self._data_source.data["y"], [numpy.random.random() * 70 + 15])
        # new_data["text_color"] = concat(self._data_source.data["text_color"],
        #                                          [RdYlBu3[self._iterator % 3]])
        # new_data["text"] = concat(self._data_source.data["text"], [str(self._iterator)])
        # self._data_source.data = new_data
        # self._iterator += 1


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
# from itertools import chain
#
# import numpy
# import asyncio
# from bokeh.palettes import RdYlBu3
#
# from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive import interactive_example_layout
# from lsst_ts.library.bokeh_framework_interactive.data_aggregation import DataAggregator
#
# from typing import TYPE_CHECKING, TypedDict
#
# if TYPE_CHECKING:
#     from bokeh.plotting import figure
#     from lsst_ts.library.bokeh_framework_interactive.layout import Layout
#     from typing import List, Optional
#
#
# class TextInformation(TypedDict):
#     x: list[float]
#     y: list[float]
#     text: list[str]
#     text_color: list[str]
#
# class InteractiveExampleDataAggregator(DataAggregator):
#     """
#     Data aggregator class for the app.
#     """
#
#     def __init__(self) -> None:
#         super().__init__()
#         self._iterator = 0
#         self._data_source = {'x': [], 'y': [], 'text':[], 'text_color': []} # type: TextInformation
#
#     def setup(self, layout: 'Layout') -> None:
#         # force type layout also for typing purposes
#         assert (isinstance(layout,
#                            interactive_example_layout.InteractiveExampleLayout))
#         self._plot = layout.plot
#
#     def retrieve_data(self) -> None:
#         """Retrieve data."""
#         asyncio.run(self._retrieve_data_async())
#
#     async def _retrieve_data_async(self) -> None:
#         """
#         Testing async methods in apps.
#         """
#         print("aaa")
#         self._data_source["x"].append(numpy.random.random() * 70 + 15)
#         self._data_source["y"].append(numpy.random.random() * 70 + 15)
#         self._data_source["text_color"].append(RdYlBu3[self._iterator % 3])
#         self._data_source["text"].append(str(self._iterator))
#         assert(self._plot is not None)
#         self._plot.text(
#             x=self._data_source['x'],
#             y=self._data_source['y'],
#             text=self._data_source['text_color'],
#             text_color=self._data_source['text'],
#             text_font_size="26px",
#             text_baseline="middle",
#             text_align="center",
#         )
#         # logging.info("Waiting 1s before generating data...")
#         # new_data = dict()  # type: Dict[str, Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]]
#         # new_data["x"] = concat()
#         # new_data["y"] = concat(self._data_source.data["y"], [numpy.random.random() * 70 + 15])
#         # new_data["text_color"] = concat(self._data_source.data["text_color"],
#         #                                          [RdYlBu3[self._iterator % 3]])
#         # new_data["text"] = concat(self._data_source.data["text"], [str(self._iterator)])
#         # self._data_source.data = new_data
#         # self._iterator += 1
