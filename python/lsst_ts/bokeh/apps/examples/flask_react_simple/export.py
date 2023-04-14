import os

from flask import Flask, render_template, Blueprint
from jinja2 import Environment, FileSystemLoader

from lsst_ts.bokeh.main.server_information import ServerInformation

app = Flask(__name__)

def initialize_app(server_information: ServerInformation):
    flask_react_simple_blueprint = Blueprint('flask_react_simple_blueprint', __name__, url_prefix="/examples/flask_react_simple",
                                        static_folder="flask_react_simple_app/build/static", static_url_path="/flask_react_simple_app/build/static")

    @flask_react_simple_blueprint.route("/", methods=['GET'])
    def flask_react_simple():
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("flask_react_simple_app/build/index.html")
        print(index_template)
        return render_template(index_template)

    server_information.flask_app.register_blueprint(flask_react_simple_blueprint)

    return server_information
