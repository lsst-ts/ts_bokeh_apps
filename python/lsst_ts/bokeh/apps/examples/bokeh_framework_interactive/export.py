from bokeh.document import Document
from lsst_ts.bokeh.apps.examples.bokeh_framework_interactive.interactive_example_layout import \
    InteractiveExampleLayout
from lsst_ts.bokeh.main.server_information import ServerInformation


def initialize_app(server_information: ServerInformation) -> ServerInformation:
    def create_application(doc: Document) -> None:
        try:
            app = InteractiveExampleLayout()
            app.deploy(doc)
            doc.title = "Bokeh framework interactive Example"
        except Exception as ex:
            import traceback

            traceback.print_exc()
            print(ex)

    server_information.add_application(
        "/examples/bokeh_framework_interactive", create_application
    )
    return server_information
