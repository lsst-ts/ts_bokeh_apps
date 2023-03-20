import asyncio
import os
from threading import Thread

from bokeh.document import Document
from bokeh.server.server import Server, BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from flask import Flask
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler

from lsst_ts.bokeh.apps.log_reader.flask_export import initialize_app
from lsst_ts.bokeh.main.flask_information import FlaskInformation
from lsst_ts.library.data_controller.edf.simulated_data_controller import SimulatedDataController


def initialize_main_app(flask_information: FlaskInformation):

    def create_application(doc: Document):
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("templates/index.html")
        doc.template = index_template

    flask_information.add_application("/", create_application)

    return flask_information


def bk_worker(flask_information: FlaskInformation):
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    static_patterns = [(r'/(.*)', StaticFileHandler, {'path': os.path.normpath(os.path.join(os.path.dirname(__file__), "../apps"))})] #for file in flask_information.static_path
    server = Server(flask_information.applications, io_loop=IOLoop(), extra_patterns=static_patterns)
    server.start()
    server.io_loop.start()


def bk_worker_gnunicorn(flask_information: FlaskInformation):
    # This is not working yet
    pass
#     static_patterns = [(r'/(.*)', StaticFileHandler, {'path': os.path.normpath(os.path.join(os.path.dirname(__file__), "../apps"))})] #for file in flask_information.static_path
#     sockets, port = bind_sockets("localhost", 0)
#     print(port)
#     asyncio.set_event_loop(asyncio.new_event_loop())
#
#     print(flask_information.applications)
#     bokeh_tornado = BokehTornado(flask_information.applications,  extra_websocket_origins=["localhost:8000"], allow_websocket_origin=["localhost:8000"], extra_patterns=static_patterns)
#     bokeh_http = HTTPServer(bokeh_tornado)
#     bokeh_http.add_sockets(sockets)
#
#     server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
#     server.start()
#     server.io_loop.start()


if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    server_name = 'localhost'
    port = 5006
    app = Flask(__name__)
    CORS(app)
    information = FlaskInformation(server_name, port, app)
    edf_controller = SimulatedDataController()
    #edf_controller =  SimulatedDataController("usdf_efd")
    initialize_app(information, edf_controller)
    initialize_main_app(information)
    Thread(target=bk_worker, args=[information]).start()
    app.run(port=8000)
