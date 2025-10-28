#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['EwbDataFilePaths']

from abc import ABC, abstractmethod
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, List, Generator

from zepben.ewb import require
from zepben.ewb.database.paths.database_type import DatabaseType


class EwbDataFilePaths(ABC):
    """Provides paths to all the various data files / folders used by EWB."""

    VARIANTS_PATH: str = "variants"
    """
    The folder containing the variants. Will be placed under the dated folder alongside the network model database.
    """

    def resolve(self, database_type: DatabaseType, database_date: Optional[date] = None, variant: Optional[str] = None) -> Path:
        """
        Resolves the :class:`Path` to the database file for the specified :class:`DatabaseType`, within the specified `database_date`
        and optional `variant` when `DatabaseType.per_date` is set to true.

        :param database_type: The :class:`DatabaseType` to use for the database :class:`Path`.
        :param database_date: The :class:`date` to use for the database :class:`Path`. Required when `database_type.per_date` is true, otherwise must be `None`.
        :param variant: The optional name of the variant containing the database.

        :return: The :class:`Path` to the :class:`DatabaseType` database file.
        """
        if database_date is not None:
            require(database_type.per_date, lambda: "database_type must have its per_date set to True to use this method with a database_date.")
            if variant is not None:
                return self.resolve_database(self._to_dated_variant_path(database_type, database_date, variant))
            else:
                return self.resolve_database(self._to_dated_path(database_type, database_date))
        else:
            require(not database_type.per_date, lambda: "database_type must have its per_date set to False to use this method without a database_date.")
            return self.resolve_database(Path(self._database_name(database_type)))

    @abstractmethod
    def create_directories(self, database_date: date) -> Path:
        """
        Create the directories required to have a valid path for the specified date.

        :param database_date: The :class:`date` required in the path.
        :return: The :class:`Path` to the directory for the `database_date`.
        """
        raise NotImplemented

    def find_closest(
        self,
        database_type: DatabaseType,
        max_days_to_search: int = 999999,
        target_date: date = date.today(),
        search_forwards: bool = False
    ) -> Optional[date]:
        """
        Find the closest date with a usable database of the specified type.

        :param database_type: The type of database to search for.
        :param max_days_to_search: The maximum number of days to search for a valid database.
        :param target_date: The target date. Defaults to today.
        :param search_forwards: Indicates the search should also look forwards in time from `target_date` for a valid file. Defaults to reverse search only.

        :return: The closest :class:`date` to `target_date` with a valid database of `database_type` within the search parameters, or null if no valid database
          was found.
        """
        if not database_type.per_date:
            return None

        descendants = list(self.enumerate_descendants())
        if self._check_exists(descendants, database_type, target_date):
            return target_date

        offset = 1
        while offset <= max_days_to_search:
            offset_days = timedelta(offset)
            try:
                previous_date = target_date - offset_days
                if self._check_exists(descendants, database_type, previous_date):
                    return previous_date
            except OverflowError:
                pass

            if search_forwards:
                try:
                    forward_date = target_date + offset_days
                    if self._check_exists(descendants, database_type, forward_date):
                        return forward_date
                except OverflowError:
                    pass

            offset += 1

        return None

    def get_available_dates_for(self, database_type: DatabaseType) -> List[date]:
        """
        Find available databases specified by :class:`DatabaseType` in data path.

        :param database_type: The type of database to search for.

        :return: list of :class:`date`'s for which this specified :class:`DatabaseType` databases exist in the data path.
        """
        if not database_type.per_date:
            raise ValueError(
                "INTERNAL ERROR: Should only be calling `get_available_dates_for` for `per_date` files, "
                "which should all be covered above, so go ahead and add it."
            )

        to_return = list()

        for it in self.enumerate_descendants():
            if it.name.endswith(self._database_name(database_type)):
                try:
                    to_return.append(date.fromisoformat(it.parent.name))
                except ValueError:
                    pass

        return sorted(to_return)

    def get_available_variants_for(self, target_date: date = date.today()) -> List[str]:
        """
        Find available variants for the specified `target_date` in data path.

        :param target_date: The target date. Defaults to today.

        :return: list of variant names that exist in the data path for the specified `target_date`.
        """
        to_return = list()

        for it in self.enumerate_descendants():
            try:
                if (str(it.parent.name).lower() == self.VARIANTS_PATH) and (str(it.parent.parent.name) == str(target_date)):
                    to_return.append(str(it.name))
            except ValueError:
                pass

        return sorted(to_return)

    @abstractmethod
    def enumerate_descendants(self) -> Generator[Path, None, None]:
        """
        Lists the child items of source location.

        :return: generator of child items.
        """
        raise NotImplemented

    @abstractmethod
    def resolve_database(self, path: Path) -> Path:
        """
        Resolves the database in the specified source :class:`Path`.

        :param path: :class:`Path` to the source database file.
        :return: :class:`Path` to the local database file.
        """
        raise NotImplemented

    def _check_exists(self, descendants: List[Path], database_type: DatabaseType, database_date: date) -> bool:
        """
        Check if a database :class:`Path` of the specified :class:`DatabaseType` and :class:`date` exists.

        :param descendants: A list of :class:`Path` representing the descendant paths.
        :param database_type: The type of database to search for.
        :param database_date: The date to check.

        :return: True if a database of the specified `database_type` and `database_date` exits in the date path.
        """
        for cp in descendants:
            if cp.is_relative_to(self._to_dated_path(database_type, database_date)):
                return True

        return False

    def _to_dated_path(self, database_type: DatabaseType, database_date: date) -> Path:
        date_str = str(database_date)
        return Path(date_str).joinpath(f"{date_str}-{self._database_name(database_type)}")

    def _to_dated_variant_path(self, database_type: DatabaseType, database_date: date, variant: str) -> Path:
        date_str = str(database_date)
        return Path(date_str).joinpath(self.VARIANTS_PATH, variant, f"{date_str}-{self._database_name(database_type)}")

    @staticmethod
    def _database_name(database_type: DatabaseType) -> str:
        return f"{database_type.file_descriptor}.sqlite"
