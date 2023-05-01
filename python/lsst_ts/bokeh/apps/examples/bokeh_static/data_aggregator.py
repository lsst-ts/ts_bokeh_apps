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
from typing import Dict, Union, Sequence, List, Any

import numpy
import asyncio

from bokeh.models import ColumnDataSource
from bokeh.palettes import RdYlBu3
from numpy import ndarray, dtype


def concat(a: Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any],
           b: Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]) -> List[Any]:
    return list(chain(a, b))


class DataAggregator:
    """Data aggregator class for the app."""

    def __init__(self) -> None:
        self._data_sources = {}  # type: Dict[str, ColumnDataSource]
        self._iterator = 0  # type: int
        self._initialize_data_sources()

    def _initialize_data_sources(self) -> None:
        """Initialize data sources."""

        self._data_sources["column_data_source"] = ColumnDataSource(
            data=dict(
                x=[],
                y=[],
                text=[],
                text_color=[],
            )
        )

    @property
    def data_sources(self) -> Dict[str, ColumnDataSource]:
        return self._data_sources

    async def _retrieve_data_async(self) -> None:
        """
        Testing async methods in apps.
        """
        new_data = dict()  # type: Dict[str, Union[Sequence[Any], ndarray[Any, dtype[Any]], Any, Any]]
        new_data["x"] = concat(self._data_sources["column_data_source"].data["x"],
                               [numpy.random.random() * 70 + 15])
        new_data["y"] = concat(self._data_sources["column_data_source"].data["y"],
                               [numpy.random.random() * 70 + 15])
        new_data["text_color"] = concat(self._data_sources["column_data_source"].data["text_color"],
                                        [RdYlBu3[self._iterator % 3]])
        new_data["text"] = concat(self._data_sources["column_data_source"].data["text"],
                                  [str(self._iterator)])
        self._data_sources["column_data_source"].data = new_data

        self._iterator += 1

        print("Data generated....")

    def retrieve_data(self) -> None:
        """Retrive data."""
        asyncio.run(self._retrieve_data_async())
