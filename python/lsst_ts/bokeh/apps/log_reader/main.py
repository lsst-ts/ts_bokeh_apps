from datetime import date, timedelta, datetime
from typing import Union

from bokeh import plotting # type: ignore
from bokeh.models import CustomJS, TextInput, DatePicker


class LogViewerApplication:

    def __init__(self, doc):
        self._date_selector = None
        self._doc = doc
        self._sal_index_selector = None

    def deploy(self) -> None:
        """
        Deploy log viewer application
        """
        sal_index_changed_callback = CustomJS(args=dict(), code="""
                    sal_index.update(cb_obj.value)
                    """)
        self._sal_index_selector = TextInput(name = "salindex_selector", styles={"height": "80%","width": "100%"})
        self._doc.add_root(self._sal_index_selector)
        self._sal_index_selector.js_on_change("value", sal_index_changed_callback)

        date_changed_callback = CustomJS(args=dict(), code="""
                    select_date(cb_obj.value);         
                    """)
        self._date_selector = DatePicker(name = "date_selector", styles={"height": "80%","width": "100%"}, value=date.today())
        self._doc.add_root(self._date_selector)
        self._date_selector.js_on_change("value", date_changed_callback)

if __name__.startswith("bokeh_app_"):
    print(f"name: {0}".format(__name__))
    app = LogViewerApplication()
    app.deploy()
    app.initialize()

if __name__ == '__main__':
    widget = LogViewerApplication()
    widget.deploy()
    widget.initialize()
