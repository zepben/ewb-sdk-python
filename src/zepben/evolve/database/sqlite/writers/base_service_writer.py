#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from typing import Callable, TypeVar, Generic

from dataclassy import dataclass

from zepben.evolve import BaseService, BaseCIMWriter, NameType, Name, IdentifiedObject
from zepben.evolve.database.sqlite.writers.utils import validate_save

logger = logging.getLogger("service_writer")

T = TypeVar("T", bound=BaseService)
W = TypeVar("W", bound=BaseCIMWriter)
S = TypeVar("S", bound=IdentifiedObject)


@dataclass(slots=True)
class BaseServiceWriter(Generic[T, W]):
    has_common: Callable[[str], bool]
    add_common: Callable[[str], bool]

    def save(self, service: T, writer: W) -> bool:
        status = True

        for name_type in service.name_types:
            type_name_id = f"NameType:{name_type.name}"
            if not self.has_common(type_name_id):
                status = status and (self._validate_save_name_type(name_type, writer.save_name_type) and self.add_common(type_name_id))

            for name in name_type.names:
                name_id = f"Name:{name.type.name}:{name.name}:{name.identified_object.mrid}"
                if not self.has_common(name_id):
                    status = status and (self._validate_save_name(name, writer.save_name) and self.add_common(name_id))

        return status

    def try_save_common(self, save: Callable[[S], bool], obj: S) -> bool:
        if self.has_common(obj.mrid):
            return True

        if not self.validate_save(obj, save):
            return False

        return self.add_common(obj.mrid)

    def validate_save(self, it: S, saver: Callable[[S], bool]) -> bool:
        return validate_save(it, saver, lambda e: logger.error(f"Failed to save {it}: {e.message}"))

    def _validate_save_name_type(self, name_type: NameType, saver: Callable[[NameType], bool]) -> bool:
        return validate_save(name_type, saver, lambda e: logger.error(f"Failed to save {name_type.__class__.__name__} {name_type.name}: {e.message}"))

    def _validate_save_name(self, name: Name, saver: Callable[[Name], bool]) -> bool:
        return validate_save(name, saver, lambda e: logger.error(f"Failed to save {name.__class__.__name__} {name.name}: {e.message}"))
