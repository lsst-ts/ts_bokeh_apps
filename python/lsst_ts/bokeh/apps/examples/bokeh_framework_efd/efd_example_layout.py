from bokeh.layouts import gridplot
from bokeh.models import Span, TextInput
from bokeh.plotting import figure

from lsst_ts.bokeh.apps.examples.bokeh_framework_efd.efd_example_data_aggregator import \
    EfdExampleDataAggregator
from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout


class EfdExampleLayout(Layout):

    def __init__(self):
        super().__init__(data_aggregator=EfdExampleDataAggregator())

    def define(self) -> 'LayoutDOM':
        mount_start = self.data_aggregator.data_sources["column_data_source"].data["mount_x"][0]
        torque_start = self.data_aggregator.data_sources["column_data_source"].data["torque_x"][0]
        s1 = self._make_plot(
            "Azimuth axis",
            "mount_x",
            "mount_azimuth_calculate_angle",
            lcolors="red",
            start=mount_start,
        )
        s2 = self._make_plot(
            "Elevation axis",
            "mount_x",
            "mount_elevation_calculated_angle",
            lcolors="green",
            start=mount_start,
        )
        s3 = self._make_plot(
            "Nasmyth2 axis",
            "mount_x",
            "mount_nasmyth2_calculated_angle",
            lcolors="blue",
            start=mount_start,
        )
        s4 = self._make_plot(
            "Azimuth RMS error",
            "mount_x",
            "mount_az_err",
            lcolors="red",
        )
        s5 = self._make_plot(
            "Elevation RMS error",
            "mount_x",
            "mount_el_err",
            lcolors="green",
        )
        s6 = self._make_plot(
            "Nasmyth RMS error",
            "rotator_x",
            "rotator_error",
            lcolors="blue",
        )
        s7 = self._make_plot(
            "",
            ["torque_x", "torque_x"],
            ["torques_azimuth_motor1_torque", "torques_azimuth_motor2_torque"],
            lcolors=["blue", "green"],
            legend=["azimuthMotor1Torque", "azimuthMotor2Torque"],
            start=torque_start,
        )
        s8 = self._make_plot(
            "",
            "torque_x",
            "torques_elevation_motor_torque",
            lcolors="blue",
            legend="elevationMotorTorque",
            start=torque_start,
        )
        s9 = self._make_plot(
            "",
            "torque_x",
            "torques_nasmyth2_motor_torque",
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

        self.grid = gridplot([[s1, s2, s3], [s4, s5, s6], [s7, s8, s9]])

        self.text_input = TextInput(
            value="",
            title="Type exposure id and press enter (e.g. 2021081700541):",
            max_length=15,
            sizing_mode="fixed",
        )

    def _make_plot(self, title, xnames, ynames, lcolors=None, legend=None, start=None):
        if type(xnames) is str and type(ynames) is str:
            xnames = [xnames, ]
            ynames = [ynames, ]
        if type(lcolors) is str:
            lcolors = [lcolors, ]
        if type(legend) is str:
            legend = [legend, ]
        if lcolors is None:
            lcolors = ["black" for el in xnames]
        plot = figure(plot_width=400,
                      plot_height=400,
                      background_fill_color="#efefef",
                      x_axis_type="datetime")
        plot.title.text = title
        plot.title.align = "center"
        for i, t in enumerate(zip(xnames, ynames, lcolors)):
            x, y, c = t
            if legend:
                plot.line(x=x,
                          y=y,
                          line_color=c,
                          line_width=2,
                          source=self.data_aggregator.data_sources["column_data_source"],
                          legend_label=legend[i],
                          )
            else:
                plot.line(x=x,
                          y=y,
                          line_color=c,
                          line_width=2,
                          source=self.data_aggregator.data_sources["column_data_source"],
                          )
        if start:
            obs_start = Span(location=start,
                             dimension="height",
                             line_color="red",
                             line_dash="dashed",
                             line_width=3,
                             )
            plot.add_layout(obs_start)
        return plot
