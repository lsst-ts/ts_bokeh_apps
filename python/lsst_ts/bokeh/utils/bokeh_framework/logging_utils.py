import logging

from logging import StreamHandler

from bokeh.models import Paragraph

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bokeh.models import Markup


class ErrorViewer(StreamHandler):

    _FORMATTER = '%(asctime)s %(message)s'
    def __init__(self):
        StreamHandler.__init__(self)
        self.setFormatter(logging.Formatter(ErrorViewer._FORMATTER))
        self.setLevel(logging.ERROR)
        self._label = Paragraph(text="NO ERROR")

    def reset(self):
        self._label.style = {'color': 'black'}
        self._label.text = "NO ERROR" # typing: Label

    @property
    def widget(self) -> 'Markup':
        return self._label

    def emit(self, record: logging.LogRecord):
        self._label.style = {'color': 'red'}
        self._label.text = f"Error message: {record.message}"