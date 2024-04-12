#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["BaseCollectionWriter"]

import logging
from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Iterable

from zepben.evolve.database.sqlite.extensions.prepared_statement import SqlException

T = TypeVar("T")


class BaseCollectionWriter(ABC):
    """
    A base class for writing collections of object collections to a database.
    """

    def __init__(self):
        super().__init__()
        self._logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        """
        The logger to use for this collection writer.
        """

    @abstractmethod
    def save(self) -> bool:
        """
        Save all the objects for the available collections.

        :return: True if the save was successful, otherwise False.
        """
        pass

    def _save_each(self, items: Iterable[T], saver: Callable[[T], bool], on_save_failure: Callable[[T, Exception], None]) -> bool:
        """
        Save each of the [items] to the database.

        NOTE: This function does not short circuit and all items will be attempted, even if one fails.

        :param items: The collection of items to save.
        :param saver: A callback for saving each object to the database.
        :param on_save_failure: A callback that should be used to indicate there was a failure in the `saver`. You should pass the object that was being saved,
          and the exception that caused the failure.

        :return: True if all `items` were successfully saved, otherwise False.
        """
        status = True

        for it in items:
            status = self._validate_save(it, saver, lambda e: on_save_failure(it, e)) and status

        return status

    @staticmethod
    def _validate_save(it: T, saver: [[T], bool], on_save_failure: [[Exception], None]) -> bool:
        """
        Validate that a save actually works, and convert all exceptions into failures with a callback.

        :param it: The object instance to save.
        :param saver: The callback that will save the object to the database.
        :param on_save_failure: A callback if an exception was thrown by the [saver].

        :return: True if the saver successfully saved the object to the database, otherwise False.
        """
        try:
            return saver(it)
        except SqlException as e:
            on_save_failure(e)
            return False
