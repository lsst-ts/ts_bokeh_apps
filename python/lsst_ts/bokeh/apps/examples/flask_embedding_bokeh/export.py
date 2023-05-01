import json
import os

from bokeh.embed import json_item
from bokeh.plotting import figure
from flask import render_template, Blueprint
from jinja2 import Environment, FileSystemLoader

from lsst_ts.bokeh.main.server_information import ServerInformation


def initialize_app(server_information: ServerInformation) -> ServerInformation:
    flask_embedding_example_blueprint = Blueprint('flask_embedding_example_blueprint',
                                                  __name__,
                                                  url_prefix="/examples/flask_embedding_bokeh_example",
                                                  static_folder="static",
                                                  static_url_path='/examples/flask_embedding_bokeh_example/'
                                                                  'static')

    @flask_embedding_example_blueprint.route("/", methods=['GET'])  # type: ignore
    def plot_selector():
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("templates/index.html")
        return render_template(index_template)

    @flask_embedding_example_blueprint.route("/<variable_to_plot>", methods=['GET'])  # type: ignore
    def plot_selector_variable(variable_to_plot):
        p = figure(styles={"height": "800px", "width": "100%"})
        # p.sizing_mode = 'scale_both'
        p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
        return json.dumps(json_item(p))

    server_information.flask_app.register_blueprint(flask_embedding_example_blueprint)

    return server_information
