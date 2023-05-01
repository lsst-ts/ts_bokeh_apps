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

__all__ = ["BaseDataAggregator"]

import abc
import logging
import typing


class BaseDataAggregator(metaclass=abc.ABCMeta):
    """Base data aggregator class for building bokeh apps.

    Attributes
    ----------
    data_sources : `dict`
        Dictionary to host the bokeh data sources.
    """

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)

    def initialize_data_sources(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Method to initialize data sources."""
        raise NotImplementedError()

    @abc.abstractmethod
    def retrieve_data(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Retrieve data and set up the data sources streams."""
        raise NotImplementedError()
