import os

from flask import Flask, render_template, Blueprint
from jinja2 import Environment, FileSystemLoader

from lsst_ts.bokeh.main.server_information import ServerInformation
from lsst_ts.library.data_controller.edf.data_controller import DataController

app = Flask(__name__)

def initialize_app(server_information: ServerInformation, data_controller: DataController):
    plot_selector_react_blueprint = Blueprint('plot_selector_react_blueprint', __name__, url_prefix="/plot_selector",
                                        static_folder="plot_select_app/build/static", static_url_path="/plot_select_app/build/static")

    @plot_selector_react_blueprint.route("/", methods=['GET'])
    def plot_selector_react():
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("plot_select_app/build/index.html")
        return render_template(index_template)

    server_information.flask_app.register_blueprint(plot_selector_react_blueprint)

    return server_information
