# THIS IS NOT WORKING YET


from threading import Thread

from flask import Flask
from flask_cors import CORS

from lsst_ts.bokeh.apps.log_reader.flask_export import initialize_app
from lsst_ts.bokeh.main.flask_information import FlaskInformation
from lsst_ts.bokeh.main.main_app import initialize_main_app, bk_worker_gnunicorn
from lsst_ts.library.data_controller.edf.simulated_data_controller import SimulatedDataController

if __name__ == '__main__':
    print('This script is intended to be run with gunicorn. e.g.')
    print()
    print('    gunicorn -w 4 flask_gunicorn_embed:app')
    print()
    print('will start the app on four processes')
    import sys
    sys.exit()

server_name = 'localhost'
port = 5006
app = Flask(__name__)
CORS(app)
information = FlaskInformation(server_name, port, app)
edf_controller = SimulatedDataController()
#edf_controller =  SimulatedDataController("usdf_efd")
initialize_app(information, edf_controller)
initialize_main_app(information)
t = Thread(target=bk_worker_gnunicorn, args=[information])
t.daemon = True
t.start()