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

from bokeh.models import LogColorMapper, ColorBar, TextInput, PreText
from bokeh.plotting import figure
from bokeh.layouts import column, row

from lsst.ts.bokeh.apps.base_layout import BaseLayout
from lsst.ts.bokeh.apps.auxtel.image_explorer.data_aggregator import DataAggregator


class Layout(BaseLayout):
    """"""

    def __init__(self) -> None:
        super().__init__(DataAggregator())

    def get_page(self):

        p = figure(
            plot_width=1200,
            plot_height=1100,
            x_range=(0, 1),
            y_range=(0, 1),
            tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")],
        )
        color_mapper = LogColorMapper(palette="Viridis256", low=11000, high=21000)

        p.image(
            image="image",
            source=self.data_aggregator.data_sources["column_data_source"],
            color_mapper=color_mapper,
            dh="dh",
            dw="dw",
            x="x",
            y="y",
        )
        p.grid.grid_line_width = 0.5
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)

        p.add_layout(color_bar, "right")

        text_input = TextInput(
            value=f"{self.data_aggregator.day_obs}{self.data_aggregator.seq_num:05d}",
            title="Type exposure id and press enter:",
            max_length=15,
            width=250,
            height=50,
            sizing_mode="fixed",
        )

        status_text = PreText(text="", width=500, height=50, sizing_mode="fixed")

        return column(row(text_input, status_text), p)
