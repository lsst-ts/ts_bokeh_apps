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

# CPIO Example comment:  Installed and python default selected component imports. Alphabetical order
from bokeh.layouts import gridplot
from bokeh.models import Span, TextInput, Column, LayoutDOM, Row, Paragraph
from bokeh.plotting import figure
from typing import Optional
from typing_extensions import override

# CPIO Example comment: Own library imports. Alphabetical order
from lsst_ts.bokeh.apps.examples.bokeh_framework_efd.efd_example_data_aggregator import \
    EfdExampleDataAggregator
from lsst_ts.bokeh.apps.examples.bokeh_framework_efd.efd_example_interaction import EfdExampleInteraction
from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout
from lsst_ts.bokeh.utils.bokeh_framework.utils import CustomWidgets

# CPIO Example comment: Type checking imports (optional). Alphabetical order
from typing import TYPE_CHECKING

# CPIO Example comment: If Variables are only for type checking they may be declared inside this conditional
# but is optional to have it inside
if TYPE_CHECKING:
    from bokeh.models import ColumnDataSource


# CPIO Example comment: Auxiliar classes for plot creation
class Plot:
    _WIDTH = 400
    _HEIGHT = 400
    _ALIGN = "center"
    _X_AXIS_TYPE = "datetime"

    def __init__(self, saved_figure: figure):
        self._figure = saved_figure  # typing: figure

    def add_line(self, data_source: 'ColumnDataSource', x_data: str, y_data: str, l_color: str = 'black',
                 legend: str = ""):
        """
        Adds a line into the figure plot
        :param data_source: Column data source
        :param x_data: string with the id of the x data
        :param y_data:  string with the id of the y data
        :param l_color: line color
        :param legend: string with a legend for the line
        :return:
        """
        assert (self._figure is not None)
        self._figure.line(x=x_data,
                          y=y_data,
                          line_color=l_color,
                          line_width=2,
                          source=data_source,
                          legend_label=legend,
                          )

    def add_span(self, start):
        """
        Add a span into the figure plot #Maybe can be improved being able to set properties of the span
        :param start:
        :return:
        """
        obs_start = Span(location=start,
                         dimension="height",
                         line_color="red",
                         line_dash="dashed",
                         line_width=3,
                         )
        self._figure.add_layout(obs_start)

    @staticmethod
    def create(title: str, x_axis_label: str = "", y_axis_label: str = "") -> 'Plot':
        """
        Create the figure plot and returns the instance
        :param title: Title of the figure
        :param x_axis_label: x_label value
        :param y_axis_label: y_label_value
        :return:
        """
        _figure = figure(plot_width=Plot._WIDTH,
                         plot_height=Plot._HEIGHT,
                         background_fill_color="#EFEFEF",
                         x_axis_type=Plot._X_AXIS_TYPE)
        _figure.title.text = title
        _figure.title.align = Plot._ALIGN
        _figure.xaxis.axis_label = x_axis_label
        _figure.yaxis.axis_label = y_axis_label
        return Plot(_figure)

    def synchronize_x_range(self, plot: 'Plot'):
        """
        :param plot:
        :return:
        """
        sync_figure = plot.figure
        assert (sync_figure is not None)
        assert (self._figure is not None)
        self._figure.x_range = sync_figure.x_range

    def synchronize_y_range(self, plot: 'Plot'):
        """
        :param plot:
        :return:
        """
        sync_figure = plot.figure
        assert (sync_figure is not None)
        assert (self._figure is not None)
        self._figure.y_range = sync_figure.y_range

    @property
    def figure(self) -> Optional['figure']:
        return self._figure


