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

__all__ = ["BaseInteraction"]

import abc
import logging

from bokeh.plotting import curdoc
from .base_layout import BaseLayout


class BaseInteraction(metaclass=abc.ABCMeta):
    """Base layout class for building bokeh apps."""

    def __init__(self, layout: BaseLayout) -> None:
        self.page = None
        self.log = logging.getLogger(__name__)
        self.layout = layout
        self.setup_interaction()

    @abc.abstractmethod
    def setup_interaction(self) -> None:
        raise NotImplementedError()

    def __call__(self) -> None:
        self.page = self.layout.get_page()
        self.doc = curdoc()
        self.doc.add_root(self.page)

    def modify_doc(self, doc) -> None:
        self.page = self.layout.get_page()
        doc.add_root(self.page)
