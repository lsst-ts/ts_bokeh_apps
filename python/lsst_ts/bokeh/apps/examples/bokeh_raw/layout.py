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
from bokeh.colors import Color
from bokeh.core.property.override import Override
from bokeh.document import Document
from bokeh.model import Model
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import Button, CustomJS, Dropdown  # type: ignore

from lsst_ts.bokeh.apps.examples.bokeh_raw.data_aggregator import DataAggregator
from lsst_ts.bokeh.apps.examples.bokeh_raw.interaction import Interaction


class Layout:
    """
    """

    def __init__(self) -> None:
        self._data_aggregator = DataAggregator()
        self._interaction = Interaction(self._data_aggregator)

    def create(self, doc: Document) -> None:
        layout = self._create_layout()
        self._interaction.setup_interaction(layout)
        doc.add_root(layout)

    def _create_layout(self) -> Model:
        p = figure(border_fill_color= "black",
                   background_fill_color= "black",
                   outline_line_color= "blue",
                   toolbar_location=None,
                   x_range=(0, 100),
                   y_range=(0, 100))
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

        self._data_aggregator.data_sources['column_data_source'] = r.data_source

        # add a button widget and configure with the call back
        button = Button(label="Press Me")

        menu = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]

        dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)

        dropdown.js_on_event(
            "menu_item_click",
            CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"),
        )

        return column(children=[row(children=[dropdown, button]), p])
