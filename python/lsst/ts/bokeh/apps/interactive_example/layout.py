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

from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import Button, CustomJS, Dropdown

from lsst.ts.bokeh.apps.base_layout import BaseLayout
from lsst.ts.bokeh.apps.interactive_example.data_aggregator import DataAggregator


class Layout(BaseLayout):
    """"""

    def __init__(self) -> None:
        super().__init__(DataAggregator())

    def get_page(self):

        p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
        p.border_fill_color = "black"
        p.background_fill_color = "black"
        p.outline_line_color = None
        p.grid.grid_line_color = None

        r = p.text(
            x=[],
            y=[],
            text=[],
            text_color=[],
            text_font_size="26px",
            text_baseline="middle",
            text_align="center",
        )

        self.data_aggregator.data_sources["column_data_source"] = r.data_source

        # add a button widget and configure with the call back
        button = Button(label="Press Me")

        menu = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]

        dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)

        dropdown.js_on_event(
            "menu_item_click",
            CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"),
        )

        return column(row(dropdown, button), p)
