#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from abc import ABC

from zepben.evolve.database.sqlite.extensions.prepared_statement import PreparedStatement

__all__ = ["BaseEntryWriter"]


class BaseEntryWriter(ABC):
    """
    A base class for writing entries into tables of the database.
    """

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def _try_execute_single_update(self, prepared_statement: PreparedStatement, description: str) -> bool:
        """
        Helper function for writing the entry to the database and logging any failures.

        :param prepared_statement: The `PreparedStatement` to execute.
        :param description: A description of the object being written to use for logging of failures.
        :return: True if the entry was successfully written to the database, otherwise False.
        """
        def log_failure(ex: Exception):
            prepared_statement.log_failure(self._logger, description, ex)

        return prepared_statement.try_execute_single_update(log_failure)
