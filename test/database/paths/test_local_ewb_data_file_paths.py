#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import date, timedelta
from pathlib import Path
from typing import List, Generator, Optional
from unittest.mock import Mock

from pytest import raises

from zepben.ewb import LocalEwbDataFilePaths, DatabaseType, EwbDataFilePaths


class TestLocalEwbDataFilePaths:

    def setup_method(self):
        self.today = date.today()
        self.base_dir = Path("/not/real/path/")
        self.descendant_paths: List[Path] = []

        self.mock_create_directories = Mock(side_effect=lambda path: path)
        self.mock_is_directory = Mock(return_value=True)
        self.mock_exists = Mock(return_value=True)

        def list_files(_: Path) -> Generator[Path, None, None]:
            for it in self.descendant_paths:
                yield it

        self.ewb_paths = LocalEwbDataFilePaths(
            self.base_dir,
            create_path=False,
            create_directories_func=self.mock_create_directories,
            is_directory=self.mock_is_directory,
            exists=self.mock_exists,
            list_files=list_files
        )

    def test_validates_directory_is_valid_at_construction(self):
        self.mock_is_directory.assert_called_once_with(self.base_dir)

        self.mock_is_directory.reset_mock()
        self.mock_is_directory.return_value = False

        with raises(ValueError, match="base_dir must be a directory"):
            LocalEwbDataFilePaths(self.base_dir, is_directory=self.mock_is_directory)

        self.mock_is_directory.assert_called_once_with(self.base_dir)

    def test_creates_missing_root_directory_if_requested(self):
        # Assert the default __init__ version didn't try and create the
        self.mock_create_directories.assert_not_called()

        LocalEwbDataFilePaths(self.base_dir, create_path=True, is_directory=self.mock_is_directory, create_directories_func=self.mock_create_directories)
        self.mock_create_directories.assert_called_once_with(self.base_dir)

    def test_formats_paths(self):
        for database_type in DatabaseType:
            if database_type.per_date:
                assert self.ewb_paths.resolve(database_type, self.today) == self._expected_dated_path(self.today, database_type.file_descriptor)
            else:
                with raises(ValueError, match="database_type must have its per_date set to True to use this method with a database_date."):
                    self.ewb_paths.resolve(database_type, self.today)

        for database_type in DatabaseType:
            if not database_type.per_date:
                assert self.ewb_paths.resolve(database_type) == Path(f"{self.base_dir}/{database_type.file_descriptor}.sqlite")
            else:
                with raises(ValueError, match="database_type must have its per_date set to False to use this method without a database_date."):
                    self.ewb_paths.resolve(database_type)

    def test_creates_data_directories_if_they_dont_exist(self):
        date_dir = self.base_dir.joinpath(str(self.today))

        assert self.ewb_paths.create_directories(self.today) == date_dir

        self.mock_create_directories.assert_not_called()
        self.mock_exists.return_value = False

        assert self.ewb_paths.create_directories(self.today) == date_dir

        self.mock_create_directories.assert_called_once_with(date_dir)

    def test_finds_specified_date_if_it_exists(self):
        for database_type in DatabaseType:
            if database_type.per_date:
                self.descendant_paths.append(Path(str(self.today)).joinpath(f"{self.today}-{database_type.file_descriptor}.sqlite"))
            else:
                self.descendant_paths.append(Path(f"{database_type.file_descriptor}.sqlite"))

        self._validate_closest(self.today)

    def test_finds_previous_date_if_it_exists_and_today_is_missing(self):
        # NOTE: We want to use two days ago rather than yesterday to make sure it searches more than one day.
        two_days_ago = self.today - timedelta(days=2)

        # Files for 2 days ago.
        for database_type in DatabaseType:
            if database_type.per_date:
                self.descendant_paths.append(Path(str(two_days_ago)).joinpath(f"{two_days_ago}-{database_type.file_descriptor}.sqlite"))

        self._validate_closest(two_days_ago)

    def test_doesnt_find_files_outside_the_search_window(self):
        eleven_days_ago = self.today - timedelta(days=11)

        # Files for 11 days ago.
        for database_type in DatabaseType:
            if database_type.per_date:
                self.descendant_paths.append(Path(str(eleven_days_ago)).joinpath(f"{eleven_days_ago}-{database_type.file_descriptor}.sqlite"))

        # Doesn't find files for 11 days ago (outside the 10-day search).
        self._validate_closest(None)

    def test_can_search_forwards_in_time(self):
        # NOTE: We want to use two days from now rather than tomorrow to make sure it searches more than one day. We also use
        #       three days ago to make sure it is searching outwards from the date, not into the past then the future.
        two_days_from_now = self.today + timedelta(days=2)
        three_days_ago = self.today - timedelta(days=3)

        # Files for 2 days from now and 3 days ago.
        for database_type in DatabaseType:
            if database_type.per_date:
                self.descendant_paths.append(Path(str(two_days_from_now)).joinpath(f"{two_days_from_now}-{database_type.file_descriptor}.sqlite"))
                self.descendant_paths.append(Path(str(three_days_ago)).joinpath(f"{three_days_ago}-{database_type.file_descriptor}.sqlite"))

        self._validate_closest(two_days_from_now, search_forwards=True)

    def test_closest_date_using_default_parameters(self):
        tomorrow = self.today + timedelta(days=1)
        two_days_ago = self.today - timedelta(days=2)

        # Files for tomorrow and 2 days ago.
        for database_type in DatabaseType:
            if database_type.per_date:
                self.descendant_paths.append(Path(str(tomorrow)).joinpath(f"{tomorrow}-{database_type.file_descriptor}.sqlite"))
                self.descendant_paths.append(Path(str(two_days_ago)).joinpath(f"{two_days_ago}-{database_type.file_descriptor}.sqlite"))

        # Should find two days ago as it doesn't search forward by default.
        for database_type in DatabaseType:
            if database_type.per_date:
                assert self.ewb_paths.find_closest(DatabaseType.NETWORK_MODEL) == two_days_ago

    def test_get_available_dates_for_accepts_date_types(self):
        for db_type in DatabaseType:
            if db_type.per_date:
                self._validate_get_available_dates_for(db_type)
            else:
                with raises(ValueError, match="INTERNAL ERROR: Should only be calling `get_available_dates_for` for `per_date` files."):
                    self._validate_get_available_dates_for(db_type)

    def test_get_available_dates_for_sorts_the_returned_dates(self):
        self.descendant_paths = [
            Path("2001-02-03", "network-model.sqlite"),
            Path("2032-05-07", "network-model.sqlite"),
            Path("2009-05-09", "network-model.sqlite"),
            Path("2009-05-08", "network-model.sqlite"),
        ]

        assert self.ewb_paths.get_available_dates_for(DatabaseType.NETWORK_MODEL) == [
            date.fromisoformat("2001-02-03"),
            date.fromisoformat("2009-05-08"),
            date.fromisoformat("2009-05-09"),
            date.fromisoformat("2032-05-07"),
        ]

    def test_enumerate_descendants(self):
        self.descendant_paths = [
            Path(str(self.today), f"{self.today}-network-model.sqlite"),
            Path(str(self.today), f"{self.today}-customer.sqlite"),
            Path("results-cache.sqlite"),
            Path("weather-readings.sqlite")
        ]

        result = list(self.ewb_paths.enumerate_descendants())
        assert len(result) == len(self.descendant_paths)
        for it in result:
            assert it in self.descendant_paths, f"{it} - all listed files should have been found in the results."

    def test_resolve_database(self):
        path = "2333-11-22"
        assert self.ewb_paths.resolve_database(Path(path)) == self.base_dir.joinpath(path)

    def test_resolves_variant_databases(self):
        def to_variant_path(variant: str, db_type: DatabaseType) -> Path:
            return self.base_dir.joinpath(str(self.today)).joinpath(EwbDataFilePaths.VARIANTS_PATH) \
                .joinpath(variant).joinpath(f"{self.today}-{db_type.file_descriptor}.sqlite")

        for database_type in DatabaseType:
            if database_type.per_date:
                assert self.ewb_paths.resolve(database_type, self.today, "my-variant1") == to_variant_path("my-variant1", database_type)
                assert self.ewb_paths.resolve(database_type, self.today, "my-variant2") == to_variant_path("my-variant2", database_type)
            else:
                with raises(ValueError, match="database_type must have its per_date set to True to use this method with a database_date."):
                    self.ewb_paths.resolve(database_type, self.today, "my-variant")

    def test_can_request_variants_for_a_day(self):
        yesterday = self.today - timedelta(days=1)

        self.descendant_paths = [
            Path(str(yesterday), EwbDataFilePaths.VARIANTS_PATH, "my-variant-1"),
            Path(str(yesterday), EwbDataFilePaths.VARIANTS_PATH, "my-variant-2"),

            Path(str(self.today), EwbDataFilePaths.VARIANTS_PATH, "my-variant-2"),
            Path(str(self.today), EwbDataFilePaths.VARIANTS_PATH, "my-variant-3"),
        ]

        assert self.ewb_paths.get_available_variants_for(yesterday) == ["my-variant-1", "my-variant-2"]

        # No date will default to today.
        assert self.ewb_paths.get_available_variants_for() == ["my-variant-2", "my-variant-3"]

        # Should return an empty list if there are no variants for the specified date.
        assert self.ewb_paths.get_available_variants_for(self.today - timedelta(days=2)) == []

    def test_variant_databases_dont_count_for_the_exists_check_for_find_nearest(self):
        t1 = self.today - timedelta(days=1)
        t2 = self.today - timedelta(days=2)

        for database_type in DatabaseType:
            if database_type.per_date:
                self.descendant_paths.append(Path(str(t1), EwbDataFilePaths.VARIANTS_PATH, "my-variant", f"{t1}-{database_type.file_descriptor}.sqlite"))

        for database_type in DatabaseType:
            if database_type.per_date:
                assert self.ewb_paths.find_closest(database_type, max_days_to_search=3) is None

        for database_type in DatabaseType:
            if database_type.per_date:
                self.descendant_paths.append(Path(str(t2), f"{t2}-{database_type.file_descriptor}.sqlite"))

        for database_type in DatabaseType:
            if database_type.per_date:
                assert self.ewb_paths.find_closest(database_type, max_days_to_search=3) == t2

    def test_only_folders_under_variants_are_included(self):
        yesterday = self.today - timedelta(days=1)

        self.descendant_paths.append(Path(str(yesterday), "not-variant", "my-variant-1"))

        assert self.ewb_paths.get_available_variants_for(yesterday) == []

    def _expected_dated_path(self, expected_date, file_descriptor):
        return Path(f"{self.base_dir}/{expected_date}/{expected_date}-{file_descriptor}.sqlite")

    def _validate_closest(self, expected_date: Optional[date], search_forwards: bool = False):
        for database_type in DatabaseType:
            if database_type.per_date:
                assert self.ewb_paths.find_closest(database_type, 10, self.today, search_forwards) == expected_date
            else:
                assert self.ewb_paths.find_closest(database_type, 10, self.today, search_forwards) is None

    def _validate_get_available_dates_for(self, db_type: DatabaseType):
        usable_directories = ["2001-02-03", "2001-02-04", "2011-03-09"]
        empty_directories = ["2111-11-11", "2222-12-14"]
        non_date_directories = ["other_data", "2002-02-04-backup", "backup-2011-03-09"]
        non_directory_files = ["config.json", "other", "run.sh", "1234-11-22"]

        other_paths = empty_directories + non_date_directories + non_directory_files

        self.descendant_paths += [Path(self.base_dir, it, f"{db_type.file_descriptor}.sqlite") for it in usable_directories]
        self.descendant_paths += [Path(self.base_dir, it) for it in other_paths]

        assert self.ewb_paths.get_available_dates_for(db_type) == [date.fromisoformat(it) for it in usable_directories]
