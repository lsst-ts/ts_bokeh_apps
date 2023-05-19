from lsst.ts.bokeh.apps.examples.bokeh_framework_interactive import \
    initialize_app as bokeh_framework_interactive_example_initialize_app
from lsst.ts.bokeh.apps.examples.bokeh_framework_simple_plot import \
    initialize_app as bokeh_framework_simple_plot_example_initialize_app
from lsst.ts.bokeh.apps.examples.bokeh_raw import \
    initialize_app as bokeh_basic_example_initialize_app
from lsst.ts.bokeh.apps.examples.bokeh_static import \
    initialize_app as bokeh_static_example_initialize_app
from lsst.ts.bokeh.apps.examples.flask_bokeh_full.export import \
    initialize_app as flask_full_example_initialize_app
from lsst.ts.bokeh.apps.examples.flask_embedding_bokeh import \
    initialize_app as flask_embedding_bokeh_initialize_app
from lsst.ts.bokeh.apps.examples.flask_raw.export import \
    initialize_app as flask_raw_example_initialize_app
from lsst.ts.bokeh.apps.examples.flask_react_simple.export import \
    initialize_app as flask_react_simple_app
from lsst.ts.bokeh.main.server_information import ServerInformation


def generate_examples_page(bokeh_host: str, flask_host: str) -> str:
    return (
        f'<!doctype html>\
        <html lang="en">\
        <head>\
          <meta charset="utf-8">\
          <title>Bokeh Application Selector</title>\
        </head>\
        <body>\
      <div>\
        <a  target="_blank" '
        f'href="{bokeh_host}/examples/bokeh_raw"> Bokeh Raw Example</a><br/>\
        <a  target="_blank" '
        f'href="{bokeh_host}/examples/bokeh_static"> Bokeh Static Example</a><br/>\
        <a  target="_blank" '
        f'href="{bokeh_host}/examples/bokeh_framework_interactive">'
        f'Bokeh Framework Interactive Example</a><br/>\
        <a  target="_blank" '
        f'href="{bokeh_host}/examples/bokeh_framework_simple_plot">Bokeh Framework Simple plot</a><br/>\
        <a  target="_blank" '
        f'href="{flask_host}/examples/examples_menu">Flask Raw Example</a><br/>\
        <a  target="_blank" '
        f'href="{flask_host}/examples/flask_embedding_bokeh_example">'
        f'Flask Embedding Bokeh Example</a><br/>\
        <a  target="_blank" '
        f'href="{flask_host}/examples/flask_bokeh_full">Flask Bokeh Full Example</a><br/>\
        <a  target="_blank" '
        f'href="{flask_host}/examples/flask_react_simple">Flask React Example</a><br/>\
      </div>\
        </body>\
        </html>'
    )


def initialize_app(server_information: ServerInformation) -> ServerInformation:
    @server_information.flask_app.route("/examples", methods=["GET"])
    def examples() -> str:
        return generate_examples_page(
            str(
                server_information.get_application_information(
                    "bokeh_connection_server"
                )
            ),
            str(
                server_information.get_application_information(
                    "flask_connection_server"
                )
            ),
        )

    bokeh_basic_example_initialize_app(server_information)
    bokeh_static_example_initialize_app(server_information)
    flask_raw_example_initialize_app(server_information)
    flask_embedding_bokeh_initialize_app(server_information)
    flask_full_example_initialize_app(server_information)
    flask_react_simple_app(server_information)
    bokeh_framework_interactive_example_initialize_app(server_information)
    bokeh_framework_simple_plot_example_initialize_app(server_information)
    return server_information
