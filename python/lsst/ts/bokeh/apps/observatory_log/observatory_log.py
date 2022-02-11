import pandas as pd
import panel as pn

from bokeh.models.widgets.tables import NumberFormatter

import lsst.daf.butler as dafButler

from .helpers import (
    add_message,
    edit_message,
    delete_message,
    MessageSearcher,
    get_empty_message_dataframe,
)

__all__ = ["ObservatoryLog"]


class ObservatoryLog:
    def __init__(self, dataset, obs_id):

        self.dataset = dataset
        self.obs_id = obs_id
        self.obs_id_end = obs_id + 100000

        self.df = self.get_data()
        tabulator_formatters = {
            "exposure": NumberFormatter(format="0"),
        }

        self.tabulator = pn.widgets.Tabulator(
            self.df, layout="fit_data_fill", height=450, formatters=tabulator_formatters
        )
        self.tabulator.disabled = True
        self.tabulator.hidden_columns = [
            "id",
            "is_human",
            "is_valid",
            "instrument_x",
            "user_agent",
        ]

        self.follow = pn.widgets.Checkbox(name="Follow", value=True, align="end")

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
            pn.widgets.Button(
                name="deselect",
                width=50,
                max_width=100,
                width_policy="fixed",
            ),
        )
        self.exposure_flag_buttons[1].on_click(self.set_exposure_flag_none)
        self.exposure_flag_buttons[2].on_click(self.set_exposure_flag_questionable)
        self.exposure_flag_buttons[3].on_click(self.set_exposure_flag_junk)
        self.exposure_flag_buttons[4].on_click(self.deselect)

        self.remove_log_entry_button = pn.widgets.Button(
            name="Remove", width=50, max_width=100, width_policy="fixed"
        )
        self.remove_log_entry_button.on_click(self.handle_remove)

        self.disable_buttons()

        self.tabulator.param.watch(self.selected, "selection")
        self.text_table.param.watch(self.handle_log, "value")

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

    def _set_exposure_flag(self, flag):
        for index in self.tabulator.selection:

            exposure_id = self.tabulator.value["exposure"][index]
            latest_valid_message = MessageSearcher(
                obs_id=exposure_id, order_by=["date_added"]
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
                obs_id=exposure_id, order_by=["date_added"]
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

    def disable_buttons(self):
        self.exposure_flag_buttons[1].disabled = True
        self.exposure_flag_buttons[2].disabled = True
        self.exposure_flag_buttons[3].disabled = True
        self.exposure_flag_buttons[4].disabled = True
        self.remove_log_entry_button.disabled = True
        self.text_table.disabled = True

    def enable_buttons(self):
        self.exposure_flag_buttons[1].disabled = False
        self.exposure_flag_buttons[2].disabled = False
        self.exposure_flag_buttons[3].disabled = False
        self.exposure_flag_buttons[4].disabled = False
        self.remove_log_entry_button.disabled = False
        self.text_table.disabled = False

    def get_data(self):

        butler = dafButler.Butler(f"/repo/{self.dataset}/")

        exposures = pd.DataFrame(
            record.toDict()
            for record in butler.registry.queryDimensionRecords(
                "exposure",
                where=f"instrument = '{self.dataset}' and "
                f"exposure > {self.obs_id} and exposure < {self.obs_id_end}",
            )
        )

        if len(exposures) == 0:
            return None

        exposures["id"] = exposures["id"].astype(int)

        valid_messages = [
            message
            for message in [
                MessageSearcher(obs_id=obs_id, order_by=["date_added"]).search()[-1:]
                for obs_id in exposures["id"]
            ]
            if len(message) > 0
        ]

        if len(valid_messages) > 0:
            valid_messages = pd.concat(valid_messages)
            valid_messages["obs_id"] = valid_messages["obs_id"].astype(int)
        else:
            valid_messages = get_empty_message_dataframe()

        self.obs_id = exposures["id"].max()

        data = pd.merge(
            left=exposures,
            right=valid_messages,
            how="left",
            left_on="id",
            right_on="obs_id",
        ).fillna("")

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

    def get_patch(self, patch_indexes):

        valid_messages = [
            message
            for message in [
                MessageSearcher(obs_id=obs_id, order_by=["date_added"]).search()[-1:]
                for obs_id in self.tabulator.value["exposure"][patch_indexes]
            ]
            if len(message) > 0
            and message["id"][0] not in self.tabulator.value["id"].values
        ]

        if len(valid_messages) == 0:
            return None

        valid_messages = pd.concat(valid_messages)

        valid_messages["obs_id"] = valid_messages["obs_id"].astype(int)

        mask = self.tabulator.value["exposure"].isin(valid_messages["obs_id"])

        update_obs_id = self.tabulator.value["exposure"][mask]
        update_loc = self.tabulator.value["exposure"].index[mask]

        update_messages = valid_messages[valid_messages["obs_id"].isin(update_obs_id)]

        update_messages.index = update_loc

        return update_messages[
            [
                "user_id",
                "user_agent",
                "is_human",
                "is_valid",
                "exposure_flag",
                "id",
                "message_text",
            ]
        ]

    def stream(self):
        try:
            data = self.get_data()
            if data is not None:
                self.tabulator.stream(data, follow=self.follow.value)

            table_size = len(self.tabulator.value)
            update_size = self.tabulator.page_size + 5
            self.handle_patch(range(table_size - update_size, table_size))

        except Exception as e:
            print(f"Error: {e}")

    def handle_patch(self, patch_indexes):
        patch = self.get_patch(patch_indexes)
        if patch is not None:
            print(f"Patching {len(patch)} messages...")
            self.tabulator.patch(patch)
            for index, message_id in zip(patch.index, patch["id"]):
                self.tabulator.value["id"][index] = message_id
        else:
            print("Nothing to patch...")

    def patch_selection(self):

        patch_indexes = range(
            max([min(self.tabulator.selection) - self.tabulator.page_size, 0]),
            min(
                [
                    max(self.tabulator.selection) + self.tabulator.page_size,
                    len(self.tabulator.value),
                ]
            ),
        )

        self.handle_patch(patch_indexes)

    def selected(self, event):
        if len(event.obj.selection) == 0:
            self.text_table.placeholder = "Enter a log here..."
            self.remove_log_entry_button.disabled = True
            self.disable_buttons()
        else:
            self.patch_selection()
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
        )
