from bokeh.plotting import figure
from bokeh.models.widgets.buttons import Button, Dropdown
from bokeh.models.renderers.glyph_renderer import GlyphRenderer

from bokeh.models import Column, Row

from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive.interactive_example_data_aggregator import \
    InteractiveExampleDataAggregator
from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive.interactive_example_interaction import \
    InteractiveExampleInteraction
from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from bokeh.models.ui.ui_element import UIElement


class InteractiveExampleLayout(Layout):
    """
    """
    MENU = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]

    def __init__(self) -> None:
        super().__init__(InteractiveExampleInteraction(), InteractiveExampleDataAggregator())
        self._plot_text = None # type Optional[GlyphRenderer]
        self._dropdown = None # type: Optional[Dropdown]
        self._button = None # type: Optional[Button]
        self._plot = None # type: Optional[figure]

    def define(self) -> 'UIElement':
        self._plot = figure(border_fill_color="black",
                   background_fill_color="black",
                   outline_line_color="blue",
                   toolbar_location=None,
                   x_range=(0, 100),
                   y_range=(0, 100))
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
        assert (self._plot_text is not None)
        self.data_aggregator.data_source = self._plot_text.data_source
        # self.data_aggregator.data_sources["column_data_source"] = r.data_source # noqa: W505
        # add a button widget and configure with the call back
        self._button = Button(label="Press Me")
        self._dropdown = Dropdown(label="Dropdown button", button_type="warning",
                                  menu=InteractiveExampleLayout.MENU)
        return Column(children=[Row(children=[self._dropdown, self._button]), self._plot])

    @property
    def plot_text(self) -> GlyphRenderer:
        assert (self._plot_text is not None)
        return self._plot_text

    @property
    def button(self) -> 'Button':
        assert(self._button is not None)
        return self._button

    @property
    def dropdown(self) -> 'Dropdown':
        assert(self._dropdown is not None)
        return self._dropdown

    @property
    def plot(self) -> 'figure':
        assert(self._plot is not None)
        return self._plot
