from bokeh.models import Markup

from lsst_ts.bokeh.utils.bokeh_framework.logging_utils import ErrorViewer
from lsst_ts.library.utils.logger import add_custom_handler

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bokeh.models import Markup

class CustomWidgets:

    @staticmethod
    def create_exception_viewer() -> Markup:
        error_viewer = ErrorViewer()
        add_custom_handler(error_viewer)
        return error_viewer.widget
