from bokeh import plotting # type: ignore
from bokeh.io import show
from bokeh.layouts import row, layout, column
from bokeh.models import Paragraph, Button, ScrollBox, CustomJS, ColumnDataSource, Slider
from bokeh.events import Pan, MouseWheel
from bokeh import events
from bokeh.plotting import figure

from lsst_ts.bokeh.widgets.range_slider.range_slider import IonRangeSlider
from lsst_ts.bokeh.widgets.scrollable_div.scrollable_div import ScrollableDiv


def newfunc(attr, old, new):
    print("Scrolling!")

class SandboxApplication:

    def __init__(self):
        pass

    def _event(self, ev):
        print(ev)

    def create(self) -> layout:
        _children = []
        for i in range(200):
            _children.append(Button(label = f"CLICK {i}" ))
        col = column(children = _children)
        scroll = ScrollBox(child = col, height=500, name="empty")
        scroll.on_event(MouseWheel, self._event)
        scroll.on_change("vertical_scrollbar.position", newfunc)
        callback = CustomJS(args=dict(), code="""
                console.log("Scrolling!")
                   

        """)
        b = Button(label=f"CLICK {i}")
        print(scroll.js_event_callbacks)
        print(col.js_event_callbacks)
        point_events = [
            events.Tap, events.DoubleTap, events.Press, events.PressUp,
            events.MouseMove, events.MouseEnter, events.MouseLeave,
            events.PanStart, events.PanEnd, events.PinchStart, events.PinchEnd, events.MouseWheel
        ]

        for event in point_events:
            scroll.js_on_event(event, callback)

        return scroll
#
if __name__.startswith("bokeh_app_"):
    print(f"name: {0}".format(__name__))
    app = SandboxApplication()
    widget = app.create()
    #
    doc = plotting.curdoc()
    doc.add_root(widget)
    # scrollable_div = ScrollableDiv(width = 800, height = 400, styles={'background-color': 'red', 'overflow-y': 'auto'})
    # doc.add_root(column(children=[scrollable_div], name='empty'))


    #
    # x = [x * 0.005 for x in range(2, 198)]
    # y = x
    #
    # source = ColumnDataSource(data=dict(x=x, y=y))
    #
    # plot = figure(width=600, height=600)
    # plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6, color='#ed5565')
    #
    # callback_single = CustomJS(args=dict(source=source), code="""
    #     const f = cb_obj.value
    #     const x = source.data.x
    #     const y = Array.from(x, (x) => Math.pow(x, f))
    #     source.data = {x, y}
    # """)
    #
    # callback_ion = CustomJS(args=dict(source=source), code="""
    #     const {data} = source
    #     const f = cb_obj.range
    #     const pow = (Math.log(data.y[100]) / Math.log(data.x[100]))
    #     const delta = (f[1] - f[0]) / data.x.length
    #     const x = Array.from(data.x, (x, i) => delta*i + f[0])
    #     const y = Array.from(x, (x) => Math.pow(x, pow))
    #     source.data = {x, y}
    # """)
    #
    # slider = Slider(start=0, end=5, step=0.1, value=1, title="Bokeh Slider - Power")
    # slider.js_on_change('value', callback_single)
    #
    # ion_range_slider = IonRangeSlider(start=0.01, end=0.99, step=0.01, range=(min(x), max(x)),
    #                                   title='Ion Range Slider - Range')
    # ion_range_slider.js_on_change('range', callback_ion)
    # doc.add_root(column(children=[plot, slider, ion_range_slider], name = 'empty'))

if __name__ == '__main__':
    app = SandboxApplication()
    show(app.create())
