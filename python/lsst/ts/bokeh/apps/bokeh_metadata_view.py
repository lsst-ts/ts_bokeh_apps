import numpy


from astropy.time import Time
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Span, Div
from bokeh.models.widgets import DataTable, TableColumn, Dropdown
from bokeh.transform import linear_cmap
from bokeh.palettes import Magma256

TELEM_SELECTED = 'seeing'
INDEX_SELECTED = None

def get_data(t_start, t_end):
    def gen_random_walk(n_step=100):

        """
        Generate motion by random walk

        Arguments:
            n_step: Number of steps

        Returns:
            A NumPy array with `n_steps` points
        """
        w = numpy.ones(n_step)

        for i in range(1, n_step):
            # Sampling from the Normal distribution with probability 1/2
            yi = numpy.random.choice([1,-1])
            # Weiner process
            w[i] = w[i-1]+(yi/numpy.sqrt(n_step))

        return w

    n_chips = 45
    time_o = 1632768757
    steps = int(24*60/5)  # one sample every 5 minutes for a day
    utimes = [time_o + i for i in range(steps)]
    times = Time(utimes, format='unix', scale='utc')
    trace_data = {'x': times.datetime}
    names = ['id', 'seeing', 'transparency', 'background', 'zero_point']
    trace_data['seeing'] = {}
    trace_data['background'] = {}
    trace_data['transparency'] = {}
    trace_data['zero_point'] = {}
    for i in range(n_chips):
        print("doing ", i, "out of ", n_chips)
        trace_data['seeing'][i] = gen_random_walk(steps)
        trace_data['background'][i] = gen_random_walk(steps)
        trace_data['transparency'][i] = gen_random_walk(steps)
        trace_data['zero_point'][i] = gen_random_walk(steps)

    camera_data = {'x': [4, 5, 6]*3 + [1, 2, 3, 4, 5, 6, 7, 8, 9]*3 + [4, 5, 6]*3,
                   'y': [1,]*3 + [2,]*3 + [3,]*3 + [4,]*9 + [5,]*9 + [6,]*9 + [7,]*3 + [8,]*3 + [9,]*3,
                   'id': [i for i in range(45)],
                   'seeing': [numpy.mean(v) for k, v in trace_data['seeing'].items()],
                   'background': [numpy.mean(v) for k, v in trace_data['background'].items()],
                   'transparency': [numpy.mean(v) for k, v in trace_data['transparency'].items()],
                   'zero_point': [numpy.mean(v) for k, v in trace_data['zero_point'].items()]}

    return names, trace_data, camera_data


def organize_data(trace_data, camera_data):
    trace_source = ColumnDataSource(data={'x': [], 'y': []})
    camera_source = ColumnDataSource(data=camera_data)
    return trace_source, camera_source

def visualize_data(trace_data, trace_source, camera_source, names):
    rect_source = ColumnDataSource( data={'x': camera_source.data['x'], 'y': camera_source.data['y'], 'value': camera_source.data[TELEM_SELECTED]} )
    trace = figure(plot_width=800, plot_height=200, x_axis_type='datetime')
    line = trace.line(
                    x='x', y='y', line_width=2, source=trace_source
                 )

    columns = [ TableColumn(field=name) for name in names ]
    data_table = DataTable(source=camera_source, columns=columns, width=800, height=200)

    def update_trace(attr, old, new):
        global INDEX_SELECTED
        INDEX_SELECTED = new[0]
        trace_source.data = {'x': trace_data['x'], 'y': trace_data[TELEM_SELECTED][new[0]]}

    def dropdown_callback(new):
        global TELEM_SELECTED
        TELEM_SELECTED = new.item
        rect_source.data = {'x': camera_source.data['x'], 'y': camera_source.data['y'], 'value': camera_source.data[TELEM_SELECTED]}
        if INDEX_SELECTED:
            update_trace('indices', [], [INDEX_SELECTED])

    menu = [(name, name) for name in names[1:]]
    dropdown = Dropdown(label="Visit Information", menu=menu)
    dropdown.on_click(dropdown_callback)

    TOOLTIPS = [
    ("index", "$index"),
    ("value", "@value"),
    ]
    rect_source.selected.on_change('indices', update_trace)
    fp = figure(plot_width=800, plot_height=800, tools="hover,tap", tooltips=TOOLTIPS)
    rect = fp.rect(x='x', y='y', width=0.95, height=0.95, fill_color=linear_cmap('value', palette=Magma256, low=-2, high=2), source=rect_source)

    return column(column(data_table, trace, dropdown, fp))


names, trace_data, camera_data = get_data(None, None)
trace_source, camera_source = organize_data(trace_data, camera_data)
viz = visualize_data(trace_data, trace_source, camera_source, names)


curdoc().add_root(viz)
