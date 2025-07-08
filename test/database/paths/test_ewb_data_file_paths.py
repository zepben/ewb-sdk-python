#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import date, timedelta
from pathlib import Path
from typing import Iterator
from unittest.mock import Mock

from _pytest.python_api import raises

from zepben.ewb import EwbDataFilePaths, DatabaseType

base_dir = Path("/not/real/path/")


def expected_dated_path(expected_date, file_descriptor):
    return Path(f"{base_dir}/{expected_date}/{expected_date}-{file_descriptor}.sqlite")


def expected_path(file_descriptor):
    return Path(f"{base_dir}/{file_descriptor}.sqlite")


def test_validates_directory_is_valid_at_construction():
    mock_is_directory = Mock(return_value=True)
    EwbDataFilePaths(base_dir, is_directory=mock_is_directory)
    mock_is_directory.assert_called_once_with(base_dir)

    mock_is_directory.reset_mock()
    mock_is_directory.return_value = False
    with raises(ValueError, match="base_dir must be a directory"):
        EwbDataFilePaths(base_dir, is_directory=mock_is_directory)
    mock_is_directory.assert_called_once_with(base_dir)


def test_creates_missing_root_directory_if_requested():
    mock_create_dir = Mock(side_effect=lambda to_create: to_create)

    EwbDataFilePaths(base_dir, create_path=False, is_directory=lambda _: True, create_directories_func=mock_create_dir)
    mock_create_dir.assert_not_called()

    EwbDataFilePaths(base_dir, create_path=True, is_directory=lambda _: True, create_directories_func=mock_create_dir)
    mock_create_dir.assert_called_once_with(base_dir)


def test_formats_paths():
    ewb_paths = EwbDataFilePaths(base_dir,
                                 create_path=False,
                                 create_directories_func=lambda _: None,
                                 is_directory=lambda _: True,
                                 exists=lambda _: True,
                                 list_files=lambda _: iter(list())
                                 )

    test_date = date(4444, 5, 6)

    assert ewb_paths.customer(test_date) == expected_dated_path(test_date, "customers")
    assert ewb_paths.diagram(test_date) == expected_dated_path(test_date, "diagrams")
    assert ewb_paths.measurement(test_date) == expected_dated_path(test_date, "measurements")
    assert ewb_paths.network_model(test_date) == expected_dated_path(test_date, "network-model")
    assert ewb_paths.tile_cache(test_date) == expected_dated_path(test_date, "tile-cache")
    assert ewb_paths.energy_reading(test_date) == expected_dated_path(test_date, "load-readings")

    assert ewb_paths.energy_readings_index() == expected_path("load-readings-index")
    assert ewb_paths.load_aggregator_meters_by_date() == expected_path("load-aggregator-mbd")
    assert ewb_paths.weather_reading() == expected_path("weather-readings")
    assert ewb_paths.results_cache() == expected_path("results-cache")


def test_creates_data_directories_if_they_dont_exist():
    test_date = date(1111, 2, 3)

    expected_date_path = Path(str(base_dir), str(test_date))

    mock_exists = Mock(return_value=True)

    mock_create_dir = Mock(side_effect=lambda to_create: to_create)

    ewb_paths = EwbDataFilePaths(base_dir,
                                 create_path=False,
                                 create_directories_func=mock_create_dir,
                                 is_directory=lambda _: True,
                                 exists=mock_exists,
                                 list_files=lambda _: iter(list())
                                 )

    # if the date directory already exists
    assert ewb_paths.create_directories(test_date) == expected_date_path
    mock_exists.assert_called_once_with(expected_date_path)
    mock_create_dir.assert_not_called()

    mock_exists.reset_mock()
    mock_exists.return_value = False

    # if the date directory needs to be created
    assert ewb_paths.create_directories(test_date) == expected_date_path
    mock_exists.assert_called_once_with(expected_date_path)
    mock_create_dir.assert_called_once_with(expected_date_path)


def test_finds_specified_date_if_it_exists():
    test_date = date(2222, 3, 4)
    for db_type in DatabaseType:
        if db_type.per_date:
            validate_closest_by_exists_calls(db_type, test_date, test_date, 10, False, 1, True, lambda _: True)
            # confirm finds the database on the exact day if max_days_to_search = 0
            validate_closest_by_exists_calls(db_type, test_date, test_date, 0, False, 1, True, lambda _: True)
        else:
            validate_closest_by_exists_calls(db_type, test_date, test_date, 10, False, 0, False, lambda _: True)


def test_finds_previous_date_if_it_exists_and_today_is_missing():
    actual_date = date(2000, 5, 5)
    search_date = date(2000, 5, 7)
    for db_type in DatabaseType:
        if db_type.per_date:
            validate_closest_by_exists_calls(db_type, actual_date, search_date, 10, False, 3, True)


def validate_closest_by_exists_calls(database_type: DatabaseType, db_date: date, search_date: date, max_days_to_search: int, search_forwards: bool,
                                     expected_exist_calls: int, expect_to_find: bool, my_exists=None):
    if my_exists is None:
        def my_exists(to_test: Path) -> bool:
            return to_test == expected_dated_path(db_date, database_type.file_descriptor)

    mock_exists = Mock(side_effect=my_exists)

    ewb_paths = EwbDataFilePaths(base_dir,
                                 create_path=False,
                                 create_directories_func=Mock(),
                                 is_directory=lambda _: True,
                                 exists=mock_exists,
                                 list_files=lambda _: iter(list())
                                 )

    expected_return = None
    if expect_to_find:
        expected_return = db_date

    assert ewb_paths.find_closest(database_type, max_days_to_search=max_days_to_search, target_date=search_date,
                                  search_forwards=search_forwards) == expected_return
    assert mock_exists.call_count == expected_exist_calls


