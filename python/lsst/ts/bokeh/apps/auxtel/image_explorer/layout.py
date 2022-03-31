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

from bokeh.models import (
    LogColorMapper,
    ColorBar,
    TextInput,
    PreText,
    Dropdown,
    RangeSlider,
    CustomJS,
)
from bokeh.plotting import figure
from bokeh.layouts import column, row

from ..base_layout import BaseLayout
from .data_aggregator import DataAggregator


class Layout(BaseLayout):
    """Layout for the image explorer app."""

    def __init__(self) -> None:
        super().__init__(DataAggregator())

    def _get_color_mapper(self, palette="Viridis256"):
        return LogColorMapper(
            palette=palette,
            low=self.image_low,
            high=self.image_high,
        )

    def get_page(self):

        self.image_low = 1000
        self.image_high = 21000

        p = figure(
            plot_width=1200,
            plot_height=1100,
            x_range=(0, 1),
            y_range=(0, 1),
            tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")],
        )
        color_mapper = self._get_color_mapper("Viridis256")

        self.image = p.image(
            image="image",
            source=self.data_aggregator.data_sources["column_data_source"],
            color_mapper=color_mapper,
            dh="dh",
            dw="dw",
            x="x",
            y="y",
        )
        p.grid.grid_line_width = 0.5
        self.color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)

        p.add_layout(self.color_bar, "right")

        text_input = TextInput(
            value=f"{self.data_aggregator.day_obs}{self.data_aggregator.seq_num:05d}",
            title="Type exposure id and press enter:",
            max_length=15,
            width=250,
            height=50,
            sizing_mode="fixed",
        )

        status_text = PreText(text="", width=500, height=50, sizing_mode="fixed")

        menu = [
            ("Viridis256", "Viridis256"),
            ("Greys", "Greys9"),
            ("Oranges", "Oranges9"),
        ]

        dropdown = Dropdown(label="Color Map", button_type="success", menu=menu)

        dropdown.js_on_event(
            "menu_item_click",
            CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"),
        )

        range_slider = RangeSlider(
            start=self.image_low,
            end=self.image_high,
            value=(self.image_low, self.image_high),
            step=1000,
            title="Image Scale",
        )
        range_slider.js_on_change(
            "value",
            CustomJS(
                code="""
            console.log('range_slider: value=' + this.value, this.toString())
        """
            ),
        )
        return column(row(text_input, status_text, dropdown), p, range_slider)
