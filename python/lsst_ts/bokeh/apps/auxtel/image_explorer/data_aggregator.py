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

import typing
import numpy

from lsst_efd_client import EfdClient

from bokeh.models import ColumnDataSource

from lsst.rapid.analysis import BestEffortIsr
from lsst.pipe.tasks.quickFrameMeasurement import QuickFrameMeasurementTask

from lsst_ts.bokeh.apps.base_data_aggregator import BaseDataAggregator


class DataAggregator(BaseDataAggregator):
    """Data aggregator class for the torque bokeh app."""

    def __init__(self) -> None:
        super().__init__()

        self.day_obs = 20211005
        self.seq_num = 236
        self.data_cache = dict()

    def create_data_sources(self) -> None:
        self.efd = EfdClient("summit_efd")
        qm_config = QuickFrameMeasurementTask.ConfigClass()
        self.qm = QuickFrameMeasurementTask(config=qm_config)
        self.best_effort_isr = BestEffortIsr("/repo/LATISS")

    def initialize_data_sources(self, *args, **kwargs) -> None:
        """Initialize data sources."""

        self.create_data_sources()

        self.data_sources["column_data_source"] = ColumnDataSource(
            data=dict(
                image=[numpy.zeros((4, 4))],
                dh=[1.0],
                dw=[1.0],
                x=[0],
                y=[0],
                image_low=[0],
                image_high=[0],
            )
        )

    def retrieve_data(self, *args: typing.Any, **kwargs: typing.Any) -> None:

        exposure_id = f"{self.day_obs}{self.seq_num:05d}"
        if exposure_id in self.data_cache:
            best_effor_exp = self.data_cache[exposure_id]
        else:
            best_effor_exp = self.best_effort_isr.getExposure(
                dict(day_obs=self.day_obs, seq_num=self.seq_num, detector=0)
            )
            self.data_cache[exposure_id] = best_effor_exp

        self.data_sources["column_data_source"].data["image"] = [
            best_effor_exp.getImage().getArray()[::10, ::10]
        ]
        self.data_sources["column_data_source"].data["image_low"] = [
            numpy.min(best_effor_exp.getImage().getArray()[::10, ::10])
        ]
        self.data_sources["column_data_source"].data["image_high"] = [
            numpy.max(best_effor_exp.getImage().getArray()[::10, ::10])
        ]
