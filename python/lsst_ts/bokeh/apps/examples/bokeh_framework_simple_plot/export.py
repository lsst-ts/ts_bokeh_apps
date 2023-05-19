import os

from bokeh.document import Document
from jinja2 import Environment, FileSystemLoader
from lsst_ts.bokeh.apps.examples.bokeh_framework_simple_plot.simple_plot_layout import \
    SimplePlotLayout
from lsst_ts.bokeh.main.server_information import ServerInformation


def initialize_app(server_information: ServerInformation) -> ServerInformation:
    def create_application(doc: Document) -> None:
        try:
            app = SimplePlotLayout()
            app.deploy(doc)
            doc.title = "Bokeh framework Simple Plot"
            template_dir = os.path.normpath(os.path.dirname(__file__))
            env = Environment(loader=FileSystemLoader(template_dir))
            index_template = env.get_template("templates/index.html")
            doc.template = index_template
        except Exception as ex:
            import traceback

            traceback.print_exc()
            print(ex)

    server_information.add_application(
        "/examples/bokeh_framework_simple_plot", create_application
    )
    return server_information
