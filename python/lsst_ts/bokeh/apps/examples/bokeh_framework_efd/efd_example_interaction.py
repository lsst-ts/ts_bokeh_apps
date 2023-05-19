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

# Type checking imports (optional). Alphabetical order
from typing import TYPE_CHECKING

from lsst_ts.bokeh.apps.examples.bokeh_framework_efd import efd_example_layout
from lsst_ts.bokeh.utils.bokeh_framework.interaction import Interaction
from lsst_ts.bokeh.utils.bokeh_framework.utils import CustomWidgets
from lsst_ts.library.utils.logger import get_logger
from typing_extensions import override

if TYPE_CHECKING:
    from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

# User this function get_logger in order to obtain a valid logger that will
# be integrated inside the application
_log = get_logger("examples.efd.data_aggregator")


# child class that inherits from Interaction, has the responsibility of
# creating the interaction between the components from the layout and the user
class EfdExampleInteraction(Interaction):
    def __init__(self):
        super().__init__()
        self._data_aggregator = None  # Optional[EfdExampleDataAggregator]

    # A decorator is used in order to advise that the method is override
    # from the base call. Override decorator really doesn't affect the
    # method execution
    @override
    def setup(self, layout: "Layout") -> None:
        """
        Set up the interaction of the components from the Layout
        :param layout:
        """
        assert isinstance(layout, efd_example_layout.EfdExampleLayout)
        self._data_aggregator = layout.data_aggregator
        text_input = layout.text_input
        text_input.on_change("value", self._handle_text_input)

    # Callback to be executed when handle input text changes
    def _handle_text_input(self, attr, old, new):
        """
        Callback method that will be called when text input is changed
        :param attr: attribute name
        :param old: old attribute value
        :param new: new attribute value
        :return:
        """
        try:
            assert self._data_aggregator is not None
            # Reset the custom widgets we are using
            custom_widgets = CustomWidgets.get_custom_widgets()
            custom_widgets.reset()
            observation_day = int(new[:8])
            sequence_number = int(new[8:])
            _log.debug(f"Processing: {new}.")
            self._data_aggregator.update_observation_information(
                observation_day, sequence_number
            )
        except Exception as ex:
            _log.exception(f"Error retrieving data for {new}: {str(ex)}")
