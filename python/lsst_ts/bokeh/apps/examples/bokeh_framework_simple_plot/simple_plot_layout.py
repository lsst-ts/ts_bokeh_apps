# CPIO Example comment: First installed and python default imports. Alphabetical order
from bokeh.models import Row
from bokeh.plotting import figure
from typing_extensions import override

# CPIO Example comment: Second Own lobrary imports. Alphabetical order
from lsst_ts.bokeh.apps.examples.bokeh_framework_simple_plot.simple_plot_data_aggregator import \
    SimplePlotDataAggregator
from lsst_ts.bokeh.utils.bokeh_framework.layout import Layout

# CPIO Example comment: Third Type checking imports (optional). Alphabetical order
from typing import TYPE_CHECKING

# CPIO Example comment: If Variables are only for type checking they may be declared inside this conditional
# but is optional to have it inside
if TYPE_CHECKING:
    from typing import Optional
    from bokeh.models import LayoutDOM

__all__ = ['SimplePlotLayout']

# CPIO Example comment: child class that inherits from Layout, has the responsibility of creating
# the application Layout (the view with all its components)
class SimplePlotLayout(Layout):

    def __init__(self) -> None:
        super().__init__(data_aggregator=SimplePlotDataAggregator())
        # CPIO Example comment: Attributes used by the class must be defined in the __init__ method.
        # Type is used to set the variable type, it has 2 uses:
        # .- Other readers can know which is the type value (without checking through the code)
        # .- Static checker may be run to check is variables are correctly used according to its type
        self._plot = None # type: Optional[figure]

    # CPIO Example comment: A decorator is used in order to advise that the method is override  from the
    # base call. Override decorator really doesn't affect the method execution
    @override
    # CPIO Example comment: Method overriden to create the layout of the application,
    # Should always return a LayoutDOM, so better puts all component inside a Layout (Row, Column...)
    # (check UIElement when upgrading to bokeh 3.0.x)
    def define(self) -> 'LayoutDOM':
        self._plot = figure()
        return Row(children=[self._plot], name="SimplePlot")

    # CPIO Example comment: According to general OOP programming concepts, attributes should be private
    # and be accessible using a getter. In python concretely all attributes are declared a 'private' beginning
    # with "_" and use @property decorator to create the getter to access the attribute
    @property
    def plot(self) -> 'figure':
        # CPIO Example comment: Assert used since type of variable has been defined as optional
        assert(self._plot is not None)
        return self._plot