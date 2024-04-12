#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["BaseServiceWriter"]

from abc import ABC, abstractmethod
from typing import Callable, Type

from zepben.evolve.database.sqlite.common.base_cim_writer import BaseCimWriter
from zepben.evolve.database.sqlite.common.base_collection_writer import BaseCollectionWriter
from zepben.evolve.model.cim.iec61970.base.core.identified_object import TIdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.services.common.base_service import BaseService


class BaseServiceWriter(BaseCollectionWriter, ABC):
    """
    A base class for writing object from a [BaseService] into the database.

    :param service: The `BaseService` to save to the database.
    :param writer: The `BaseServiceWriter` used to actually write the objects to the database.
    """

    def __init__(self, service: BaseService, writer: BaseCimWriter):
        super().__init__()
        self._service: BaseService = service
        """
        The `BaseService` to save to the database.
        """

        self._writer: BaseCimWriter = writer
        """
        The `BaseServiceWriter` used to actually write the objects to the database.
        """

    def save(self) -> bool:
        return all([self._save_name_types(), self._do_save()])

    @abstractmethod
    def _do_save(self) -> bool:
        """
        Save the service specific objects to the database.

        :return: True if the objects were successfully saved to the database, otherwise False
        """

    """
    Save each object of the specified type using the provided `saver`.
    
    @param T The type of object to save to the database.
    @param saver The callback used to save the objects to the database. Will be called once for each object and should return True if the object is
      successfully saved to the database.
    
    :return: True if all objects are successfully saved to the database, otherwise False.
    """

    def _save_each_object(self, type_: Type[TIdentifiedObject], saver: Callable[[TIdentifiedObject], bool]) -> bool:
        status = True
        for it in self._service.objects(type_):
            status = status and self._validate_save_object(it, saver)

        return status

    """
    Validate that an object is actually saved to the database, logging an error if anything goes wrong.
    
    @param T The type of object being saved.
    @param it The object being saved.
    @param saver The callback actually saving the object to the database.
    
    :return: True if the object is successfully saved to the database, otherwise False.
    """

    def _validate_save_object(self, it: TIdentifiedObject, saver: Callable[[TIdentifiedObject], bool]) -> bool:
        def log_error(e: Exception):
            self._logger.error(f"Failed to save {it.__class__.__name__} {it.name} [{it.mrid}]: {e}")

        return self._validate_save(it, saver, log_error)

    def _save_name_types(self) -> bool:
        status = True

        for it in self._service.name_types:
            status = all([status, self._validate_save_name_type(it, self._writer.save_name_type)])

            for name in it.names:
                status = all([status, self._validate_save_name(name, self._writer.save_name)])

        return status

    def _validate_save_name_type(self, name_type: NameType, saver: Callable[[NameType], bool]) -> bool:
        def log_error(e: Exception):
            self._logger.error(f"Failed to save {name_type.__class__.__name__} {name_type.name}: {e}")

        return self._validate_save(name_type, saver, log_error)

    def _validate_save_name(self, name: Name, saver: Callable[[Name], bool]) -> bool:
        def log_error(e: Exception):
            self._logger.error(f"Failed to save {name.__class__.__name__} {name.name}: {e}")

        return self._validate_save(name, saver, log_error)
