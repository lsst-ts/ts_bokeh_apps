import asyncio
import os
from threading import Thread

from bokeh.document import Document
from bokeh.server.server import Server
from flask import Flask
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler

from lsst_ts.bokeh.apps.log_reader.flask_export import initialize_app
from lsst_ts.bokeh.apps.simple_plot.flask_export import initialize_app as initialize_simple_plot
from lsst_ts.bokeh.apps.plot_selector.flask_export import initialize_app as initialize_plot_selector
from lsst_ts.bokeh.apps.plot_selector_r.flask_export import initialize_app as initialize_react_plot_selector
from lsst_ts.bokeh.main.server_information import ServerInformation
#from lsst_ts.library.data_controller.efd.efd_data_controller import EFDDataController
from lsst_ts.library.data_controller.efd.simulated_data_controller import SimulatedDataController


def initialize_main_app(flask_information: ServerInformation):

    def create_application(doc: Document):
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("templates/index.html")
        doc.template = index_template

    flask_information.add_application("/", create_application)

    return flask_information


def bk_worker(server_information: ServerInformation):
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    static_patterns = [(r'/(.*)', StaticFileHandler, {'path': os.path.normpath(os.path.join(os.path.dirname(__file__), "../apps"))})] #for file in flask_information.static_path
    server = Server(server_information.applications, io_loop=IOLoop(), allow_websocket_origin=server_information.bokeh_allowed_websocket_origin, extra_patterns=static_patterns)
    server.start()
    server.io_loop.start()


def bk_worker_gnunicorn(flask_information: ServerInformation):
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
    bokeh_host = 'localhost'
    bokeh_port = 5006
    flask_host = "0.0.0.0" # All Interfaces
    flask_port = 8000
    app = Flask(__name__)
    CORS(app)
    information = ServerInformation(bokeh_host, bokeh_port, app)
    information.add_applications_information("data_server_host", "127.0.0.1")
    information.add_applications_information("data_server_port", 8000)
    information.add_bokeh_allow_websocket_origin("localhost:5006")
    information.add_bokeh_allow_websocket_origin("172.16.20.8:5006")
    efd_controller = SimulatedDataController()
    # efd_controller =  EFDDataController("usdf_efd")
    initialize_app(information, efd_controller)
    initialize_main_app(information)
    initialize_app(information, efd_controller)
    initialize_simple_plot(information, efd_controller)
    # initialize_plot_selector(information, edf_controller)
    initialize_react_plot_selector(information, efd_controller)
    Thread(target=bk_worker, args=[information]).start()

    # run Flask all hosts and Port 8000
    app.run(host=flask_host, port=flask_port)
