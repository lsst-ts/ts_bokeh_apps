from lsst_ts.bokeh.app_templates.plot_2D_viewer.application import Plot2DApplication
from lsst_ts.bokeh.main.server_information import ServerInformation


def initialize_app(server_information: ServerInformation):
    app = Plot2DApplication(server_information, "2dplot_example")
    app.deploy()
    app1 = Plot2DApplication(server_information, "2dplot_example1")
    app1.deploy()
    app2 = Plot2DApplication(server_information, "2dplot_example2")
    app2.deploy()
    app3 = Plot2DApplication(server_information, "2dplot_example3")
    app3.deploy()