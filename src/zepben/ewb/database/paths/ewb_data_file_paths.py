#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['EwbDataFilePaths']

from abc import ABC, abstractmethod
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, List, Generator, overload

from zepben.ewb import require
from zepben.ewb.database.paths.database_type import DatabaseType, VariantContents
from zepben.ewb.database.paths.dated_variant_path_components import DatedVariantPathComponents


class EwbDataFilePaths(ABC):
    """Provides paths to all the various data files / folders used by EWB."""

    VARIANTS_PATH: str = "variants"
    """
    The folder containing the variants. Will be placed under the dated folder alongside the network model database.
    """

    @overload
    def resolve(self, database_type: DatabaseType, database_date: date | None = None) -> Path: ...
    """
    Resolves the `Path` to the database file for the specified `DatabaseType` that has 
    `DatabaseType.per_date` set to true and the specified `date`.
    """

    @overload
    def resolve(self, database_type: DatabaseType) -> Path: ...

    @overload
    def resolve(
        self,
        database_type: DatabaseType,
        database_date: date | None = None,
        variant: str | None = None,
        variant_contents: VariantContents | None = None
    ) -> Path: ...
    """
    Resolves the `Path` to the database file for the specified `DatabaseType` that has 
    `DatabaseType.per_date` set to true and the specified `date`, within the `variant`, for the specified `variant_contents.
    
    `ChangeSet` content is split into two separate databases for each supported `DatabaseType`, with targets of ObjectCreations and ObjectModifications going
    to one database, and targets of ObjectDeletions and ObjectReverseModifications going to another. This is to avoid conflicting IDs between the two
    databases.
    The ChangeSet and it's associated ObjectCreation, ObjectDeletion and ObjectModifications will be in a single `DatabaseType.VARIANT` database.
    """

    def resolve(
        self,
        database_type: DatabaseType,
        database_date: date | None = None,
        variant: str | None = None,
        variant_contents: VariantContents | None = None
    ) -> Path:
        """
        Resolves the :class:`Path` to the database file for the specified :class:`DatabaseType`, within the specified `database_date`
        and optional `variant` when `DatabaseType.per_date` is set to true.

        :param database_type: The :class:`DatabaseType` to use for the database :class:`Path`.
        :param database_date: The :class:`date` to use for the database :class:`Path`. Required when `database_type.per_date` is true, otherwise must be `None`.
        :param variant: The optional name of the variant containing the database.
        :param variant_contents: The relevant content for the desired `database_type`, when resolving a variant database. Defaults to `VariantContents.CHANGESET` when a variant is supplied.

        :return: The :class:`Path` to the :class:`DatabaseType` database file.
        """
        if database_date is not None:
            require(database_type.per_date, lambda: "database_type must have its per_date set to True to use this method with a database_date.")
            if variant is not None:
                contents = variant_contents if variant_contents is not None else VariantContents.CHANGESET
                require(contents.types.__contains__(database_type),
                        lambda: f"database_type must be compatible with variant_contents. Compatible options for {contents.name}: {', '.join([t.short_name for t in contents.types])}")
                return self.resolve_database(self._to_dated_variant_path(database_type, database_date, variant, contents))
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
        raise NotImplementedError

    def find_closest(
        self,
        database_type: DatabaseType,
        max_days_to_search: int = 999999,
        target_date: date = date.today(),
        search_forwards: bool = False
    ) -> date | None:
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
        to_return = set()

        for it in self.enumerate_descendants():
            try:
                # GIS extractor doesn't have a variant service file at the 2 parents level.
                if (str(it.parent.parent.name) == self.VARIANTS_PATH) and (str(it.parent.parent.parent.name) == str(target_date)):
                    to_return.add(str(it.parent.name))
                elif (str(it.parent.name) == self.VARIANTS_PATH) and (str(it.parent.parent.name) == str(target_date)):
                    to_return.add(str(it.name))
            except ValueError:
                pass

        return sorted(to_return)

    def exists(
        self,
        database_type: DatabaseType,
        database_date: date,
        variant: str,
        variant_contents: VariantContents
    ) -> bool:
        """
        A helper to check if variant files exist before attempting to access them. This can be used to prevent
        excess errors being logged when files that aren't required are missing.

        :param database_type: The :class:`DatabaseType` to use for the database :class:`Path`.
        :param database_date: The :class:`date` to use for the database :class:`Path`.
        :param variant: The name of the variant containing the database.
        :param variant_contents: The relevant content for the desired `database_type`.

        :return: `True` if the :class:`Path` to the :class:`DatabaseType` database file for the `variant` exists in the current descendants.
        """
        require(database_type.per_date, lambda: "database_type must have its per_date set to True to use this method.")
        require(variant_contents.types.__contains__(database_type),
                lambda: f"database_type must be compatible with variant_contents. Compatible options for {variant_contents.name}: "
                        f"{', '.join([t.short_name for t in variant_contents.types])}")

        target = self._to_dated_variant_path(database_type, database_date, variant, variant_contents)
        return any(it == target for it in self.enumerate_descendants(f"{database_date}/{self.VARIANTS_PATH}"))

    def get_dated_path(self, database_type: DatabaseType, database_date: date) -> Path:
        """
        Generate a file path for a given date and type.

        :param database_type: The :class:`DatabaseType` to use for the database :class:`Path`.
        :param database_date: The :class:`date` to use for the database :class:`Path`.
        """
        return self._to_dated_path(database_type, database_date)

    def get_dated_variant_path(
        self,
        database_type: DatabaseType,
        database_date: date,
        variant: str,
        variant_contents: VariantContents
    ) -> Path:
        """
        Generate a file path for a given date, variant, and the contents of that variant.

        :param database_type: The :class:`DatabaseType` to use for the database :class:`Path`.
        :param database_date: The :class:`date` to use for the database :class:`Path`.
        :param variant: The name of the variant containing the database.
        :param variant_contents: The relevant content for the desired `database_type`.

        :return: The :class:`Path` to the :class:`DatabaseType` database file for the `variant`.
        """
        return self._to_dated_variant_path(database_type, database_date, variant, variant_contents)

    def parse_dated_variant_path(self, path: Path) -> DatedVariantPathComponents:
        """
        Parses a dated variant `path` into its constituent components.

        This is the inverse of :meth:`get_dated_variant_path`.

        Expected path formats:
        - `{date}/variants/{variant}/{subDirectory}/{date}-{databaseName}` (when `variant_contents.sub_directory` is non-empty)
        - `{date}/variants/{variant}/{date}-{databaseName}` (when `variant_contents.sub_directory` is empty)

        :param path: The path to parse.

        :return: A :class:`DatedVariantPathComponents` containing the extracted :class:`DatabaseType`, :class:`date`, variant name, and :class:`VariantContents`.
        :raises ValueError: If the path does not match the expected format.
        """
        path_components = [str(it) for it in path.parts]

        if len(path_components) == 4:
            variant_contents = VariantContents.CHANGESET
        elif len(path_components) == 5:
            sub_dir = path_components[3]
            variant_contents = next((it for it in VariantContents if it.sub_directory == sub_dir), None)
            if variant_contents is None:
                raise ValueError(f"Invalid path. There is no `VariantContent` for the sub directory `{sub_dir}`.")
        else:
            raise ValueError("Invalid path. Make sure the path is correct by using `get_dated_variant_path`.")

        file_name = path.with_suffix("").name
        date_str = path_components[0]
        database_type = next((it for it in variant_contents.types if file_name == f"{date_str}-{it.file_descriptor}"), None)
        if database_type is None:
            raise ValueError(f"Invalid path. There is no `DatabaseType` for the file name `{file_name}`.")

        return DatedVariantPathComponents(
            type=database_type,
            date=date.fromisoformat(date_str),
            variant=path_components[2],
            variant_contents=variant_contents,
        )

    @abstractmethod
    def enumerate_descendants(self, prefix: str | None = None) -> Generator[Path, None, None]:
        """
        Lists the child items of source location, optionally scoped under a sub `prefix` of the base directory.

        :param prefix: An optional sub-directory (relative to the base directory) to enumerate under. When `None`, the whole
          source location is enumerated.
        :return: generator of child items.
        """
        raise NotImplementedError

    @abstractmethod
    def resolve_database(self, path: Path) -> Path:
        """
        Resolves the database in the specified source :class:`Path`.

        :param path: :class:`Path` to the source database file.
        :return: :class:`Path` to the local database file.
        """
        raise NotImplementedError

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

    def _to_dated_variant_path(
        self,
        database_type: DatabaseType,
        database_date: date,
        variant: str,
        variant_contents: VariantContents = VariantContents.CHANGESET
    ) -> Path:
        date_str = str(database_date)
        return (Path(date_str).joinpath(
            self.VARIANTS_PATH,
            variant,
            variant_contents.sub_directory,
            f"{date_str}-{self._database_name(database_type)}"
        ))

    @staticmethod
    def _database_name(database_type: DatabaseType) -> str:
        return f"{database_type.file_descriptor}.sqlite"
