#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import field
from typing import List

import pytest

from zepben.ewb.dataslot import *


@dataslot(eq=True)
class DsBuiltins:
    i: int = field(default=42, kw_only=False)
    f: float = field(default=2.4, kw_only=False)
    s: str = 'abc'
    b: bool = field(default=True, compare=False)

def test_builtin_attrs():
    def assert_all_are_default(obj_):
        assert obj_.i == 42
        assert obj_.f == 2.4
        assert obj_.s == 'abc'
        assert obj_.b == True
    # Test default and kwargs input;
    obj = DsBuiltins()
    other = DsBuiltins(i = 42, f = 2.4, s = 'abc', b = True)
    assert_all_are_default(obj)
    assert_all_are_default(other)

    # Test whether attribute assignments modify the fields;
    obj.i = 24
    assert obj.i == 24
    # Test whether attribute assignments don't have side effects for other objects
    assert_all_are_default(other)

    obj.f = 4.2
    assert obj.f == 4.2
    assert_all_are_default(other)

    obj.s = 'cba'
    assert obj.s == 'cba'
    assert_all_are_default(other)

    obj.b = False
    assert obj.b == False
    assert_all_are_default(other)

def test_eq():
    # Test generated equality for all fields;
    obj = DsBuiltins()
    other = DsBuiltins(i=42, f=2.4, s='abc', b=True)
    assert obj == other

    # Test eq=False fields don't affect equality
    obj.b = not obj.b
    assert obj == other

    # Test modifying a field breaks equality;
    obj.i = 24
    assert obj != other

def test_kwargs():
    # Test arg/kwarg parity
    obj = DsBuiltins(42, 2.4, s = 'abc', b = True)
    other = DsBuiltins(i = 42, f = 2.4, s = 'abc', b = True)
    assert obj == other

    # Test kwonly fields raise TypeError
    with pytest.raises(TypeError):
        _ = DsBuiltins(42, 2.4, 'abc', b=True)


class Dummy:
    def __init__(self, x: int=42):
        self.x = x

    def __eq__(self, other):
        return isinstance(other, Dummy) and self.x == other.x

@dataslot
class DsInstantiated:
    L: List[int] = instantiate(list)
    d: Dummy = instantiate(Dummy)

def test_instantiation():
    obj = DsInstantiated()
    # Test custom values don't override defaults instantiations
    other1 = DsInstantiated(L=[2, 3], d=Dummy(24))
    # Test memory is not shared between default instantiations
    other2 = DsInstantiated()

    # Test for builtin list
    assert obj.L == []
    assert other1.L == [2, 3]
    assert other2.L == []

    obj.L.append(8)
    other2.L.append(9)

    assert obj.L == [8]
    assert other1.L == [2, 3]
    assert other2.L == [9]

    # Test for custom class instance
    assert obj.d == Dummy(42)
    assert other1.d == Dummy(24)
    assert other2.d == Dummy(42)

    obj.d.x = 8
    other2.d.x = 9

    assert obj.d == Dummy(8)
    assert other1.d == Dummy(24)
    assert other2.d == Dummy(9)

@dataslot
class DsHashed:
    x: int = 42
    s: str = "abcd"

    def __hash__(self):
        return self.x.__hash__()

@dataslot
class DsHashedChild(DsHashed):
    y: int = 24

def test_hash():
    # Test hash only includes relevant field
    obj = DsHashed(x=42, s='a')
    other = DsHashed(x=42, s='b')
    assert hash(obj) == hash(other)

    # Test hash on specific field
    other.x = 24
    assert hash(obj) != hash(other)

    obj = DsHashedChild(x=42, s='a', y=8)
    other = DsHashedChild(x=42, s='b', y=9)
    assert hash(obj) == hash(other)

    # Test hash on specific field
    other.x = 24
    assert hash(obj) != hash(other)