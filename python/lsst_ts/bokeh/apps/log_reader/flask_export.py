import os
from datetime import datetime, timedelta
from threading import Thread

import pytz
from bokeh.document import Document
from bokeh.server.server import Server
from flask import Flask, request, jsonify
from jinja2 import FileSystemLoader, Environment
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler

from lsst_ts.bokeh.apps.log_reader.main import LogViewerApplication

__all__ = ['initialize_app']

from lsst_ts.bokeh.main.server_information import ServerInformation
from lsst_ts.library.controllers.efd_log_controller import EfdLogController
from lsst_ts.library.data_controller.efd.data_controller import DataController
from lsst_ts.library.data_controller.efd.efd_data_controller import EFDDataController
from lsst_ts.library.utils.date_interval import DateInterval

_app_route = "log_messages_app"
_messages_data_route = "log_messages"


def initialize_app(server_information: ServerInformation, data_controller: DataController):

    def create_application(doc: Document):
        log_application = LogViewerApplication(doc)
        template_dir = os.path.normpath(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        index_template = env.get_template("templates/index.html")
        doc.title = "Log Reader"
        doc.template_variables["data_server_host"] = server_information.get_application_information("data_server_host")
        doc.template_variables["data_server_port"] = server_information.get_application_information("data_server_port")
        log_application.deploy()
        doc.template = index_template

    server_information.add_application(f"/{_app_route}", create_application)

    @server_information.flask_app.route(f'/{_messages_data_route}', methods=['GET'])
    async def log_messages():
        efd_log_controller = EfdLogController(data_controller)
        max_number_of_elements = request.args.get('n')
        if max_number_of_elements:
            response = await efd_log_controller.get_logs_last_n(int(max_number_of_elements))
            response = [(index,) + tuple(r) for index, r in zip(response.index.to_numpy(), response.to_numpy())]
            return jsonify(response)

        begin_date = datetime.today()
        if request.args.get('begin_date'):
            begin_date = datetime.strptime(request.args.get('begin_date'), '%Y-%m-%d')
            begin_date = begin_date.replace(hour = 12)
            begin_date = pytz.utc.localize(begin_date)
        elif request.args.get('begin_datetime'):
            begin_date = datetime.strptime(request.args.get('begin_datetime'), '%Y-%m-%d %H:%M:%S')

        prev_delta_days = int(request.args.get('prev_delta_days', 0))
        prev_delta_hours = int(request.args.get('prev_delta_days', 12))
        prev_delta = timedelta(days=prev_delta_days, hours=prev_delta_hours)

        post_delta_days = int(request.args.get('post_delta_days', 0))
        post_delta_hours = int(request.args.get('post_delta_days', 12))
        post_delta = timedelta(days=post_delta_days, hours=post_delta_hours)
        date_interval = DateInterval.from_central_date(begin_date, prev_delta, post_delta)
        response = await efd_log_controller.get_logs_by_interval(date_interval)
        response = [(index,)  + tuple(r) for index, r in zip(response.index.to_numpy(), response.to_numpy())]
        return jsonify(response)

    return server_information


def bk_worker(server_information: ServerInformation):
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server(server_information.applications, io_loop=IOLoop(), allow_websocket_origin=server_information.bokeh_allowed_websocket_origin(),
                    extra_patterns=[
                        (r'/(.*)', StaticFileHandler, {'path':os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))})],
                    )
    server.start()
    server.io_loop.start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    server_name = 'localhost'
    port = 5006
    app = Flask(__name__)
    information = ServerInformation(server_name, port, app)
    efd_controller = EFDDataController("usdf_efd")
    initialize_app(information, efd_controller)
    Thread(target=bk_worker, args=[information]).start()
    app.run(port=8000)
