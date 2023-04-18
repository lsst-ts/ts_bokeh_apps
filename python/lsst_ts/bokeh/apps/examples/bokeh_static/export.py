import os

from bokeh.document import Document
from jinja2 import Environment, FileSystemLoader

from lsst_ts.bokeh.apps.examples.bokeh_static.layout import Layout
from lsst_ts.bokeh.main.server_information import ServerInformation

def initialize_app(server_information: ServerInformation):

    def create_application(doc: Document):
        try:
            app = Layout()
            app.create(doc)
            template_dir = os.path.normpath(os.path.dirname(__file__))
            env = Environment(loader=FileSystemLoader(template_dir))
            index_template = env.get_template("templates/index.html")
            doc.title = "Bokeh Static Example"
            doc.template = index_template
        except Exception as ex:
            import traceback
            traceback.print_exc()

    server_information.add_application("/examples/bokeh_static", create_application)
    return server_information