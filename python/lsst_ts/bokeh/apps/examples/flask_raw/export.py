from lsst_ts.bokeh.main.server_information import ServerInformation


def generate_examples_page(bokeh_host: str) -> str:
    return f"""<!doctype html>
                    <html lang="en">
                    <head>
                      <meta charset="utf-8">
                      <title>Bokeh Examples Selector</title>
                    </head>
                    <body>
                      <div>
                        <a  target="_blank"
                        href="{bokeh_host}/examples/bokeh_raw"> Bokeh Basic Example</a><br/>
                        <a  target="_blank"
                        href="{bokeh_host}/examples/bokeh_static"> Bokeh Static Example</a><br/>
                      </div>
                    </body>
                    </html>"""


def initialize_app(server_information: ServerInformation) -> ServerInformation:
    @server_information.flask_app.route("/examples/examples_menu", methods=["GET"])  # type: ignore
    def examples_menu():
        return generate_examples_page(
            str(
                server_information.get_application_information(
                    "bokeh_connection_server"
                )
            )
        )

    return server_information
