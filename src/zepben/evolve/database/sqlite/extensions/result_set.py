#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import Any, Optional, Union, Type, TypeVar, List

from zepben.evolve.model.cim.iec61968.infiec61968.infcommon.ratio import Ratio

__all__ = ["ResultSet"]

T = TypeVar("T")


class ResultSet:
    """
    Wrapper class for records read from a database.
    """
    # The values of this row
    _rows: List[List[Any]]

    # The index of the next row to process
    _next_row_index: int = 0

    # The current row being processed
    _current_row: Optional[List[Any]] = None

    def __init__(self, rows: List[List[Any]]):
        self._rows = rows

    def next(self) -> bool:
        """
        Move to the next row.
        :return: True if a new row was available, otherwise False.
        """
        if self._next_row_index >= len(self._rows):
            self._current_row = None
            return False

        self._current_row = self._rows[self._next_row_index]
        self._next_row_index = self._next_row_index + 1
        return True

    def get_string(self, column_index: int, on_none: Union[Optional[str], Type[Exception]] = ValueError) -> Optional[str]:
        """
        Get the value in the specified `column_index` as a string.
        :param column_index: The column to read the value from. This uses 1 based indexes.
        :param on_none: The value to use if a null is read from the database, or an exception to raise if a null value is not supported.
        :return: The string read from the column, or the `on_none` value if there was no value.
        """
        if (column_index <= 0) or (column_index > len(self._current_row)):
            raise IndexError

        value = self._current_row[column_index - 1]
        if value is None:
            return self._value_or_raise(on_none)
        elif isinstance(value, str):
            return value
        else:
            raise ValueError

    def get_int(self, column_index: int, on_none: Union[Optional[int], Type[Exception]] = ValueError) -> Optional[int]:
        """
        Get the value in the specified `column_index` as an integer.
        :param column_index: The column to read the value from. This uses 1 based indexes.
        :param on_none: The value to use if a null is read from the database, or an exception to raise if a null value is not supported.
        :return: The integer read from the column, or the `on_none` value if there was no value.
        """
        if (column_index <= 0) or (column_index > len(self._current_row)):
            raise IndexError

        value = self._current_row[column_index - 1]
        if value is None:
            return self._value_or_raise(on_none)
        elif isinstance(value, int):
            return value
        else:
            raise ValueError

    def get_float(self, column_index: int, on_none: Union[Optional[float], Type[Exception]] = ValueError) -> Optional[float]:
        """
        Get the value in the specified `column_index` as a float.
        :param column_index: The column to read the value from. This uses 1 based indexes.
        :param on_none: The value to use if a null is read from the database, or an exception to raise if a null value is not supported.
        :return: The float read from the column, or the `on_none` value if there was no value.
        """
        if (column_index <= 0) or (column_index > len(self._current_row)):
            raise IndexError

        value = self._current_row[column_index - 1]
        if value is None:
            return self._value_or_raise(on_none)
        elif isinstance(value, float) or isinstance(value, int):
            return value
        else:
            raise ValueError

    def get_boolean(self, column_index: int, on_none: Union[Optional[bool], Type[Exception]] = ValueError) -> Optional[bool]:
        """
        Get the value in the specified `column_index` as a bool.
        :param column_index: The column to read the value from. This uses 1 based indexes.
        :param on_none: The value to use if a null is read from the database, or an exception to raise if a null value is not supported.
        :return: The bool read from the column, or the `on_none` value if there was no value.
        """
        if (column_index <= 0) or (column_index > len(self._current_row)):
            raise IndexError

        value = self._current_row[column_index - 1]
        if value is None:
            return self._value_or_raise(on_none)
        else:
            return bool(value)

    def get_instant(self, column_index: int, on_none: Union[Optional[datetime], Type[Exception]] = ValueError) -> Optional[datetime]:
        """
        Get the value in the specified `column_index` as a datetime.
        :param column_index: The column to read the value from. This uses 1 based indexes.
        :param on_none: The value to use if a null is read from the database, or an exception to raise if a null value is not supported.
        :return: The datetime read from the column, or the `on_none` value if there was no value.
        """
        value = self.get_string(column_index, None)
        if value is None:
            return self._value_or_raise(on_none)
        else:
            # The timestamp in the database uses Z for UTC while python uses +HH:mm format, and potentially has more than 6 decimals for the fractions
            # of seconds field, so only use the first 26 characters (yyyy-mm-ddThh:mm:ss.zzzzzz).
            return datetime.fromisoformat(value.rstrip('Z')[:26])

    def get_ratio(self, numerator_column_index: int, denominator_column_index: int, on_none: Union[Optional[bool], Type[Exception]] = ValueError):
        """
        Get a :class:`Ratio` using two columns: a numerator column and denominator column.

        :param numerator_column_index: The column to read the numerator from. This uses 1 based indexes.
        :param denominator_column_index: The column to read the denominator from. This uses 1 based indexes.
        :param on_none: The value to use if a null is read from the database, or an exception to raise if a null value is not supported.
        :return: The Ratio read from the column, or the `on_none` value if there was no value.
        """
        numerator = self.get_float(numerator_column_index, None)
        denominator = self.get_float(denominator_column_index, None)

        if numerator is None or denominator is None:
            return self._value_or_raise(on_none)
        else:
            # noinspection PyArgumentList
            return Ratio(numerator, denominator)

    @staticmethod
    def _value_or_raise(on_none: Union[Optional[T], Type[Exception]]) -> T:
        if type(on_none) is type and issubclass(on_none, Exception):
            raise on_none
        else:
            return on_none
