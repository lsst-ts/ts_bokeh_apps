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

__all__ = ["BaseLayout"]

import abc
import logging


class BaseLayout(metaclass=abc.ABCMeta):
    """Base layout class for building bokeh apps."""

    def __init__(self, data_aggregator) -> None:

        self.log = logging.getLogger(__name__)

        self.data_aggregator = data_aggregator
        self.data_aggregator.initialize_data_sources()
        try:
            self.data_aggregator.retrieve_data()
        except Exception:
            self.log.exception("Failed to retrieve initial dataset.")

    @abc.abstractmethod
    def get_page(self):
        """Method to initialize data sources."""
        raise NotImplementedError()
