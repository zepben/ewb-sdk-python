#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from autoslot import dataslot
from boilerplate import *


@dataslot
class Dummy:
    mrid: str = ''

    def __repr__(self):
        return f'({self.mrid})'

@boilermaker
@dataslot
class A:

    x: int = 42

    items: List[Dummy] = ListAccessor()

    def _retype(self):
        self.items: ListRouter = ...


@boilermaker
@dataslot
class B:

    ctr: int = 0

    items: List[Dummy] = ListAccessor()

    def _retype(self):
        self.items: ListRouter = ...

    @custom_add(items)
    def add_item(self, item):
        self.ctr += 1
        self.items.append_unchecked(item)
    @custom_clear(items)
    def clear_items(self):
        self.ctr += 1
        self.items.raw.clear()
    @custom_get(items)
    def get_item(self, identifier):
        self.ctr += 1
        return self.items.raw[identifier]
    @custom_remove(items)
    def remove_item(self, item):
        self.ctr += 1
        return self.items.raw.remove(item)
    @custom_len(items)
    def num_items(self):
        return len(self.items.raw)


@boilermaker
@dataslot
class C:

    x: int = 42

    items: List[Dummy] = MRIDListAccessor()

    def _retype(self):
        self.items: MRIDListRouter = ...


@boilermaker
@dataslot
class D:

    x: int = 42

    items: List[Dummy] = MRIDDictAccessor()

    def _retype(self):
        self.items: MRIDDictRouter = ...

def eq_all(it1, it2):
    assert len(it1) == len(it2)
    assert all(e1 == e2 for e1, e2 in zip(it1, it2))

e1, e2, e3, e4 = (Dummy(str(i)) for i in range(1, 5))
e_dup = Dummy('2')

def test_collection_normal(cls):
    a = cls(items=[e3, e4])
    eq_all(a.items, [e3, e4]) # Init, extend
    a.items.append(e1)
    eq_all(a.items, [e3, e4, e1]) # add
    assert len(a.items) == 3 # len
    a.items.remove(e4)
    eq_all(a.items, [e3, e1]) # remove

def test_collection_index(cls):
    a = cls(items=[e3, e4])
    a.items.append(e1)
    assert a.items.get(1) == e4  # get

def test_collection_empty(cls):
    a = cls(items=[])
    eq_all(a.items, []) # Init, extend

    a.items.append(e1)
    eq_all(a.items, [e1]) # add

    a.items.remove(e1)
    eq_all(a.items, []) # remove

    assert len(a.items) == 0 # len
    a.items.clear()
    eq_all(a.items, []) # remove


def test_collection_custom():
    a = B(items=[e3, e4])
    eq_all(a.items, [e3, e4]) # Init, extend
    assert a.ctr == 2
    a.items.append(e1)
    eq_all(a.items, [e3, e4, e1]) # add
    assert a.ctr == 3
    assert a.items.get(1) == e4 # get
    assert a.ctr == 4
    assert len(a.items) == 3 # len
    a.items.remove(e4)
    eq_all(a.items, [e3, e1]) # remove
    assert a.ctr == 5

def test_collection_mrid(cls):
    a = cls(items=[e1, e2, e3])
    eq_all(a.items, [e1, e2, e3])

    try: a.items.append(e_dup)
    except Exception as e: assert isinstance(e, ValueError)

    try: cls(items=[e1, e2, e3, e_dup])
    except Exception as e: assert isinstance(e, ValueError)

    eq_all(a.items, [e1, e2, e3])
    assert a.items['3'] == e3
    assert a.items.get_by_mrid('3') == e3


def test_collection(cls):
    test_collection_normal(cls)
    test_collection_index(cls)
    test_collection_empty(cls)

if __name__ == '__main__':
    # TODO: Make this a pytest

    print("Running ListRouter test:")
    test_collection(A)
    print("\tPASS")

    print("Running custom impl ListRouter test:")
    test_collection_custom()
    print("\tPASS")

    print("Running MRIDListRouter test:")
    test_collection(C)
    test_collection_mrid(C)
    print("\tPASS")

    print("Running MRIDDictRouter test:")
    test_collection_normal(D)
    test_collection_empty(D)
    test_collection_mrid(D)
    print("\tPASS")



    # a.items.clear()
    # eq_all(a.items, [])
    # print(a.items)
    # a.clear_items()
    # print(a.items)
    # print(len(a.items))
