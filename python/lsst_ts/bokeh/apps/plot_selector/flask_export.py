import json
import os

from bokeh.embed import json_item
from bokeh.plotting import figure
from flask import render_template, Blueprint
from jinja2 import Template, Environment, FileSystemLoader

from lsst_ts.bokeh.main.server_information import ServerInformation
from lsst_ts.library.data_controller.efd.data_controller import DataController

def initialize_app(server_information: ServerInformation, data_controller: DataController):
    plot_selector_blueprint = Blueprint('plot_selector_blueprint', __name__, url_prefix="/plot_selector", static_folder="static", static_url_path='/plot_selector/static')
    @plot_selector_blueprint.route("/", methods=['GET'])
    def plot_selector():
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("templates/index.html")
        return render_template(index_template)

    @plot_selector_blueprint.route("/<variable_to_plot>", methods=['GET'])
    def plot_selector_variable(variable_to_plot):
        p = figure(styles={"height": "400px"})
        p.sizing_mode = 'scale_width'
        p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
        return json.dumps(json_item(p))

    server_information.flask_app.register_blueprint(plot_selector_blueprint)

    return server_information
