import os

from flask import Blueprint, Flask, render_template
from jinja2 import Environment, FileSystemLoader
from lsst.ts.bokeh.main.server_information import ServerInformation

app = Flask(__name__)


def initialize_app(server_information: ServerInformation) -> ServerInformation:
    plot_selector_react_blueprint = Blueprint(
        "plot_selector_react_blueprint",
        __name__,
        url_prefix="/plot_selector",
        static_folder="plot_select_app/build/static",
        static_url_path="/plot_select_app/build/static",
    )

    @plot_selector_react_blueprint.route("/", methods=["GET"])
    def plot_selector_react() -> str:
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("plot_select_app/build/index.html")
        return render_template(index_template)

    server_information.flask_app.register_blueprint(plot_selector_react_blueprint)

    return server_information
