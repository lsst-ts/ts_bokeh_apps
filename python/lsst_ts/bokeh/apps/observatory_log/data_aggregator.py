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

import pandas as pd

import lsst.daf.butler as dafButler

from lsst.ts.bokeh.apps.base_data_aggregator import BaseDataAggregator

from .helpers import (
    MessageSearcher,
    get_empty_message_dataframe,
)


class DataAggregator(BaseDataAggregator):
    """Data aggregator class for the observatory log app."""

    def __init__(self) -> None:

        super().__init__()

        self.dataset = None
        self.obs_id = None

        self.df = None

    @property
    def obs_id_end(self) -> int:
        return self.obs_id + 100000 if self.obs_id is not None else 0

    def get_data(self) -> pd.DataFrame:
        """Retrieve data from the butler and the log tables.

        Returns
        -------
        pd.DataFrame
            Log table data.
        """

        exposures = self._get_exposures_metadata()

        if len(exposures) == 0:
            return self.get_empty_table_view()

        valid_messages = self._get_valid_messages(exposure_ids=exposures["id"])

        data = pd.merge(
            left=exposures,
            right=valid_messages,
            how="left",
            left_on="id",
            right_on="obs_id",
        ).fillna("")

        data["exposure"] = exposures["id"]
        data["id"] = data["id_y"]

        return data.get(self._get_table_columns())

    def get_patch(
        self, patch_indexes: typing.List[int]
    ) -> typing.Union[pd.DataFrame, None]:
        """Get patch for data table.

        Parameters
        ----------
        patch_indexes : list of int
            Table indexes to patch.

        Returns
        -------
        pd.DataFrame or None
            Patched data.
        """

        valid_messages = self._get_valid_messages(
            self.tabulator.value["exposure"][patch_indexes]
        )

        if len(valid_messages) == 0:
            return None

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

    def get_empty_table_view(self) -> pd.DataFrame:
        """Return an empty data frame with the same data structure as that of
        the display table.

        Returns
        -------
        pd.DataFrame
            Empty pandas dataframe.
        """
        return pd.DataFrame(columns=self._get_table_columns())

    def _get_table_columns(self) -> typing.List[str]:
        """Return table columns names.

        Returns
        -------
        list of str
            List with table column names.
        """
        return [
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

    def _get_exposures_metadata(self) -> pd.DataFrame:
        """Return exposure metadata from butler for the specified dataset and
        obs_id.

        Returns
        -------
        exposures_metadata : pd.DataFrame
            Exposures metadata from butler.
        """

        if None in {self.dataset, self.obs_id}:
            return pd.DataFrame()

        butler = dafButler.Butler(f"/repo/{self.dataset}/")

        exposures_metadata = pd.DataFrame(
            record.toDict()
            for record in butler.registry.queryDimensionRecords(
                "exposure",
                where=f"instrument = '{self.dataset}' and "
                f"exposure > {self.obs_id} and exposure < {self.obs_id_end}",
            )
        )

        exposures_metadata["id"] = exposures_metadata["id"].astype(int)

        self.obs_id = exposures_metadata["id"].max()

        return exposures_metadata

    def _get_valid_messages(self, exposure_ids: pd.Series) -> pd.DataFrame:
        """Get valid log messages from the log database.

        Parameters
        ----------
        exposure_ids : `pd.Series`
            Exposure ids.

        Returns
        -------
        valid_messages : `pd.DataFrame`
            Valid log messages.
        """

        valid_messages = [
            message
            for message in [
                MessageSearcher(
                    instruments=[
                        self.dataset.lower(),
                    ],
                    obs_id=obs_id,
                    order_by=["date_added"],
                ).search()[-1:]
                for obs_id in exposure_ids
            ]
            if len(message) > 0
        ]

        if len(valid_messages) > 0:
            valid_messages = pd.concat(valid_messages)
            valid_messages["obs_id"] = valid_messages["obs_id"].astype(int)
        else:
            valid_messages = get_empty_message_dataframe()

        return valid_messages
