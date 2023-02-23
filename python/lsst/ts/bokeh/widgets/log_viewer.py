from typing import List, Tuple

from bokeh.core.enums import SizingPolicy
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import CustomJS, Div, Toggle, Widget, LayoutDOM

from lsst.ts.library.utils.exception_parser import parse_exceptions_text, ExceptionRelation

class ExceptionInformationWidget:

    _relation_factory={ExceptionRelation.END: "",
                       ExceptionRelation.DIRECT_CAUSE: "The above exception was the direct cause of the following exception:",
                       ExceptionRelation.SIDE_CAUSE: "During handling of the above exception, another exception occurred:"}

    def __init__(self, exception: str, stacktrace: List[str], relation: int):
        self._relation_div = None
        self._stacktrace_div = None
        self._show_info_button = None
        self._exception = exception
        self._child_relation = relation
        self._stacktrace = "<br/>".join(stacktrace)

    def create(self) -> List[Widget]:
        """
        Create the widget and return it to be placed in the doc
        :return: LayoutDOM
        """
        self._stacktrace_div = Div(text=self._stacktrace, visible=False)
        self._relation_div = Div(text=ExceptionInformationWidget._relation_factory[self._child_relation], style={"color": "red"})
        self._show_info_button = Toggle(label=self._exception, width_policy=SizingPolicy.max);
        self._set_callback()
        return [self._show_info_button, self._stacktrace_div, self._relation_div]

    def _set_callback(self):
        callback = CustomJS(args=dict(button=self._show_info_button, stacktrace=self._stacktrace_div), code=""" 
                                if(button.active)
                                    stacktrace.visible = true;
                                else stacktrace.visible = false;
                                """)
        self._show_info_button.js_on_click(callback)


class LogViewer:
    """
    """
    def __init__(self, name = "exception_viewer"):
        self._no_information_label = None
        self._show_information = None
        self._name = name

    def create(self) -> LayoutDOM:
        """
        Create the widget and return it to be placed in the doc
        :return: LayoutDOM
        """
        self._no_information_label = Div(name = "no_information_lbl", text = "PLEASE SELECT A CORRECT <BR/> SALINDEX TO SHOW INFORMATION", style={'text-align': 'center', 'width': '100%'})
        self._show_information = column(children = [self._no_information_label], name = self._name, width_policy=SizingPolicy.max)
        return self._show_information

    def update(self, log_information: str) -> None:
        """
        Update the information shown by the widget, in case log_information is a widget it will be parsed and formed using ExceptionInformationWidget
        :param log_information: Information to be shown
        """
        self._clear()
        if LogViewer._is_exception(log_information):
            self._parse_exception(log_information)
        else:
            div_info = Div(text=log_information)
            self._show_information.children.append(div_info)

    def set_no_data_available(self) -> None:
        """
        Set information for empty salindex log information
        """
        self._clear()
        no_information_label = Div(name="no_information_lbl",
                                         text="NO VALID SALINDEX",
                                         style={'text-align': 'center', 'width': '100%'})
        self._show_information.children.append(no_information_label)

    def _clear(self):
        for _ in list(self._show_information.children):
            widget = self._show_information.children.pop()
            widget.destroy()

    def _parse_exception(self, stacktrace: str):
        root = parse_exceptions_text(stacktrace)
        for exception_values in root:
            exception_information = ExceptionInformationWidget(exception_values.type, exception_values.stacktrace, exception_values.relation)
            widgets = exception_information.create()
            self._show_information.children.append(widgets[0])
            self._show_information.children.append(widgets[1])
            self._show_information.children.append(widgets[2])

    @classmethod
    def _is_exception(cls, information: str) -> bool:
        if 'Traceback' in information:
            return True
        return False


# Just to have a first view of the object
if __name__ == '__main__':
    date_selector = LogViewer()
    show(date_selector.create())
