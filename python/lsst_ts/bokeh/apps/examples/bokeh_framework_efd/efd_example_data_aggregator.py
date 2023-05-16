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

# CPIO Example comment: Installed and python default imports. Alphabetical order
import asyncio
import logging

# CPIO Example comment:  Installed and python default selected component imports. Alphabetical order
import lsst.daf.butler as daf_butler
import numpy as np
from bokeh.models import ColumnDataSource
from lsst.daf.butler import DimensionRecord
from lsst_efd_client import EfdClient
from typing_extensions import override

# CPIO Example comment: Own library imports. Alphabetical order
from lsst_ts.bokeh.apps.examples.bokeh_framework_efd import efd_example_layout
from lsst_ts.bokeh.utils.bokeh_framework.data_aggregator import DataAggregator
from lsst_ts.library.utils.logger import get_logger

# CPIO Example comment: Type checking imports (optional). Alphabetical order
from typing import TYPE_CHECKING

# CPIO Example comment: If Variables are only for type checking they may be declared inside this conditional
# but is optional to have it inside
if TYPE_CHECKING:
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

__all__ = ['EfdExampleDataAggregator']


# CPIO Example comment: User this function get_logger in order to obtain a valid logger that will be integrated
# inside the application

_log = get_logger("examples.efd.data_aggregator")

# # CPIO Example comment: Auxiliar classes to hardcode information, maybe can be inside a configuration file
class ButlerData:
    configuration: str = "LATISS"
    instrument: str = "LATISS"
    collections: str = "LATISS/raw/all"

class EdfData:
    client: str = "usdf_efd"

