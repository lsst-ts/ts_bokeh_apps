from typing import TYPE_CHECKING

from bokeh.io import show
from bokeh.models import Row, Select  # type: ignore

if TYPE_CHECKING:
    from typing import TYPE_CHECKING, Any, List, Tuple

    from bokeh.models.ui.ui_element import UIElement
    from lsst_ts.library.pub_sub.observable import Observable  # noqa: F401


class ComboboxSelector("Observable[str]"):
    """
    A Combobox to select one in a series of str values.
    """

    _FIRST_INDEX_TEXT = "Select a valid SalIndex"

    def __init__(
        self, name: str = "combobox_selector", options: "List[Tuple[str]]" = []
    ) -> None:
        super().__init__()
        self._dropdown = Select()  # type: Select
        self._name = name
        self._options = options[:]

    def create(self) -> "UIElement":
        """
        Create the widget and return it to be placed in the doc
        :return: UIElement
        """
        self._dropdown = Select(options=self._options)
        self._dropdown.on_change("value", self._selection_changed)
        self._set_first_value()
        return Row(children=[self._dropdown], name=self._name)

    def update(self, options: "List[Tuple[str]]") -> None:
        """
        :param options: List of str options to be shown in the combobox
        """
        self._options = options[:]
        self._dropdown.options = self._options
        self._set_first_value()

    def _set_first_value(self) -> None:
        if not len(self._dropdown.options):
            self._dropdown.options = ["No values Available"]
            self._dropdown.disabled = True
        else:
            self._dropdown.options.insert(0, "Select a valid SalIndex")
            self._dropdown.disabled = False

    def _selection_changed(self, attr: Any, old: Any, new: Any) -> None:
        self._notify(new)


if __name__ == "__main__":
    integer_selector = ComboboxSelector(
        options=[("foo",), ("bar",), ("baz",), ("quux",)]
    )
    show(integer_selector.create())