# CPIO Example comment: child class that inherits from Layout, has the responsibility of creating
# the application Layout (the view with all its components)
class EfdExampleLayout(Layout):
    _WIDTH = 400
    _HEIGHT = 400

    def __init__(self):
        super().__init__(data_aggregator=EfdExampleDataAggregator(), interaction=EfdExampleInteraction())
        self._torque_start = 0  # typing: int
        self._mount_start = 0  # typing: int
        self._efd_data_aggregator = None  # Optional[EfdExampleDataAggregator]
        self._s1 = None # typing: Optional[Plot]
        self._s2 = None # typing: Optional[Plot]
        self._s3 = None # typing: Optional[Plot]
        self._s4 = None # typing: Optional[Plot]
        self._s5 = None # typing: Optional[Plot]
        self._s6 = None # typing: Optional[Plot]
        self._s7 = None # typing: Optional[Plot]
        self._s8 = None # typing: Optional[Plot]
        self._s9 = None # typing: Optional[Plot]
        self._text_input = None # typing: Optional[TextInput]


    # CPIO Example comment: A decorator is used in order to advise that the method is override  from the
    # base call. Override decorator really doesn't affect the method execution
    @override
    # CPIO Example comment: Method overriden to create the layout of the application,
    # Should always return a LayoutDOM, so better puts all component inside a Layout (Row, Column, Grid...)
    # (check UIElement when upgrading to bokeh 3.0.x)
    def define(self) -> LayoutDOM:
        self._efd_data_aggregator = self.data_aggregator
        assert (isinstance(self._efd_data_aggregator, EfdExampleDataAggregator))
        self._mount_start = self._efd_data_aggregator.data_sources.data["mount_x"][0]
        self._torque_start = self._efd_data_aggregator.data_sources.data["torque_x"][0]

        self._s1 = self._create_s1()
        self._s2 = self._create_s2()
        self._s3 = self._create_s3()
        self._s4 = self._create_s4()
        self._s5 = self._create_s5()
        self._s6 = self._create_s6()
        self._s7 = self._create_s7()
        self._s8 = self._create_s8()
        self._s9 = self._create_s9()

        error_message = CustomWidgets.create_exception_viewer()
        label = Paragraph(text="Type exposure id and press enter (e.g. 2021081700541):")
        self._text_input = TextInput(
            value="",
            max_length=15,
            sizing_mode="fixed",
        )
        header_utils = Column(children=[label, Row(children=[self._text_input, error_message])])

        plot_grid = gridplot(children=[[self._s1.figure, self._s2.figure, self._s3.figure],
                                       [self._s4.figure, self._s5.figure, self._s6.figure],
                                       [self._s7.figure, self._s8.figure, self._s9.figure]])

        return Column(children=[header_utils, plot_grid])

    # CPIO Example comment: According to general OOP programming concepts, attributes should be private
    # and be accessible using a getter. In python concretely all attributes are declared a 'private' beginning
    # with "_" and use @property decorator to create the getter to access the attribute
    @property
    def text_input(self) -> Optional[TextInput]:
        return self._text_input

    # CPIO Example comment: Plot instantiation
    def _create_s1(self):
        s1 = Plot.create("Azimuth axis", y_axis_label="Degrees")
        s1.add_line(self._efd_data_aggregator.data_sources, "mount_x", "mount_azimuth_calculate_angle",
                    l_color="red")
        s1.add_span(start=self._mount_start)
        return s1

    def _create_s2(self):
        s2 = Plot.create("Elevation axis")
        s2.add_line(self._efd_data_aggregator.data_sources, "mount_x", "mount_elevation_calculated_angle",
                    l_color="green")
        s2.add_span(start=self._mount_start)
        s2.synchronize_x_range(self._s1)
        return s2

    def _create_s3(self):
        s3 = Plot.create("Nasmyth2 axis")
        s3.add_line(self._efd_data_aggregator.data_sources, "mount_x", "mount_nasmyth2_calculated_angle",
                    l_color="blue")
        s3.add_span(start=self._mount_start)
        s3.synchronize_x_range(self._s1)
        return s3

    def _create_s4(self):
        s4 = Plot.create("Azimuth RMS error", y_axis_label="Arcseconds")
        s4.add_line(self._efd_data_aggregator.data_sources, "mount_x", "mount_az_err", l_color="red")
        s4.synchronize_x_range(self._s1)
        return s4

    def _create_s5(self):
        s5 = Plot.create("Elevation RMS error")
        s5.add_line(self._efd_data_aggregator.data_sources, "mount_x", "mount_el_err", l_color="green")
        s5.synchronize_x_range(self._s1)
        s5.synchronize_y_range(self._s4)
        return s5

    def _create_s6(self):
        s6 = Plot.create("Nasmyth RMS error")
        s6.add_line(self._efd_data_aggregator.data_sources, "rotator_x", "rotator_error", l_color="blue")
        s6.synchronize_x_range(self._s1)
        s6.synchronize_y_range(self._s4)
        return s6

    def _create_s7(self):
        s7 = Plot.create("Nasmyth RMS error", x_axis_label="Elapsed Time",
                         y_axis_label="Torque (motor current in amps)")
        s7.add_line(self._efd_data_aggregator.data_sources, "torque_x", "torques_azimuth_motor1_torque",
                    l_color="blue")
        s7.add_line(self._efd_data_aggregator.data_sources, "torque_x", "torques_azimuth_motor2_torque",
                    l_color="green")
        s7.add_span(self._torque_start)
        s7.synchronize_x_range(self._s1)
        return s7

    def _create_s8(self):
        s8 = Plot.create("", x_axis_label="Elapsed Time")
        s8.add_line(self._efd_data_aggregator.data_sources, "torque_x", "torques_elevation_motor_torque",
                    l_color="blue",
                    legend="elevationMotorTorque")
        s8.add_span(self._torque_start)
        s8.synchronize_x_range(self._s1)
        return s8

    def _create_s9(self):
        s9 = Plot.create("", x_axis_label="Elapsed Time")
        s9.add_line(self._efd_data_aggregator.data_sources, "torque_x", "torques_nasmyth2_motor_torque",
                    l_color="blue",
                    legend="nasmyth2MotorTorque")
        s9.add_span(self._torque_start)
        s9.synchronize_x_range(self._s1)
        return s9
