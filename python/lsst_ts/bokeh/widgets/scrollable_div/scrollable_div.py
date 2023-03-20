
from bokeh.core.properties import Bool
from bokeh.models import Div


class ScrollableDiv(Div):
    # The special class attribute ``__implementation__`` should contain a string
    # of JavaScript or TypeScript code that implements the web browser
    # side of the custom extension model or a string name of a file with the implementation.

    __implementation__ = "scrollable_div.ts"
    __javascript__ = []

    # Below are all the "properties" for this model. Bokeh properties are
    # class attributes that define the fields (and their types) that can be
    # communicated automatically between Python and the browser. Properties
    # also support type validation. More information about properties in
    # can be found here:
    #
    #    https://docs.bokeh.org/en/latest/docs/reference/core/properties.html#bokeh-core-properties

    disable = Bool(default=False, help="""
    """)
