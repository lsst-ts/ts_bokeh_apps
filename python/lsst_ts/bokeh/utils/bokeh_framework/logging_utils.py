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
        self.setLevel(logging.ERROR)
        self._label = Paragraph() # typing: Label

    @property
    def widget(self) -> 'Markup':
        return self._label

    def emit(self, record: logging.LogRecord):
        self._label.text = record.message