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

from bokeh.models import ColumnDataSource

from ..base_data_aggregator import BaseDataAggregator


class DataAggregator(BaseDataAggregator):
    """Data aggregato class for the torque bokeh app."""

    def __init__(self) -> None:
        super().__init__()

    def initialize_data_sources(self, *args, **kwargs):
        """Initialize data sources."""

        self.data_sources["column_data_source"] = ColumnDataSource(
            data=dict(
                mount_x=[],
                mount_azimuth_calculate_angle=[],
                mount_elevation_calculated_angle=[],
                mount_azimuth_fit=[],
                mount_elevation_fit=[],
                mount_nasmyth2_calculated_angle=[],
                mount_az_err=[],
                mount_el_err=[],
                torque_x=[],
                torques_azimuth_motor1_torque=[],
                torques_azimuth_motor2_torque=[],
                torques_elevation_motor_torque=[],
                torques_nasmyth2_motor_torque=[],
                rotator_x=[],
                rotator_error=[],
                rotator_fit=[],
            )
        )
