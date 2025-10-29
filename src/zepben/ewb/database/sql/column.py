#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Nullable", "Column"]

from dataclasses import dataclass
from enum import Enum


from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.util import require


class Nullable(Enum):
    NONE = ""
    NOT_NULL = "NOT NULL"
    NULL = "NULL"

    @property
    def sql(self):
        return self.value


@dataclass(slots=True)
class Column:
    query_index: int
    name: str
    type: str
    nullable: Nullable = Nullable.NONE

    def __str__(self):
        return f"{self.name} {self.type} {self.nullable.sql}".rstrip()
