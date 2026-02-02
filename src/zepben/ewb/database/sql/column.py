#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Nullable", "Column"]

from enum import Enum

from dataclasses import dataclass
from zepben.ewb.util import require


class Nullable(Enum):
    NONE = ""
    NOT_NULL = "NOT NULL"
    NULL = "NULL"

    @property
    def sql(self):
        return self.value


class Type(Enum):
    STRING = "TEXT"
    INTEGER = "INTEGER"
    DOUBLE = "NUMBER"
    BOOLEAN = "BOOLEAN"
    UUID = "TEXT"
    TIMESTAMP = "TEXT"
    BYTES = "BLOB"


@dataclass(slots=True)
class Column:
    query_index: int
    name: str
    type: str | Type
    """Deprecated, use `type` instead"""
    nullable: Nullable = Nullable.NONE

    def __post_init__(self):
        require(self.query_index >= 0, lambda: "You cannot use a negative query index.")
        if not isinstance(self.type, Type):
            DeprecationWarning("Passing strings directly to Column is being phased out, use the Type enum instead.")
            require(not self.name.isspace() and self.name, lambda: "Column Name cannot be blank.")
            require(not self.type.isspace() and self.type, lambda: "Column Type cannot be blank.")
            # FIXME: We should accept isinstance(self.type, Type) from here on.

    def __str__(self):
        if isinstance(self.type, Type):
            return f"{self.name} {self.type.value} {self.nullable.sql}".rstrip()
        return f"{self.name} {self.type} {self.nullable.sql}".rstrip()
