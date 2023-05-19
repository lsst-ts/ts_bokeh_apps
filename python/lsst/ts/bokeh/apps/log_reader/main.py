from datetime import date
from typing import TYPE_CHECKING

from bokeh.document import Document
from bokeh.models import CustomJS, DatePicker, TextInput  # type: ignore

if TYPE_CHECKING:
    from typing import Optional  # noqa: F401


class LogViewerApplication:
    def __init__(self, doc: Document) -> None:
        self._doc = doc
        self._date_selector = None  # type: Optional[DatePicker]
        self._sal_index_selector = None  # type: Optional[TextInput]

    def deploy(self) -> None:
        """
        Deploy log viewer application
        """
        sal_index_changed_callback = CustomJS(
            args=dict(),
            code="""
                    sal_index.update(cb_obj.value)
                    """,
        )
        self._sal_index_selector = TextInput(
            name="salindex_selector", styles={"height": "80%", "width": "100%"}
        )
        self._doc.add_root(self._sal_index_selector)
        self._sal_index_selector.js_on_change("value", sal_index_changed_callback)

        date_changed_callback = CustomJS(
            args=dict(),
            code="""
                    select_date(cb_obj.value);
                    """,
        )
        self._date_selector = DatePicker(
            name="date_selector",
            styles={"height": "80%", "width": "100%"},
            value=date.today(),
        )
        self._doc.add_root(self._date_selector)
        self._date_selector.js_on_change("value", date_changed_callback)
