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

from bokeh.models import Span, Div
from bokeh.plotting import figure
from bokeh.layouts import column, gridplot

from ..base_layout import BaseLayout
from .data_aggregator import DataAggregator


class Layout(BaseLayout):
    """"""

    def __init__(self) -> None:
        super().__init__(DataAggregator())

    def get_layout(self):
        mount_start = self.data_aggregator.data_sources["column_data_source"].data[
            "mount_x"
        ][0]
        torque_start = self.data_aggregator.data_sources["column_data_source"].data[
            "torque_x"
        ][0]
        rotator_start = self.data_aggregator.data_sources["column_data_source"].data[
            "rotator_x"
        ][0]

        s1 = self.make_plot(
            "Azimuth axis",
            "x1",
            "y1",
            lcolors="red",
            start=mount_start,
        )
        s2 = self.make_plot(
            "Elevation axis", "x2", "y2", lcolors="green", start=mount_start
        )
        s3 = self.make_plot(
            "Nasmyth2 axis", "x3", "y3", lcolors="blue", start=mount_start
        )
        s4 = self.make_plot(
            f"Azimuth RMS error",
            "x4",
            "y4",
            lcolors="red",
        )
        s5 = self.make_plot(
            f"Elevation RMS error",
            "x5",
            "y5",
            lcolors="green",
        )
        s6 = self.make_plot(
            f"Nasmyth RMS error",
            "x6",
            "y6",
            lcolors="blue",
        )
        s7 = self.make_plot(
            "",
            ["x7", "x7"],
            ["y7a", "y7b"],
            lcolors=["blue", "green"],
            legend=["azimuthMotor1Torque", "azimuthMotor2Torque"],
            start=torque_start,
        )
        s8 = self.make_plot(
            "",
            "x8",
            "y8",
            lcolors="blue",
            legend="elevationMotorTorque",
            start=torque_start,
        )
        s9 = self.make_plot(
            "",
            "x9",
            "y9",
            lcolors="blue",
            legend="nasmyth2MotorTorque",
            start=torque_start,
        )
        s2.x_range = s1.x_range
        s3.x_range = s1.x_range
        s4.x_range = s1.x_range
        s5.x_range = s1.x_range
        s6.x_range = s1.x_range
        s7.x_range = s1.x_range
        s8.x_range = s1.x_range
        s9.x_range = s1.x_range

        s4.y_range = s6.y_range
        s5.y_range = s6.y_range

        s1.yaxis.axis_label = "Degrees"
        s4.yaxis.axis_label = "Arcseconds"
        s7.yaxis.axis_label = "Torque (motor current in amps)"

        s7.xaxis.axis_label = "Elapsed Time"
        s8.xaxis.axis_label = "Elapsed Time"
        s9.xaxis.axis_label = "Elapsed Time"

        grid = gridplot([[s1, s2, s3], [s4, s5, s6], [s7, s8, s9]])

        title = Div(
            text=f"<h1>Mount Tracking: "
            f"Azimuth = {'Placeholder Az'}, Elevation = {'Placeholder El'}</h1>",
            align="center",
        )

        return column(title, grid)

    def _make_plot(self, title, xnames, ynames, lcolors=None, legend=None, start=None):
        if type(xnames) is str and type(ynames) is str:
            xnames = [
                xnames,
            ]
            ynames = [
                ynames,
            ]
        if type(lcolors) is str:
            lcolors = [
                lcolors,
            ]
        if type(legend) is str:
            legend = [
                legend,
            ]
        if lcolors is None:
            lcolors = ["black" for el in xnames]
        plot = figure(
            plot_width=400,
            plot_height=400,
            background_fill_color="#efefef",
            x_axis_type="datetime",
        )
        plot.title.text = title
        plot.title.align = "center"
        for i, t in enumerate(zip(xnames, ynames, lcolors)):
            x, y, c = t
            if legend:
                line = plot.line(
                    x=x,
                    y=y,
                    line_color=c,
                    line_width=2,
                    source=self.data_aggregator.data_sources["column_data_source"],
                    legend_label=legend[i],
                )
            else:
                line = plot.line(
                    x=x,
                    y=y,
                    line_color=c,
                    line_width=2,
                    source=self.data_aggregator.data_sources["column_data_source"],
                )
        if start:
            obs_start = Span(
                location=start,
                dimension="height",
                line_color="red",
                line_dash="dashed",
                line_width=3,
            )
            plot.add_layout(obs_start)
        return plot
