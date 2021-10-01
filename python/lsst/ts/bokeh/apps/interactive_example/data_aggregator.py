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

from bokeh.models import ColumnDataSource
from bokeh.palettes import RdYlBu3

from lsst.ts.bokeh.apps.base_data_aggregator import BaseDataAggregator


class DataAggregator(BaseDataAggregator):
    """Data aggregator class for the app."""

    def __init__(self) -> None:
        super().__init__()

    def initialize_data_sources(self, *args, **kwargs):
        """Initialize data sources."""

        self.iterator = 0

        self.data_sources["column_data_source"] = ColumnDataSource(
            data=dict(
                x=[],
                y=[],
                text=[],
                text_color=[],
            )
        )

    def retrieve_data(self, *args, **kwargs):
        """"""
        new_data = dict()
        new_data["x"] = self.data_sources["column_data_source"].data["x"] + [
            numpy.random.random() * 70 + 15
        ]
        new_data["y"] = self.data_sources["column_data_source"].data["y"] + [
            numpy.random.random() * 70 + 15
        ]
        new_data["text_color"] = self.data_sources["column_data_source"].data[
            "text_color"
        ] + [RdYlBu3[self.iterator % 3]]
        new_data["text"] = self.data_sources["column_data_source"].data["text"] + [
            str(self.iterator)
        ]
        self.data_sources["column_data_source"].data = new_data

        self.iterator += 1
