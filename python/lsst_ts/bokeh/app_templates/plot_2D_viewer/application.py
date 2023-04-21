import os

from flask import Blueprint, render_template
from jinja2 import FileSystemLoader, Environment

from lsst_ts.bokeh.main import server_information
from lsst_ts.bokeh.main.server_information import ServerInformation


# Application name
# Data to be shown

def change_name(function_name):
    def decorator(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        inner.__name__ = function_name
        return inner
    return decorator


class Plot2DApplication:

    def __init__(self, svr_information: ServerInformation, identifier: str):
        self._identifier = identifier
        self._server_information = svr_information

    def deploy(self):
        application_blueprint = Blueprint(f'plot2dapp_blueprint_{self._identifier}',
                                                  __name__,
                                                  url_prefix=f"/plot_2D_viewer/{self._identifier}",
                                                  static_folder="static",
                                                  static_url_path="/plot_2D_viewer/static")

        @application_blueprint.route("/", methods=['GET'])
        @change_name(function_name = self._identifier)
        def plot_selector():
            template_dir = os.path.normpath(os.path.dirname(__file__))
            env = Environment(loader=FileSystemLoader([template_dir, os.path.join(template_dir, "../templates")]))
            #env.get_template("templates/base.html")
            index_template = env.get_template("templates/index.html")
            return render_template(index_template)

        self._server_information.flask_app.register_blueprint(application_blueprint)
        return server_information
