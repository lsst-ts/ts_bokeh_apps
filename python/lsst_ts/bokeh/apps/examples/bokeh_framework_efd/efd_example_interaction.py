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

from lsst_ts.bokeh.apps.examples.bokeh_framework_efd import efd_example_layout
from lsst_ts.bokeh.utils.bokeh_framework.interaction import Interaction

from typing import TYPE_CHECKING

from lsst_ts.library.utils.logger import get_logger

_log = get_logger("examples.efd.data_aggregator")

if TYPE_CHECKING:
    from typing import Optional
    from lsst_ts.bokeh.apps.examples.bokeh_framework_efd.efd_example_data_aggregator import \
        EfdExampleDataAggregator
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

class EfdExampleInteraction(Interaction):

    def __init__(self):
        super().__init__()
        self._data_aggregator = None # Optional[EfdExampleDataAggregator]

    def setup(self, layout: 'Layout') -> None:
        assert (isinstance(layout, efd_example_layout.EfdExampleLayout))
        self._data_aggregator = layout.data_aggregator
        text_input = layout.text_input
        text_input.on_change("value", self._handle_text_input)

    def _handle_text_input(self, attr, old, new):
        try:
            assert(self._data_aggregator is not None)
            observation_day = int(new[:8])
            sequence_number = int(new[8:])
            _log.debug(f"Processing: {new}.")
            self._data_aggregator.update_observation_information(observation_day, sequence_number)
        except Exception:
            _log.exception(f"Error retrieving data for {new}.")