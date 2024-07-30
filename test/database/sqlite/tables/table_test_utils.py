#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import Nullable, Column


def verify_column(column: Column, query_index: int, name: str, type_: str, nullable: Nullable):
    assert column.query_index > 0
    assert column.query_index == query_index, f"{column.query_index} != {query_index}"
    assert column.name == name
    assert column.type == type_
    assert column.nullable == nullable
