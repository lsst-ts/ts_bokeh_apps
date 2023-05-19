# THIS IS NOT WORKING YET


from threading import Thread

from flask import Flask
from flask_cors import CORS
from lsst.bokeh.apps.log_reader.export import initialize_app
from lsst.ts.bokeh.main.main_app import (bk_worker_gnunicorn,
                                         initialize_main_app)
from lsst.ts.bokeh.main.server_information import ServerInformation
from lsst.ts.library.data_controller.efd.simulated_data_controller import \
    SimulatedDataController

if __name__ == "__main__":
    print("This script is intended to be run with gunicorn. e.g.")
    print()
    print("    gunicorn -w 4 flask_gunicorn_embed:app")
    print()
    print("will start the app on four processes")
    import sys

    sys.exit()

server_name = "localhost"
port = 5006
app = Flask(__name__)
CORS(app)
information = ServerInformation(app)
efd_controller = SimulatedDataController()
# efd_controller =  SimulatedDataController("usdf_efd")
initialize_app(information)
initialize_main_app(information)
t = Thread(target=bk_worker_gnunicorn, args=[information])
t.daemon = True
t.start()
