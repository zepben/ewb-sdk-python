#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from logging import Logger
from sqlite3 import Cursor
from typing import Dict, Any, Optional, Callable

from zepben.evolve.model.cim.iec61968.infiec61968.infcommon.ratio import Ratio


class SqlException(Exception):
    pass


class PreparedStatement(object):
    """
    A class giving the same functionality as the JVM PreparedStatement with the JVM SDK extensions added.
    """

    def __init__(self, sql: str, cursor: Cursor):
        self.sql: str = sql
        self._cursor: Cursor = cursor

        self._num_cols: int = self.sql.count('?')
        self._values: Dict[int, Any] = dict()

    def __str__(self):
        return f"PreparedStatement[sql={self.sql}, values={self._values}]"

    @property
    def num_columns(self):
        return self._num_cols

    @property
    def parameters(self):
        """
        Get the string representation of the current parameters set on this PreparedStatement.
        '(unset)' means this index has not yet been set.
        This function should be used for error handling and debugging only.

        Returns the string representation of all parameters that have been set on this PreparedStatement, separated by commas.
        """
        pm = []
        for i in range(1, self.num_columns + 1):
            try:
                pm.append(str(self._values[i]))
            except KeyError:
                pm.append("(unset)")
        return ", ".join(pm)

    def execute(self):
        """
        Execute this PreparedStatement using the given `cursor`.

        Throws any exception possible from `cursor.execute`, typically `sqlite3.DatabaseError`
        """
        parameters = []
        missing = []
        for i in range(1, self.num_columns + 1):
            try:
                parameters.append(self._values[i])
            except KeyError:
                missing.append(str(i))

        if missing:
            raise SqlException(f"Missing values for indices {', '.join(missing)}. Ensure all ?'s have a corresponding value in the prepared statement.")

        self._cursor.execute(self.sql, parameters)

    def add_value(self, index: int, value: Any):
        if 0 < index <= self._num_cols:
            self._values[index] = value
        else:
            raise SqlException(f"index must be between 1 and {self.num_columns} for this statement, got {index}")

    def add_ratio(self, numerator_index: int, denominator_index: int, value: Optional[Ratio]):
        if value is None:
            self.add_value(numerator_index, None)
            self.add_value(denominator_index, None)
        else:
            self.add_value(numerator_index, value.numerator)
            self.add_value(denominator_index, value.denominator)

    def try_execute_single_update(self, on_error: Optional[Callable[[Exception], None]] = None) -> bool:
        """
        Execute an update on the database with the given `query`.
        Failures will be logged as warnings.
        `query` The PreparedStatement to execute.
        `id` The mRID of the relevant object that is being saved
        `description` A description of the type of object (e.g. AcLineSegment)
        Returns True if the `execute` was successful, False otherwise.
        """
        try:
            self.execute()
            return True
        except Exception as ex:
            if on_error:
                on_error(ex)
            return False

    def log_failure(self, logger: Logger, description: str, ex: Exception):
        logger.warning(
            f"Failed to save {description}.\n" +
            f"SQL: {self}\n" +
            f"Fields: {self.parameters}\n"
            f"Additional Info: {str(ex)}"
        )

    def close(self):
        """Unused function on the Python side. Kept for compatibility with JVM side."""
        pass
