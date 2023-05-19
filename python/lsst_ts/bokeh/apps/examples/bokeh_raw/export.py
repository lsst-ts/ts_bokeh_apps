from bokeh.document import Document
from lsst_ts.bokeh.apps.examples.bokeh_raw.layout import Layout
from lsst_ts.bokeh.main.server_information import ServerInformation


def initialize_app(server_information: ServerInformation) -> ServerInformation:
    def create_application(doc: Document) -> None:
        try:
            app = Layout()
            app.create(doc)
            doc.title = "Bokeh raw Example"
        except Exception as ex:
            import traceback

            traceback.print_exc()
            print(ex)

    server_information.add_application("/examples/bokeh_raw", create_application)
    return server_information
