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

from lsst.ts.bokeh.apps.base_interaction import BaseInteraction
from lsst.ts.bokeh.apps.auxtel.torques.layout import Layout


class Interaction(BaseInteraction):
    def __init__(self) -> None:
        super().__init__(Layout())

    def handle_text_input(self, attr, old, new):
        self.layout.data_aggregator.day_obs = int(new[:8])
        self.layout.data_aggregator.seq_num = int(new[8:])

        try:
            self.log.debug(f"Processing: {new}.")
            self.layout.data_aggregator.retrieve_data()
        except Exception:
            self.log.exception(f"Error retrieving data for {new}.")

    def setup_interaction(self):

        text_input = self.page.children[0]
        text_input.on_change("value", self.handle_text_input)
