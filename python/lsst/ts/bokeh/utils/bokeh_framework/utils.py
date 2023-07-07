from typing import TYPE_CHECKING

from lsst.ts.bokeh.utils.bokeh_framework.logging_utils import ErrorViewer
from lsst.ts.library.utils.logger import add_custom_handler

if TYPE_CHECKING:
    from bokeh.models import Markup


class CustomWidgets:
    _CUSTOM_WIDGETS = None  # typing: Optional[CustomWidgets]

    @staticmethod
    def get_custom_widgets() -> "CustomWidgets":
        if CustomWidgets._CUSTOM_WIDGETS is None:
            CustomWidgets._CUSTOM_WIDGETS = CustomWidgets()
        return CustomWidgets._CUSTOM_WIDGETS

    def __init__(self):
        self._error_viewer = None  # typing: Optional[Markup]

    def get_exception_viewer(self) -> "Markup":
        if self._error_viewer is not None:
            return self._error_viewer
        self._error_viewer = ErrorViewer()
        add_custom_handler(self._error_viewer)
        return self._error_viewer.widget

    def reset(self):
        if self._error_viewer is not None:
            self._error_viewer.reset()
