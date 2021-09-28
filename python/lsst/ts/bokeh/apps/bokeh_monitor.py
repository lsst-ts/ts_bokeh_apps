from bokeh.plotting import figure, curdoc
from bokeh.models import Div, ColumnDataSource, ColorBar, LogColorMapper, HoverTool, LabelSet, OpenURL, TapTool
import numpy

import lsst.daf.butler as dafButler
butler = dafButler.Butler('/repo/LATISS', instrument='LATISS', collections='LATISS/raw/all')

day_obs = 20210909
seq_num = 811

def get_data(day_obs, seq_num ):
    calexp = butler.get('raw', day_obs=day_obs, seq_num=seq_num, detector=0)
    md = {'detector': calexp.getDetector()}
    return calexp, md

def organize_data(calexp, md):
    subsample  = calexp.getImage().getArray()[::10,::10]
    ds = ColumnDataSource(
         data = {'image': [subsample], 'dh': [1.0], 'dw': [1.0], 'x': [0], 'y': [0]})
    return ds, md

def render_viz(ds, md):
    box_ds = ColumnDataSource(
             data = {'x': [(1/16) + i*(1/8) for i in range(8)]*2, 'y': [1/4 for j in range(8)]+[3/4 for j in range(8)],
                     'height': [0.5 for i in range(16)], 'width': [1/8. for i in range(16)],
                     'names': [f'C{i}{j}' for i,j in zip([0]*8+[1]*8, [i for i in range(8)]*2)],
                     'x_offset': [-15 for i in range(16)]})

    p = figure(plot_width=1200, plot_height=1100, x_range=(0,1), y_range=(0,1), tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
    color_mapper = LogColorMapper(palette="Viridis256", low=11000, high=21000)

    # must give a vector of image data for image parameter
    img = p.image(image='image', source=ds, color_mapper=color_mapper, dh='dh', dw='dw', x='x', y='y')
    p.grid.grid_line_width = 0.5
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)
    rect = p.rect(x='x', y='y', height='height', width='width', line_color='black', line_width=2, fill_alpha=0., source=box_ds)
    labels = LabelSet(x='x', y='y', text='names', x_offset='x_offset', source=box_ds, render_mode='canvas')

    p.add_layout(color_bar, 'right')
    p.add_layout(labels)
    # Disables the tooltip on rect_renderer, but also does not trigger the outline
    p.hover.renderers = [img]
    # Seperate hover triggers the hover, but also shows an empty tooltip.
    p.add_tools(HoverTool(renderers=[rect], tooltips=None), TapTool(renderers=[rect]))
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url='https://www.google.com/?q=@names')

    return p

calexp, md = get_data(day_obs, seq_num)
ds, md = organize_data(calexp, md)
viz = render_viz(ds, md)

curdoc().add_root(viz)