# CPIO Example comment: child class that inherits from DataAggregator. has the responsibility of creating and
# interacting with plotting data
class EfdExampleDataAggregator(DataAggregator):

    def __init__(self):
        super().__init__()
        self._data_sources = None  # typing: Optional[ColumnDataSource]

    # CPIO Example comment: A decorator is used in order to advise that the method is override  from the
    # base call. Override decorator really doesn't affect the method execution
    @override
    # CPIO Example comment: Method overriden from DataAggregator to set up the plotting data.
    # It may be empty.
    def setup(self, layout: 'Layout') -> None:
        """
        :param layout: Layout instance
        :return: None
        """
        # force type layout also for typing purposes
        # To avoid circular import full module must be imported
        assert (isinstance(layout, efd_example_layout.EfdExampleLayout))
        self._create_data_sources()
        self._initialize_data_sources()

    # CPIO Example comment: Function to update data sources
    def update_observation_information(self, new_observation_day: int, new_sequence_number: int) -> None:
        """
        :param new_observation_day:
        :param new_sequence_number:
        :return:
        """
        asyncio.run(self._retrieve_data_async(new_observation_day, new_sequence_number))

    # CPIO Example comment: According to general OOP programming concepts, attributes should be private
    # and be accessible using a getter. In python concretely all attributes are declared a 'private' beginning
    # with "_" and use @property decorator to create the getter to access the attribute
    # This getter will be used in interaction in order to create interaction
    @property
    def data_sources(self) -> ColumnDataSource:
        """
        :return:
        """
        assert (self._data_sources is not None)
        return self._data_sources

    def _create_data_sources(self) ->  None:
        """
        :return:
        """
        _log.info("Creating data sources.")
        self.butler = daf_butler.Butler(ButlerData.configuration,
                                        instrument=ButlerData.instrument,
                                        collections=ButlerData.collections)
        self.efd = EfdClient(EdfData.client)

    def _initialize_data_sources(self) -> None:
        """
        Initialize data sources.
        """
        _log.info("Initializing data sources.")
        self._data_sources = ColumnDataSource(
            data=dict(
                mount_x=[0.0],
                mount_azimuth_calculate_angle=[0.0],
                mount_elevation_calculated_angle=[0.0],
                mount_azimuth_fit=[0.0],
                mount_elevation_fit=[0.0],
                mount_nasmyth2_calculated_angle=[0.0],
                mount_az_err=[0.0],
                mount_el_err=[0.0],
                rotator_x=[0.0],
                rotator_error=[0.0],
                rotator_fit=[0.0],
                torque_x=[0.0],
                torques_azimuth_motor1_torque=[0.0],
                torques_azimuth_motor2_torque=[0.0],
                torques_elevation_motor_torque=[0.0],
                torques_nasmyth2_motor_torque=[0.0]
            )
        )
    def _query_observation_data(self, observation_day, sequence_number) -> DimensionRecord:
        """
        :return:
        """
        query_condition = f"exposure.day_obs = {observation_day} and exposure.seq_num = {sequence_number}"
        values = list(self.butler.registry.queryDimensionRecords("exposure", where=query_condition))
        assert len(
            values) <= 1, f"Something went wrong. We only expected one record for observation day: {observation_day} sequence: {sequence_number}."
        assert len(
            values) == 0, f"No registers available for observation day: {observation_day} sequence: {sequence_number}."
        return values[0]

    async def _retrieve_data_async(self, observation_day, sequence_number) -> None:
        """
        """
        _log.info("Retrieving data")
        try:
            md = self._query_observation_data(observation_day, sequence_number)
        except Exception as ex:  #
            logging.exception("Failed retrieving observation information.")
            raise ex

        mount_position = await self.efd.select_packed_time_series("lsst.sal.ATMCS.mount_AzEl_Encoders",
                                                                  ["azimuthCalculatedAngle",
                                                                   "elevationCalculatedAngle"],
                                                                  md.timespan.begin.utc,
                                                                  md.timespan.end.utc)
        rotation = await self.efd.select_packed_time_series("lsst.sal.ATMCS.mount_Nasmyth_Encoders",
                                                            ["nasmyth2CalculatedAngle", ],
                                                            md.timespan.begin.utc,
                                                            md.timespan.end.utc)
        torques = await self.efd.select_packed_time_series("lsst.sal.ATMCS.measuredTorque",
                                                           ["azimuthMotor1Torque",
                                                            "azimuthMotor2Torque",
                                                            "elevationMotorTorque",
                                                            "nasmyth2MotorTorque",
                                                            ],
                                                           md.timespan.begin.utc,
                                                           md.timespan.end.utc)

        afit = np.polyfit(mount_position.times, mount_position["azimuthCalculatedAngle"], 1)
        efit = np.polyfit(mount_position.times, mount_position["elevationCalculatedAngle"], 1)
        rfit = np.polyfit(rotation.times, rotation["nasmyth2CalculatedAngle"], 1)

        mount_position["amodel"] = afit[0] * mount_position.times + afit[1]
        mount_position["emodel"] = efit[0] * mount_position.times + efit[1]
        rotation["rmodel"] = rfit[0] * rotation.times + rfit[1]

        mount_position["az_err"] = (mount_position["azimuthCalculatedAngle"] - mount_position[
            "amodel"]) * 3600
        mount_position["el_err"] = (mount_position["elevationCalculatedAngle"] - mount_position[
            "emodel"]) * 3600
        rotation["rot_err"] = (rotation["nasmyth2CalculatedAngle"] - rotation["rmodel"]) * 3600

        assert (self._data_sources is not None)
        self._data_sources.data = dict(
            mount_x=mount_position.index,
            mount_azimuth_calculate_angle=mount_position["azimuthCalculatedAngle"],
            mount_elevation_calculated_angle=mount_position["elevationCalculatedAngle"],
            mount_azimuth_fit=mount_position["amodel"],
            mount_elevation_fit=mount_position["emodel"],
            mount_nasmyth2_calculated_angle=rotation["rmodel"],
            mount_az_err=mount_position["az_err"],
            mount_el_err=mount_position["el_err"],
            torque_x=torques.index,
            torques_azimuth_motor1_torque=torques["azimuthMotor1Torque"],
            torques_azimuth_motor2_torque=torques["azimuthMotor2Torque"],
            torques_elevation_motor_torque=torques["elevationMotorTorque"],
            torques_nasmyth2_motor_torque=torques["nasmyth2MotorTorque"],
            rotator_x=rotation.index,
            rotator_error=rotation["rot_err"],
            rotator_fit=rotation["rmodel"]
        )
        _log.info("Data refreshed correctly")
