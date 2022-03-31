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

import panel as pn

from bokeh.models import LayoutDOM
from bokeh.models.widgets.tables import NumberFormatter

from ..base_layout import BaseLayout
from .data_aggregator import DataAggregator


class Layout(BaseLayout):
    """Layout for Observatory Log App."""

    def __init__(self) -> None:
        super().__init__(DataAggregator())

        self.select_dataset = pn.widgets.Select(
            name="Select Dataset", options=["LATISS", "LSSTComCam"]
        )
        self.select_data_id = pn.widgets.TextInput(
            name="Data id:", placeholder="YYYYMMDD, e.g. 20220317"
        )

        tabulator_formatters = {
            "exposure": NumberFormatter(format="0"),
        }

        self.tabulator = pn.widgets.Tabulator(
            self.df, layout="fit_data_fill", height=450, formatters=tabulator_formatters
        )
        self.tabulator.disabled = True
        self.tabulator.show_index = False
        self.tabulator.hidden_columns = [
            "id",
            "is_human",
            "is_valid",
            "instrument_x",
            "user_agent",
        ]

        self.follow = pn.widgets.Checkbox(name="Follow", value=True, align="end")

        self.cb = pn.state.add_periodic_callback(self.stream, 10000)
        self.text_table = pn.widgets.TextInput(
            name="Log:", placeholder="Enter a string here..."
        )

        self.exposure_flag_buttons = (
            "## Exposure flags: ",
            pn.widgets.Button(
                name="none",
                button_type="success",
                width=50,
                max_width=100,
                width_policy="fixed",
            ),
            pn.widgets.Button(
                name="questionable",
                button_type="warning",
                width=50,
                max_width=100,
                width_policy="fixed",
            ),
            pn.widgets.Button(
                name="junk",
                button_type="danger",
                width=50,
                max_width=100,
                width_policy="fixed",
            ),
            pn.widgets.Button(
                name="deselect",
                width=50,
                max_width=100,
                width_policy="fixed",
            ),
        )

        self.remove_log_entry_button = pn.widgets.Button(
            name="Remove", width=50, max_width=100, width_policy="fixed"
        )

        self.disable_buttons()

    def disable_buttons(self) -> None:
        self.exposure_flag_buttons[1].disabled = True
        self.exposure_flag_buttons[2].disabled = True
        self.exposure_flag_buttons[3].disabled = True
        self.exposure_flag_buttons[4].disabled = True
        self.remove_log_entry_button.disabled = True
        self.text_table.disabled = True

    def enable_buttons(self) -> None:
        self.exposure_flag_buttons[1].disabled = False
        self.exposure_flag_buttons[2].disabled = False
        self.exposure_flag_buttons[3].disabled = False
        self.exposure_flag_buttons[4].disabled = False
        self.remove_log_entry_button.disabled = False
        self.text_table.disabled = False

    def get_component(self):

        return pn.Column(
            pn.Row(*self.exposure_flag_buttons),
            self.tabulator,
            self.text_table,
        )

    def get_page(self) -> LayoutDOM:

        return self.get_component().get_root()
