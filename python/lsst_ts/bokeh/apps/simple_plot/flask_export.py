import json
import os

from flask import Flask, jsonify, render_template
from jinja2 import Template, Environment, FileSystemLoader
import math

from bokeh.plotting import figure
from bokeh.models import AjaxDataSource
from bokeh.embed import components, json_item
from bokeh.resources import INLINE

from lsst_ts.bokeh.main.server_information import ServerInformation
from lsst_ts.library.data_controller.edf.data_controller import DataController

app = Flask(__name__)

x, y = 0, 0

template = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Streaming Example</title>
        {{ js_resources }}
        {{ css_resources }}
    </head>
    <body>
    {{ plot_div }}
    {{ plot_script }}
    </body>
</html>
''')

def initialize_app(server_information: ServerInformation, data_controller: DataController):

    @server_information.flask_app.route("/simple_widget", methods=['GET'])
    def simple_app():
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("templates/index.html")
        return render_template(index_template)



    @server_information.flask_app.route("/widget", methods=['GET'])
    def widget():
        streaming = True
        source = AjaxDataSource(data_url="http://localhost:8000/data",
                                polling_interval=1000, mode='append')

        source.data = dict(x=[], y=[])

        fig = figure(title="Streaming Example")
        fig.line('x', 'y', source=source)

        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()

        return json.dumps(json_item(fig))
        #script, div = components(fig, INLINE)
        #print(script, div)
        #return jsonify((script, div))
        #
        # html = template.render(
        #     plot_script=script,
        #     plot_div=div,
        #     js_resources=js_resources,
        #     css_resources=css_resources
        # )
        # return html

    @server_information.flask_app.route('/data', methods=['POST'])
    async def data():
        global x, y
        x = x + 0.1
        y = math.sin(x)
        return jsonify(x=[x], y=[y])


    return server_information
