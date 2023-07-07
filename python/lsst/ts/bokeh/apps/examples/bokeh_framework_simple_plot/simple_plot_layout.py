# First installed and python default imports. Alphabetical order
# Third Type checking imports (optional). Alphabetical order
from typing import TYPE_CHECKING

from bokeh.models import Row
from bokeh.plotting import figure
from lsst.ts.bokeh.apps.examples.bokeh_framework_simple_plot.simple_plot_data_aggregator import \
    SimplePlotDataAggregator
from lsst.ts.bokeh.utils.bokeh_framework.layout import Layout
from typing_extensions import override

if TYPE_CHECKING:
    from typing import Optional  # noqa: F401

    from bokeh.models import LayoutDOM

__all__ = ["SimplePlotLayout"]


# child class that inherits from Layout, has the responsibility of creating
# the application Layout (the view with all its components)
class SimplePlotLayout(Layout):
    def __init__(self) -> None:
        super().__init__(data_aggregator=SimplePlotDataAggregator())
        # Attributes used by the class must be defined in the __init__ method.
        # Type is used to set the variable type, it has 2 uses:
        # .- Other readers can know which is the type value
        # (without checking through the code)
        # .- Static checker may be run to check is variables are correctly
        # used according to its type
        self._plot = None  # type: Optional[figure]

    # A decorator is used in order to advise that the method is override from
    # the base call. Override decorator really doesn't affect the method
    # execution
    @override
    # Method overriden to create the layout of the application,
    # Should always return a LayoutDOM, so better puts all component inside a
    # Layout (Row, Column...)
    # (check UIElement when upgrading to bokeh 3.0.x)
    def define(self) -> 'LayoutDOM':
        """
        Method to create the layout of the application, including
        all its components
        :return: Layout of the application
        """
        self._plot = figure()
        return Row(children=[self._plot], name="SimplePlot")

    # According to general OOP programming concepts, attributes should be
    # private and be accessible using a getter. In python concretely all
    # attributes are declared a 'private' beginning with "_" and use @property
    # decorator to create the getter to access the attribute
    @property
    def plot(self) -> 'figure':
        """
        Getter for plot to use by the interaction class
        :return: plot from the application
        """
        # Assert used since type of variable has been defined as optional
        assert self._plot is not None
        return self._plot
