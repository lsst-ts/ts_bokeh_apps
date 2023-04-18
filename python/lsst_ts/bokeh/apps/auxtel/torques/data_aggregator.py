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
import asyncio

import lsst.daf.butler as dafButler
from lsst_efd_client import EfdClient
from bokeh.models import ColumnDataSource

from lsst_ts.bokeh.apps.base_data_aggregator import BaseDataAggregator


class DataAggregator(BaseDataAggregator):
    """Data aggregator class for the torque bokeh app."""

    def __init__(self) -> None:
        super().__init__()

        self.day_obs = 20210817
        self.seq_num = 541

    def create_data_sources(self):
        self.butler = dafButler.Butler(
            "LATISS", instrument="LATISS", collections="LATISS/raw/all"
        )
        self.efd = EfdClient("usdf_efd")

    def initialize_data_sources(self, *args, **kwargs):
        """Initialize data sources."""

        self.create_data_sources()

        self.data_sources["column_data_source"] = ColumnDataSource(
            data=dict(
                mount_x=[0.0],
                mount_azimuth_calculate_angle=[0.0],
                mount_elevation_calculated_angle=[0.0],
                mount_azimuth_fit=[0.0],
                mount_elevation_fit=[0.0],
                mount_nasmyth2_calculated_angle=[0.0],
                mount_az_err=[0.0],
                mount_el_err=[0.0],
                torque_x=[0.0],
                torques_azimuth_motor1_torque=[0.0],
                torques_azimuth_motor2_torque=[0.0],
                torques_elevation_motor_torque=[0.0],
                torques_nasmyth2_motor_torque=[0.0],
                rotator_x=[0.0],
                rotator_error=[0.0],
                rotator_fit=[0.0],
            )
        )

    def retrieve_data(self, *args, **kwargs):
        asyncio.run(self._retrieve_data_async())

    async def _retrieve_data_async(self):
        """
        :return:
        """

        t = [
            r
            for r in self.butler.registry.queryDimensionRecords(
                "exposure",
                where=f"exposure.day_obs = {self.day_obs} and exposure.seq_num = {self.seq_num}",
            )
        ]
        if len(t) > 1:
            raise RuntimeError(
                f"Something went wrong. We only expected one record for {self.day_obs}-{self.seq_num}"
            )
        md = t[0]

        mountpos = await self.efd.select_packed_time_series(
            "lsst.sal.ATMCS.mount_AzEl_Encoders",
            ["azimuthCalculatedAngle", "elevationCalculatedAngle"],
            md.timespan.begin.utc,
            md.timespan.end.utc,
        )
        rot = await self.efd.select_packed_time_series(
            "lsst.sal.ATMCS.mount_Nasmyth_Encoders",
            [
                "nasmyth2CalculatedAngle",
            ],
            md.timespan.begin.utc,
            md.timespan.end.utc,
        )
        torques = await self.efd.select_packed_time_series(
            "lsst.sal.ATMCS.measuredTorque",
            [
                "azimuthMotor1Torque",
                "azimuthMotor2Torque",
                "elevationMotorTorque",
                "nasmyth2MotorTorque",
            ],
            md.timespan.begin.utc,
            md.timespan.end.utc,
        )

        afit = numpy.polyfit(mountpos.times, mountpos["azimuthCalculatedAngle"], 1)
        efit = numpy.polyfit(mountpos.times, mountpos["elevationCalculatedAngle"], 1)
        rfit = numpy.polyfit(rot.times, rot["nasmyth2CalculatedAngle"], 1)

        mountpos["amodel"] = afit[0] * mountpos.times + afit[1]
        mountpos["emodel"] = efit[0] * mountpos.times + efit[1]
        rot["rmodel"] = rfit[0] * rot.times + rfit[1]

        mountpos["az_err"] = (
            mountpos["azimuthCalculatedAngle"] - mountpos["amodel"]
        ) * 3600
        mountpos["el_err"] = (
            mountpos["elevationCalculatedAngle"] - mountpos["emodel"]
        ) * 3600
        rot["rot_err"] = (rot["nasmyth2CalculatedAngle"] - rot["rmodel"]) * 3600

        self.data_sources["column_data_source"].data = dict(
            mount_x=mountpos.index,
            mount_azimuth_calculate_angle=mountpos["azimuthCalculatedAngle"],
            mount_elevation_calculated_angle=mountpos["elevationCalculatedAngle"],
            mount_azimuth_fit=mountpos["amodel"],
            mount_elevation_fit=mountpos["emodel"],
            mount_nasmyth2_calculated_angle=rot["rmodel"],
            mount_az_err=mountpos["az_err"],
            mount_el_err=mountpos["el_err"],
            torque_x=torques.index,
            torques_azimuth_motor1_torque=torques["azimuthMotor1Torque"],
            torques_azimuth_motor2_torque=torques["azimuthMotor2Torque"],
            torques_elevation_motor_torque=torques["elevationMotorTorque"],
            torques_nasmyth2_motor_torque=torques["nasmyth2MotorTorque"],
            rotator_x=rot.index,
            rotator_error=rot["rot_err"],
            rotator_fit=rot["rmodel"],
        )