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

from bokeh.models import Column, Row
from bokeh.models.renderers import GlyphRenderer
from bokeh.models.widgets.buttons import Button, Dropdown
from bokeh.plotting import figure
from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive.interactive_example_data_aggregator import \
    InteractiveExampleDataAggregator
from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive.interactive_example_interaction import \
    InteractiveExampleInteraction
from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout
from typing_extensions import override

if TYPE_CHECKING:
    from typing import Optional  # noqa: F401

    from bokeh.models import LayoutDOM

__all__ = ["InteractiveExampleLayout"]


# child class that inherits from Layout, has the responsibility of creating
# the application Layout (the view with all its components)
class InteractiveExampleLayout(Layout):
    """ """

    MENU = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]

    def __init__(self) -> None:
        super().__init__(
            InteractiveExampleInteraction(), InteractiveExampleDataAggregator()
        )
        # Attributes used by the class must be defined in the __init__ method.
        # Type is used to set the variable type, it has 2 uses:
        # .- Other readers can know which is the type value (without checking
        #   through the code)
        # .- Static checker may be run to check is variables are correctly used
        # according to its type
        # Attributes by definition should be private hence '_' is needed
        self._plot_text = None  # type: Optional[GlyphRenderer]
        self._dropdown = None  # type: Optional[Dropdown]
        self._button = None  # type: Optional[Button]
        self._plot = None  # type: Optional[figure]

    # A decorator is used in order to advise that the method is override from
    # the
    # base call. Override decorator really doesn't affect the method execution
    @override
    # Method overriden to create the layout of the application,
    # Should always return a LayoutDOM, so better puts all component inside a
    # Layout (Row, Column...)
    # (check UIElement when upgrading to bokeh 3.0.x)
    def define(self) -> "LayoutDOM":
        self._plot = figure(
            border_fill_color="black",
            background_fill_color="black",
            outline_line_color="blue",
            toolbar_location=None,
            x_range=(0, 100),
            y_range=(0, 100),
        )
        self._plot.grid.grid_line_color = None
        self._plot_text = self._plot.text(
            x=[],
            y=[],
            text=[],
            text_color=[],
            text_font_size="26px",
            text_baseline="middle",
            text_align="center",
        )
        # Assert used since type of variable has been defined as optional
        assert self._plot_text is not None
        # Layout has a getter to access to data_aggregator, data_source is
        # linked from the plot we are showing. This is defined here but all
        # reference to data should be encapsulated inside the data_aggregator
        self.data_aggregator.data_source = self._plot_text.data_source
        # add a button widget and configure with the call back
        self._button = Button(label="Press Me")
        self._dropdown = Dropdown(
            label="Dropdown button",
            button_type="warning",
            menu=InteractiveExampleLayout.MENU,
        )
        return Column(
            children=[Row(children=[self._dropdown, self._button]), self._plot]
        )

    # According to general OOP programming concepts, attributes should be
    # private and be accessible using a getter. In python concretely all
    # attributes are declared a 'private' beginning with "_" and use @property
    # decorator to create the getter to access the attribute
    @property
    def plot_text(self) -> GlyphRenderer:
        # Assert used since type of variable has been defined as optional
        assert self._plot_text is not None
        return self._plot_text

    @property
    def button(self) -> "Button":
        # Assert used since type of variable has been defined as optional
        assert self._button is not None
        return self._button

    @property
    def dropdown(self) -> "Dropdown":
        # Assert used since type of variable has been defined as optional
        assert self._dropdown is not None
        return self._dropdown

    @property
    def plot(self) -> "figure":
        # Assert used since type of variable has been defined as optional
        assert self._plot is not None
        return self._plot
