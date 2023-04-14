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

import numpy
import asyncio

from bokeh.models import ColumnDataSource
from bokeh.palettes import RdYlBu3

from lsst_ts.bokeh.apps.base_data_aggregator import BaseDataAggregator


class DataAggregator:
    """Data aggregator class for the app."""

    def __init__(self):
        self._data_sources = {}
        self._iterator = 0
        self._initialize_data_sources()

    def _initialize_data_sources(self, *args, **kwargs):
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
    def data_sources(self):
        return self._data_sources

    async def _retrieve_data_async(self):
        """
        Testing async methods in apps.
        """
        new_data = dict()
        new_data["x"] = self._data_sources["column_data_source"].data["x"] + [numpy.random.random() * 70 + 15]
        new_data["y"] = self._data_sources["column_data_source"].data["y"] + [numpy.random.random() * 70 + 15]
        new_data["text_color"] = self._data_sources["column_data_source"].data["text_color"] + [RdYlBu3[self._iterator % 3]]
        new_data["text"] = self._data_sources["column_data_source"].data["text"] + [str(self._iterator)]
        self._data_sources["column_data_source"].data = new_data
        self._iterator += 1

        print("Data generated...")

    def retrieve_data(self, *args, **kwargs):
        """Retrive data."""
        asyncio.run(self._retrieve_data_async())
