# This file is part of ts_bokeh_apps.
#
# Developed for the Vera Rubin Observatory Telescope and Site.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import typing
import panel

from ..base_interaction import BaseInteraction
from .layout import Layout
from .helpers import MessageSearcher, add_message, edit_message


class Interaction(BaseInteraction):
    def __init__(self) -> None:
        super().__init__(Layout())

    def setup_interaction(self) -> None:

        self.data_aggregator.dataset = self.select_dataset.value

        self.exposure_flag_buttons[1].on_click(self.set_exposure_flag_none)
        self.exposure_flag_buttons[2].on_click(self.set_exposure_flag_questionable)
        self.exposure_flag_buttons[3].on_click(self.set_exposure_flag_junk)
        self.exposure_flag_buttons[4].on_click(self.deselect)
        self.remove_log_entry_button.on_click(self.handle_remove)

        self.tabulator.param.watch(self.selected, "selection")
        self.text_table.param.watch(self.handle_log, "value")

        self.select_dataset.param.watch(self.handle_dataset, "value")
        self.select_data_id.param.watch(self.handle_data_id, "value")

    @property
    def tabulator(self) -> panel.widgets.Tabulator:
        return self.layout.tabulator

    @property
    def text_table(self) -> panel.widgets.TextInput:
        return self.layout.text_table

    @property
    def exposure_flag_buttons(self) -> typing.List[panel.widgets.Button]:
        return self.layout.exposure_flag_buttons

    @property
    def remove_log_entry_button(self) -> panel.widgets.Button:
        return self.layout.remove_log_entry_button

    @property
    def select_dataset(self) -> panel.widgets.Select:
        return self.layout.select

    @property
    def select_data_id(self) -> panel.widgets.TextInput:
        return self.layout.select_data_id

    @property
    def data_aggregator(self):
        return self.layout.data_aggregator

    def handle_dataset(self, event):
        self.data_aggregator.dataset = self.select_dataset.value

    def handle_data_id(self, event):
        self.data_aggregator.obs_id = self.select_data_id.value
        self.data_aggregator.df = self.data_aggregator.get_data()

    def set_exposure_flag_none(self, event):
        self._set_exposure_flag("none")
        self.reset_selection()

    def set_exposure_flag_questionable(self, event):
        self._set_exposure_flag("questionable")
        self.reset_selection()

    def set_exposure_flag_junk(self, event):
        self._set_exposure_flag("junk")
        self.reset_selection()

    def deselect(self, event):
        self.reset_selection()

    def reset_selection(self):
        self.tabulator.selection = []
        self.text_table.value = ""

    def _set_exposure_flag(self, flag):
        for index in self.tabulator.selection:

            exposure_id = self.tabulator.value["exposure"][index]
            latest_valid_message = MessageSearcher(
                instruments=[
                    self.dataset.lower(),
                ],
                obs_id=exposure_id,
                order_by=["date_added"],
            ).search()[-1:]

            try:
                if len(latest_valid_message) == 0:
                    message = add_message(
                        obs_id=f"{exposure_id}",
                        instrument=self.dataset.lower(),
                        message_text="",
                        exposure_flag=flag,
                        is_new=True,
                    )
                else:
                    message = edit_message(
                        latest_valid_message["id"][0], exposure_flag=flag
                    )
                self.tabulator.patch(
                    {
                        "message_text": [(index, message["message_text"])],
                        "user_id": [(index, message["user_id"])],
                        "user_agent": [(index, message["user_agent"])],
                        "exposure_flag": [(index, message["exposure_flag"])],
                        "id": [(index, message["id"])],
                        "is_human": [(index, message["is_human"])],
                        "is_valid": [(index, message["is_valid"])],
                    }
                )
                self.tabulator.value["id"][index] = message["id"]
            except Exception:
                raise RuntimeError(f"Failed to set flag {flag} for message: {index}.")

    def _is_new(self, index):
        return len(self.tabulator.value["id"][index]) == 0

    def _add_new_log_entry(self, index, message):

        exposure_id = self.tabulator.value["exposure"][index]

        try:
            latest_valid_message = MessageSearcher(
                instruments=[
                    self.dataset.lower(),
                ],
                obs_id=exposure_id,
                order_by=["date_added"],
            ).search()[-1:]

            is_new = len(latest_valid_message) == 0

            if is_new:
                message = add_message(
                    obs_id=f"{exposure_id}",
                    instrument=self.dataset.lower(),
                    message_text=message,
                    is_new=is_new,
                )
            else:
                message = edit_message(
                    message_id=latest_valid_message["id"][0],
                    message_text=message,
                    check_validity=False,
                )
            self.tabulator.patch(
                {
                    "message_text": [(index, message["message_text"])],
                    "user_id": [(index, message["user_id"])],
                    "user_agent": [(index, message["user_agent"])],
                    "exposure_flag": [(index, message["exposure_flag"])],
                    "id": [(index, message["id"])],
                    "is_human": [(index, message["is_human"])],
                    "is_valid": [(index, message["is_valid"])],
                }
            )
            self.tabulator.value["id"][index] = message["id"]
        except Exception:
            raise RuntimeError(
                f"Failed to add message: {exposure_id}, "
                f"{self.dataset.lower()}, {message}, {is_new}."
            )
