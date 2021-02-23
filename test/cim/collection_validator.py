#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import TypeVar, Callable

from pytest import raises

T = TypeVar("T")
U = TypeVar("U")


def validate_collection_unordered(create_it: Callable[[], T],
                                  create_other: Callable[[str, T], U],
                                  num: Callable[[int], T],
                                  get: Callable[[str], U],
                                  iterate,
                                  add: Callable[[U], T],
                                  remove: Callable[[U], T],
                                  clear: Callable[[T], T]):
    it = create_it()
    other1 = create_other("1", it)
    other2 = create_other("2", it)
    other3 = create_other("3", it)
    duplicate = create_other("1", it)
    assert other1 != other2
    assert other1 != other3
    assert other2 != other3
    assert num(it) == 0

    add(it, other1)
    add(it, other2)
    add(it, other3)
    assert num(it) == 3

    with raises(ValueError, match=f"An? (current )?{other1.__class__.__name__} with mRID {other1.mrid} already exists in {str(it)}"):
        add(it, duplicate)

    assert num(it) == 3
    assert remove(it, other1)

    with raises(ValueError):
        remove(it, other1)

    with raises(ValueError):
        remove(it, None)

    assert num(it) == 2

    assert get(it, other2.mrid) == other2

    assert other2 in [x for x in iterate(it)]
    assert other3 in [x for x in iterate(it)]

    clear(it)
    assert num(it) == 0

    # Make sure you can add an item back after it has been removed
    add(it, other1)
    assert num(it) == 1

    remove(it, other1)
    assert num(it) == 0

    # Make sure remove on an empty list raises an exception.
    with raises(ValueError):
        remove(it, other2)
    assert num(it) == 0

