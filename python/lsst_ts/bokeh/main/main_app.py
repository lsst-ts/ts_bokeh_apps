import os
import sys
from typing import Dict, Union

import yaml

from threading import Thread

from bokeh.document import Document
from bokeh.server.server import Server
from flask import Flask
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler

from lsst_ts.bokeh.apps.examples.export import initialize_app as initialize_examples
from lsst_ts.bokeh.apps.log_reader.export import initialize_app
from lsst_ts.bokeh.apps.plot_selector_r.export import initialize_app as initialize_react_plot_selector
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
    print(server_information.applications)
    print(os.path.normpath(os.path.join(os.path.dirname(__file__), "../apps/examples")))
    static_patterns = [(r'/examples_appexample_static_folder/(.*)', StaticFileHandler, {'path': os.path.normpath(os.path.join(os.path.dirname(__file__),
                                                                                                                              "../apps/examples"))}),
                        (r'/(.*)', StaticFileHandler, {'path': os.path.normpath(os.path.join(os.path.dirname(__file__), "../apps"))})] #for file in flask_information.static_path
    server = Server(server_information.applications, io_loop=IOLoop(),
                                                    port=server_information.get_application_information("bokeh_server_port"),
                                                    allow_websocket_origin=server_information.allowed_websocket_origin,
                                                    extra_patterns=static_patterns)
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

class Configuration:

    def __init__(self, configuration: Dict[str: Union[int, str]]):
        self._configuration = configuration
    @staticmethod
    def from_yaml(config_file):
        if not os.path.isfile(config_file):
            raise Exception(f"Configuration file: {config_file} not found")

        with open(config_file, 'r') as f:
            conf = yaml.load(f)
        return Configuration(conf)
    def get_bokeh_server_host(self):
        return self._configuration["server"]["bokeh"]["host"]
    def get_bokeh_server_port(self):
        return self._configuration["server"]["bokeh"]["port"]
    def get_flask_server_host(self):
        return self._configuration["server"]["flask"]["host"]
    def get_flask_server_port(self):
        return self._configuration["server"]["flask"]["port"]

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    configuration_file = sys.argv[1]
    configuration = Configuration.from_yaml(configuration_file)


    bokeh_host = configuration.get_bokeh_server_host()
    bokeh_port = configuration.get_bokeh_server_port()
    flask_host = configuration.get_flask_server_host()
    flask_port = configuration.get_flask_server_port()

    flask_app = Flask(__name__)
    CORS(flask_app)
    information = ServerInformation(flask_app)
    # Host where server will be running, only valid localhost or 127.0.0.1 if
    # client will be running in the same computer as the server (very unlikely, but for test purposes is the case)
    information.add_application_information("data_server_host", flask_host)
    information.add_application_information("data_server_port", flask_port)
    information.add_application_information("bokeh_server_host", bokeh_host)
    information.add_application_information("bokeh_server_port", bokeh_port)

    information.add_allowed_websocket_origin("localhost:5006")
    information.add_allowed_websocket_origin("172.16.20.8:5006")
    efd_controller = SimulatedDataController()
    # efd_controller =  EFDDataController("usd_efd")
    # initialize_main_app(information)
    # initialize_app(information)
    # initialize_simple_plot(information)
    # initialize_examples(information)
    # initialize_plot_selector(information)
    # initialize_interactive_example(information)
    initialize_react_plot_selector(information)
    Thread(target=bk_worker, args=[information]).start()

    # run Flask all hosts
    flask_app.run(host=flask_host, port=flask_port)
