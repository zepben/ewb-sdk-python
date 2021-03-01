#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

from dataclassy import dataclass

from zepben.evolve.util import require


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

    def __init__(self):
        require(self.query_index >= 0, lambda: "You cannot use a negative query index.")
        require(not self.name.isspace() and self.name, lambda: "Column Name cannot be blank.")
        require(not self.type.isspace() and self.type, lambda: "Column Type cannot be blank.")

    def __str__(self):
        return f"{self.name} {self.type} {self.nullable.sql}".rstrip()
