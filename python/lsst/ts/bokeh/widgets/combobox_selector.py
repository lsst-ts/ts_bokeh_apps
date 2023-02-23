from typing import List, Tuple

from bokeh.io import show
from bokeh.layouts import row
from bokeh.models import Select, LayoutDOM

from lsst.ts.library.pub_sub.observable import Observable


class ComboboxSelector(Observable[str]):
    """
    A Combobox to select one in a series of str values.
    """
    _FIRST_INDEX_TEXT = "Select a valid SalIndex"
    def __init__(self, name: str = "combobox_selector", options: List[Tuple[str, str]] = []):
        super(ComboboxSelector, self).__init__()
        self._dropdown = None
        self._name = name
        self._options = options[:]

    def create(self) -> LayoutDOM:
        """
        Create the widget and return it to be placed in the doc
        :return: LayoutDOM
        """
        self._dropdown = Select(options = self._options)
        self._dropdown.on_change("value", self._selection_changed)
        self._set_first_value()
        return row(self._dropdown, name=self._name)

    def update(self, options: List[str]) -> None:
        """
        :param options: List of str options to be shown in the combobox
        """
        self._options = options[:]
        self._dropdown.options = self._options
        self._set_first_value()

    def _set_first_value(self):
        if not len(self._dropdown.options):
            self._dropdown.options = ["No values Available"]
            self._dropdown.disabled = True
        else:
            self._dropdown.options.insert(0, "Select a valid SalIndex")
            self._dropdown.disabled = False

    def _selection_changed(self, attr, old, new) -> None:
        self._notify(new)


if __name__ == '__main__':
    integer_selector = ComboboxSelector(options = ["foo", "bar", "baz", "quux"])
    show(integer_selector.create())