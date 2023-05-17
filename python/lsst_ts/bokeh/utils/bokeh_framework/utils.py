from bokeh.models import Markup

from lsst_ts.bokeh.utils.bokeh_framework.logging_utils import ErrorViewer
from lsst_ts.library.utils.logger import add_custom_handler


class CustomWidgets:

    @staticmethod
    def create_exception_viewer() -> Markup:
        error_viewer = ErrorViewer()
        add_custom_handler(error_viewer)
        return error_viewer.widget
