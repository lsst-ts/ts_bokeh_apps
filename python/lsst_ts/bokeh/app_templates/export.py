from flask import Blueprint

from lsst_ts.bokeh.main.server_information import ServerInformation


def initialize_apps(server_information: ServerInformation):
    application_blueprint = Blueprint("/app_templates",
                                      __name__,
                                      url_prefix="/app_templates",
                                      static_folder="static",
                                      static_url_path="/static")


    server_information.flask_app.register_blueprint(application_blueprint)
    return server_information