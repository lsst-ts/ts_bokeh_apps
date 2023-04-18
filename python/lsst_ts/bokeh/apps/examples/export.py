from lsst_ts.bokeh.main.server_information import ServerInformation
from lsst_ts.bokeh.apps.examples.bokeh_raw.export import initialize_app as bokeh_basic_example_initialize_app
from lsst_ts.bokeh.apps.examples.bokeh_static.export import initialize_app as bokeh_static_example_initialize_app
from lsst_ts.bokeh.apps.examples.flask_raw.export import initialize_app as flask_raw_example_initialize_app
from lsst_ts.bokeh.apps.examples.flask_embedding_bokeh.export import initialize_app as flask_embedding_bokeh_initialize_app
from lsst_ts.bokeh.apps.examples.flask_bokeh_full.export import initialize_app as flask_full_example_initialize_app
from lsst_ts.bokeh.apps.examples.flask_react_simple.export import initialize_app as flask_react_simple_app


def generate_examples_page(flask_host: str, bokeh_host: str):
     return  f"<!doctype html>\
                    <html lang=\"en\">\
                    <head>\
                      <meta charset=\"utf-8\">\
                      <title>Bokeh Application Selector</title>\
                    </head>\
                    <body>\
                      <div>\
                        <a  target=\"_blank\" href=\"{bokeh_host}/examples/bokeh_raw\"> Bokeh Raw Example</a><br/>\
                        <a  target=\"_blank\" href=\"{bokeh_host}/examples/bokeh_static\"> Bokeh Static Example</a><br/>\
                        <a  target=\"_blank\" href=\"{flask_host}/examples/examples_menu\">Flask Raw Example</a><br/>\
                        <a  target=\"_blank\" href=\"{flask_host}/examples/flask_embedding_bokeh_example\">Flask Embedding Bokeh Example</a><br/>\
                        <a  target=\"_blank\" href=\"{flask_host}/examples/flask_bokeh_full\">Flask Bokeh Full Example</a><br/>\
                        <a  target=\"_blank\" href=\"{flask_host}/examples/flask_react_simple\">Flask React Simple Example</a><br/>\
                      </div>\
                    </body>\
                    </html>"


def initialize_app(server_information: ServerInformation):

    @server_information.flask_app.route(f"/examples", methods=["GET"])
    def examples():
        return generate_examples_page(server_information.get_application_information("bokeh_connection_server"),
                                      server_information.get_application_information("flask_connection_server"))


    bokeh_basic_example_initialize_app(server_information)
    bokeh_static_example_initialize_app(server_information)
    flask_raw_example_initialize_app(server_information)
    flask_embedding_bokeh_initialize_app(server_information)
    flask_full_example_initialize_app(server_information)
    flask_react_simple_app(server_information)