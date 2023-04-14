import json
import os

from flask import Flask, jsonify, render_template, Blueprint
from jinja2 import Template, Environment, FileSystemLoader
import math

from bokeh.plotting import figure
from bokeh.models import AjaxDataSource
from bokeh.embed import json_item

from lsst_ts.bokeh.main.server_information import ServerInformation

app = Flask(__name__)

x, y = 0, 0

def initialize_app(server_information: ServerInformation):

    flask_embedding_full_example_blueprint = Blueprint('flask_embedding_full_example_blueprint',
                                                  __name__,
                                                  url_prefix="/examples/flask_bokeh_full",
                                                  static_folder="static",
                                                  static_url_path='/examples/flask_bokeh_full/static')

    @flask_embedding_full_example_blueprint.route("/", methods=['GET'])
    def flask_bokeh_full_component():
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("templates/index.html")
        return render_template(index_template)


    @flask_embedding_full_example_blueprint.route("/widget", methods=['GET'])
    def flask_bokeh_full__widget():
        #streaming = True
        host = server_information.get_application_information("data_server_host")
        port = server_information.get_application_information("data_server_port")
        source = AjaxDataSource(data_url=f'http://{host}:{port}/examples/flask_bokeh_full/data',
                                polling_interval=1000, mode='append')

        source.data = dict(x=[], y=[])

        fig = figure(title="Sinus Data", styles={"height": "800px", "width": "100%"})
        fig.line('x', 'y', source=source)

        return json.dumps(json_item(fig))

    @flask_embedding_full_example_blueprint.route('/data', methods=['POST'])
    async def flask_bokeh_full_data():
        global x, y
        x = x + 0.1
        y = math.sin(x)
        return jsonify(x=[x], y=[y])

    server_information.flask_app.register_blueprint(flask_embedding_full_example_blueprint)
    return server_information
