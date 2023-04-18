from lsst_ts.bokeh.main.server_information import ServerInformation
from lsst_ts.bokeh.apps.examples.bokeh_raw.export import initialize_app as bokeh_basic_example_initialize_app
from lsst_ts.bokeh.apps.examples.bokeh_static.export import initialize_app as bokeh_static_example_initialize_app

def generate_examples_page(bokeh_host: str):
    return f"""<!doctype html>
                    <html lang="en">
                    <head>
                      <meta charset="utf-8">
                      <title>Bokeh Examples Selector</title>
                    </head>
                    <body>
                      <div>
                        <a  target="_blank" href="{bokeh_host}/examples/bokeh_raw"> Bokeh Basic Example</a><br/>
                        <a  target="_blank" href="{bokeh_host}/examples/bokeh_static"> Bokeh Static Example</a><br/>
                      </div>
                    </body>
                    </html>"""

def initialize_app(server_information: ServerInformation):

    @server_information.flask_app.route(f'/examples/examples_menu', methods=['GET'])
    def examples_menu():
        return generate_examples_page(server_information.get_application_information("bokeh_connection_server"))