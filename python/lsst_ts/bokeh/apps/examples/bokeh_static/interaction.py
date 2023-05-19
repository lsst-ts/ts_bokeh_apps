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

from bokeh.events import Event
from bokeh.model import Model

if TYPE_CHECKING:
    from lsst_ts.bokeh.apps.base_data_aggregator import BaseDataAggregator


class Interaction:
    def __init__(self, data_aggregator: BaseDataAggregator) -> None:
        self._data_aggregator = data_aggregator

    def setup_interaction(self, layout: Model) -> None:
        dropdown = layout.children[0].children[0]
        button = layout.children[0].children[1]

        dropdown.on_click(self.drop_down_callback)
        button.on_click(self.on_click_callback)

    def on_click_callback(self) -> None:
        self._data_aggregator.retrieve_data()

    def drop_down_callback(self, event: Event) -> None:
        self._data_aggregator.retrieve_data()
