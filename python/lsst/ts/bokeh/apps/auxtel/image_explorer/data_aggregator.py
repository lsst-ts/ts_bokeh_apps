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

import lsst.daf.butler as dafButler

from lsst_efd_client import EfdClient

from bokeh.models import ColumnDataSource

from lsst.ts.bokeh.apps.base_data_aggregator import BaseDataAggregator


class DataAggregator(BaseDataAggregator):
    """Data aggregator class for the torque bokeh app."""

    def __init__(self) -> None:
        super().__init__()

        self.day_obs = 20211005
        self.seq_num = 236
        self.data_cache = dict()

    def create_data_sources(self):
        self.butler = dafButler.Butler(
            "/repo/LATISS", instrument="LATISS", collections="LATISS/raw/all"
        )
        self.efd = EfdClient("summit_efd")

    def initialize_data_sources(self, *args, **kwargs):
        """Initialize data sources."""

        self.create_data_sources()

        self.data_sources["column_data_source"] = ColumnDataSource(
            data=dict(image=[numpy.zeros((4, 4))], dh=[1.0], dw=[1.0], x=[0], y=[0])
        )

    def retrieve_data(self, *args, **kwargs):

        exposure_id = f"{self.day_obs}{self.seq_num:05d}"
        if exposure_id in self.data_cache:
            calexp = self.data_cache[exposure_id]
        else:
            calexp = self.butler.get(
                "raw", day_obs=self.day_obs, seq_num=self.seq_num, detector=0
            )
            self.data_cache[exposure_id] = calexp

        self.data_sources["column_data_source"].data["image"] = [
            calexp.getImage().getArray()[::10, ::10]
        ]
