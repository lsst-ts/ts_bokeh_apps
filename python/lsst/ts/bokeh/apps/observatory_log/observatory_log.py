import pandas as pd
import panel as pn

from bokeh.models.widgets.tables import NumberFormatter

import lsst.daf.butler as dafButler

from .helpers import (
    add_message,
    get_messages,
    edit_message,
    delete_message,
)

__all__ = ["ObservatoryLog"]


class ObservatoryLog:
    def __init__(self, dataset, obs_id):

        self.dataset = dataset
        self.obs_id = obs_id

        self.df = self.get_data()
        tabulator_formatters = {
            "exposure": NumberFormatter(format="0"),
        }

        self.tabulator = pn.widgets.Tabulator(
            self.df, layout="fit_data_fill", height=450, formatters=tabulator_formatters
        )
        self.tabulator.hidden_columns = [
            "id",
            "is_human",
            "is_valid",
            "instrument_x",
            "user_agent",
        ]

        self.cb = pn.state.add_periodic_callback(self.stream, 10000)
        self.text_table = pn.widgets.TextInput(
            name="Log:", placeholder="Enter a string here..."
        )

        self.exposure_flag_buttons = (
            "## Exposure flags: ",
            pn.widgets.Button(
                name="none",
                button_type="success",
                width=50,
                max_width=100,
                width_policy="fixed",
            ),
            pn.widgets.Button(
                name="questionable",
                button_type="warning",
                width=50,
                max_width=100,
                width_policy="fixed",
            ),
            pn.widgets.Button(
                name="junk",
                button_type="danger",
                width=50,
                max_width=100,
                width_policy="fixed",
            ),
        )
        self.exposure_flag_buttons[1].on_click(self.set_exposure_flag_none)
        self.exposure_flag_buttons[2].on_click(self.set_exposure_flag_questionable)
        self.exposure_flag_buttons[3].on_click(self.set_exposure_flag_junk)

        self.remove_log_entry_button = pn.widgets.Button(
            name="Remove", width=50, max_width=100, width_policy="fixed"
        )
        self.remove_log_entry_button.on_click(self.handle_remove)

        self.disable_buttons()

        self.tabulator.param.watch(self.selected, "selection")
        self.text_table.param.watch(self.handle_log, "value")

    def set_exposure_flag_none(self, event):
        self._handle_all_selected_have_log_entry()
        self._set_exposure_flag("none")
        self.reset_selection()

    def set_exposure_flag_questionable(self, event):
        self._handle_all_selected_have_log_entry()
        self._set_exposure_flag("questionable")
        self.reset_selection()

    def set_exposure_flag_junk(self, event):
        self._handle_all_selected_have_log_entry()
        self._set_exposure_flag("junk")
        self.reset_selection()

    def _handle_all_selected_have_log_entry(self):

        for index in self.tabulator.selection:
            if self._is_new(index):
                self._add_new_log_entry(index=index, message="")

    def _set_exposure_flag(self, flag):
        for index in self.tabulator.selection:
            message_id = self.tabulator.value["id"][index]
            try:
                message = edit_message(message_id, exposure_flag=flag)
                self.tabulator.patch(
                    {
                        "exposure_flag": [(index, flag)],
                    }
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
                    f"Failed to set flag {flag} for message: {message_id}."
                )

    def _is_new(self, index):
        return len(self.tabulator.value["id"][index]) == 0

    def _add_new_log_entry(self, index, message):

        exposure_id = self.tabulator.value["exposure"][index]
        message_id = self.tabulator.value["id"][index]

        try:
            is_new = self._is_new(index)
            if is_new:
                message = add_message(
                    obs_id=f"{exposure_id}",
                    instrument=self.dataset.lower(),
                    message_text=message,
                    is_new=is_new,
                )
            else:
                message = edit_message(
                    message_id=message_id,
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
                f"Failed to add message: {exposure_id}, {self.dataset.lower()}, {message}, {is_new}."
            )

    def disable_buttons(self):
        self.exposure_flag_buttons[1].disabled = True
        self.exposure_flag_buttons[2].disabled = True
        self.exposure_flag_buttons[3].disabled = True
        self.remove_log_entry_button.disabled = True
        self.text_table.disabled = True

    def enable_buttons(self):
        self.exposure_flag_buttons[1].disabled = False
        self.exposure_flag_buttons[2].disabled = False
        self.exposure_flag_buttons[3].disabled = False
        self.remove_log_entry_button.disabled = False
        self.text_table.disabled = False

    def get_data(self):

        butler = dafButler.Butler(f"/repo/{self.dataset}/")

        exposures = pd.DataFrame(
            record.toDict()
            for record in butler.registry.queryDimensionRecords(
                "exposure",
                where=f"instrument = '{self.dataset}' and exposure > {self.obs_id}",
            )
        )

        if len(exposures) == 0:
            return None

        valid_messages = get_messages()
        exposures["id"] = exposures["id"].astype(int)
        valid_messages["obs_id"] = valid_messages["obs_id"].astype(int)

        self.obs_id = exposures["id"].max()

        data = (
            pd.merge(
                left=exposures,
                right=valid_messages,
                how="left",
                left_on="id",
                right_on="obs_id",
            )
            .fillna("")
            .get(
                [
                    "instrument_x",
                    "user_id",
                    "user_agent",
                    "is_human",
                    "is_valid",
                    "exposure_flag",
                    "message_text",
                    "id_y",
                    "physical_filter",
                    "exposure_time",
                    "observation_type",
                    "observation_reason",
                    "target_name",
                    "science_program",
                ]
            )
        )
        data["exposure"] = exposures["id"]
        data["id"] = data["id_y"]

        return data.get(
            [
                "instrument_x",
                "exposure",
                "physical_filter",
                "exposure_time",
                "observation_type",
                "target_name",
                "science_program",
                "user_id",
                "user_agent",
                "is_human",
                "is_valid",
                "exposure_flag",
                "id",
                "message_text",
            ]
        )

    def stream(self):
        try:
            data = self.get_data()
            if data is not None:
                self.tabulator.stream(data, follow=self.follow.value)
        except Exception as e:
            print(f"Error: {e}")

    def selected(self, event):
        if len(event.obj.selection) == 0:
            self.text_table.placeholder = "Enter a log here..."
            self.remove_log_entry_button.disabled = True
            self.disable_buttons()
        else:
            exposure = ",".join(
                [
                    f"{event.obj.value['exposure'][index]}"
                    for index in event.obj.selection
                ]
            )
            self.text_table.placeholder = (
                f"Enter log for exposure {exposure} here. Press <enter> to apply."
            )
            self.enable_buttons()

    def handle_log(self, event):
        if not event.obj.value:
            return

        for index in self.tabulator.selection:
            self._add_new_log_entry(
                index=index,
                message=event.obj.value,
            )
        self.reset_selection()

    def reset_selection(self):
        self.tabulator.selection = []
        self.text_table.value = ""

    def handle_remove(self, event):
        for index in self.tabulator.selection:
            if not self._is_new(index):
                message_id = self.tabulator.value["id"][index]
                try:
                    delete_message(message_id)
                    self.tabulator.patch(
                        {
                            "message_text": [(index, "")],
                            "user_id": [(index, "")],
                            "user_agent": [(index, "")],
                            "exposure_flag": [(index, "")],
                            "id": [(index, "")],
                            "is_human": [(index, "")],
                            "is_valid": [(index, "")],
                        }
                    )
                    self.tabulator.value["id"][index] = ""
                except Exception:
                    raise RuntimeError(f"Failed to remove message: {message_id}.")
        self.reset_selection()

    def component(self):

        return pn.Column(
            pn.Row(*self.exposure_flag_buttons),
            self.tabulator,
            self.text_table,
            self.remove_log_entry_button,
        )
