#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pytest import raises

from zepben.evolve import Nullable, Column


def test_nullable_str():
    assert Nullable.NULL.sql == "NULL"
    assert Nullable.NOT_NULL.sql == "NOT NULL"
    assert Nullable.NONE.sql == ""


def test_column_constructor():
    with raises(TypeError):
        c = Column()

    with raises(ValueError, match="You cannot use a negative query index."):
        c = Column(-1, "", "")

    with raises(ValueError, match="Column Name cannot be blank"):
        c = Column(0, "", "")

    c = Column(0, "a", "b")
    assert c.query_index == 0
    assert c.name == "a"
    assert c.type == "b"
    assert str(c) == "a b"

    c = Column(9999999999999999, "test_name", "test_type", Nullable.NOT_NULL)
    assert c.query_index ==9999999999999999
    assert c.name == "test_name"
    assert c.type == "test_type"
    assert c.nullable == Nullable.NOT_NULL

    assert str(c) == "test_name test_type NOT NULL"

    with raises(ValueError, match="Column Name cannot be blank"):
        c = Column(1, " ", " ")

    with raises(ValueError, match="Column Type cannot be blank"):
        c = Column(1, "ayyy", " ")

    c = Column(1, "a", "b", Nullable.NULL)
    assert str(c) == "a b NULL"
