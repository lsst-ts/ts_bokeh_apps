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

from typing import TYPE_CHECKING

from bokeh.models import CustomJS
from lsst.ts.bokeh.apps.examples.bokeh_framework_interactive import interactive_example_layout
from lsst.ts.bokeh.apps.examples.bokeh_framework_interactive.interactive_example_data_aggregator import \
    InteractiveExampleDataAggregator
from lsst.ts.bokeh.utils.bokeh_framework.interaction import Interaction
from typing_extensions import override

if TYPE_CHECKING:
    from lsst.ts.bokeh.utils import Layout

__all__ = ["InteractiveExampleInteraction"]


# child class that inherits from Interaction, has the responsibility of
# creating the interaction between the components from the layout and the user
class InteractiveExampleInteraction(Interaction):
    def __init__(self) -> None:
        super().__init__()

    # A decorator is used in order to advise that the method is override from
    # the base call. Override decorator really doesn't affect the method
    # execution
    @override
    # Method overriden from Interaction to set up the interaction between
    # the user and the components of the Layout, both interactions python and
    # javascript It may be empty, if no interaction is needed
    def setup(self, layout: "Layout") -> None:
        """
        Set up the interaction of the components from the Layout
        :param layout:
        """
        # force type layout also for typing purposes
        assert isinstance(layout, interactive_example_layout.InteractiveExampleLayout)
        data_aggregator = layout.data_aggregator
        assert isinstance(data_aggregator, InteractiveExampleDataAggregator)
        layout.dropdown.js_on_event(
            "menu_item_click",
            CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"),
        )
        layout.dropdown.on_click(lambda: data_aggregator.retrieve_data())
        layout.button.on_click(lambda: data_aggregator.retrieve_data())