def test_doesnt_find_files_outside_the_search_window():
    actual_date = date(2000, 5, 5)
    search_date = date(2000, 5, 16)
    for db_type in DatabaseType:
        if db_type.per_date:
            validate_closest_by_exists_calls(db_type, actual_date, search_date, 10, False, 11, expect_to_find=False)


def test_can_search_forwards_in_time():
    previous_date = date(2000, 5, 5)
    search_date = date(2000, 5, 8)
    forward_date = date(2000, 5, 10)

    for db_type in DatabaseType:
        if db_type.per_date:
            my_list = [expected_dated_path(previous_date, db_type.file_descriptor), expected_dated_path(forward_date, db_type.file_descriptor)]

            validate_closest_by_exists_calls(db_type, forward_date, search_date, 10, True, 5, expect_to_find=True, my_exists=lambda to_test: to_test in my_list)


def test_closest_date_using_default_parameters():
    previous_date = date.today() - timedelta(days=2)
    forward_date = date.today() + timedelta(days=1)

    for db_type in DatabaseType:
        if db_type.per_date:
            my_list = [expected_dated_path(previous_date, db_type.file_descriptor), expected_dated_path(forward_date, db_type.file_descriptor)]

            mock_exists = Mock(side_effect=lambda to_test: to_test in my_list)

            ewb_paths = EwbDataFilePaths(base_dir,
                                         create_path=False,
                                         create_directories_func=Mock(),
                                         is_directory=lambda _: True,
                                         exists=mock_exists,
                                         list_files=lambda _: iter(list())
                                         )

            assert ewb_paths.find_closest(db_type) == previous_date
            assert mock_exists.call_count == 3


def test_get_available_dates_for_accepts_date_types():
    for db_type in DatabaseType:
        if db_type.per_date:
            validate_get_available_dates_for(db_type)


def test_get_available_dates_for_throws_on_non_date_type():
    for db_type in DatabaseType:
        if not db_type.per_date:
            with raises(ValueError, match="INTERNAL ERROR: Should only be calling `_get_available_dates_for` for `per_date` files."):
                validate_get_available_dates_for(db_type)


def test_get_available_dates_for_sorts_the_returned_dates():
    unsorted_dates = ["2001-02-03", "2032-05-07", "2009-05-09", "2009-05-08"]

    ewb_paths = EwbDataFilePaths(base_dir,
                                 create_path=False,
                                 create_directories_func=Mock(),
                                 is_directory=Mock(return_value=True),
                                 exists=Mock(return_value=True),
                                 list_files=Mock(return_value=iter([Path(str(base_dir), x) for x in unsorted_dates]))
                                 )
    sorted_dates = [
        date.fromisoformat("2001-02-03"),
        date.fromisoformat("2009-05-08"),
        date.fromisoformat("2009-05-09"),
        date.fromisoformat("2032-05-07")]
    assert ewb_paths._get_available_dates_for(DatabaseType.NETWORK_MODEL) == sorted_dates


def validate_get_available_dates_for(db_type: DatabaseType):
    usable_directories = ["2001-02-03", "2001-02-04", "2011-03-09"]
    empty_directories = ["2111-11-11", "2222-12-14"]
    non_date_directories = ["other_data", "2002-02-04-backup", "backup-2011-03-09"]
    non_directory_files = ["config.json", "other", "run.sh", "1234-11-22"]

    all_files = usable_directories + empty_directories + non_date_directories + non_directory_files
    date_directories = usable_directories + empty_directories

    def my_list_dir(to_list: Path) -> Iterator[Path]:
        if to_list == base_dir:
            return iter([Path(str(base_dir), x) for x in all_files])

    def my_is_directory(to_test: Path) -> bool:
        if to_test in [Path(str(base_dir), x) for x in non_directory_files]:
            return False
        return True

    def my_exists(to_test: Path) -> bool:
        if to_test in [expected_dated_path(date.fromisoformat(x), db_type.file_descriptor) for x in empty_directories]:
            return False
        return True

    mock_list_dir = Mock(side_effect=my_list_dir)
    mock_is_directory = Mock(side_effect=my_is_directory)
    mock_exists = Mock(side_effect=my_exists)

    ewb_paths = EwbDataFilePaths(base_dir,
                                 create_path=False,
                                 create_directories_func=Mock(),
                                 is_directory=mock_is_directory,
                                 exists=mock_exists,
                                 list_files=mock_list_dir
                                 )

    assert [date.fromisoformat(x) for x in usable_directories] == ewb_paths._get_available_dates_for(db_type)

    mock_list_dir.assert_called_once_with(base_dir)
    for it in all_files:
        mock_is_directory.assert_any_call(Path(str(base_dir), it))
        if it in date_directories:
            mock_exists.assert_any_call(expected_dated_path(date.fromisoformat(it), db_type.file_descriptor))
