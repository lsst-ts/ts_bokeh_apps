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

from lsst.ts.bokeh.apps.base_interaction import BaseInteraction
from lsst.ts.bokeh.apps.interactive_example.layout import Layout


class Interaction(BaseInteraction):
    def __init__(self) -> None:
        super().__init__(Layout())
        self.log.debug("Starting Iteraction...")

    def setup_interaction(self):

        dropdown = self.page.children[0].children[0]
        button = self.page.children[0].children[1]

        dropdown.on_click(self.drop_down_callback)

        button.on_click(self.on_click_callback)

    def on_click_callback(self):
        self.layout.data_aggregator.retrieve_data()

    def drop_down_callback(self, event):
        self.layout.data_aggregator.retrieve_data()
