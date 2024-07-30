#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter
from typing import TypeVar, Callable, Type, Optional

from pytest import raises

from zepben.evolve import IdentifiedObject

T = TypeVar("T", bound=IdentifiedObject)
U = TypeVar("U", bound=IdentifiedObject)
V = TypeVar("V")
E = TypeVar("E", bound=Exception)


#
# NOTE: The callables below that use `...` do so to work around bugs in the type checking of both the IDE and mypy.
#       Ideally they should have `get: Callable[[T, str]], U]`, `add: Callable[[T, U], T]` and `remove: Callable[[T, U], T]`
#
def validate_collection(create_it: Callable[[], T],
                        create_other: Callable[[str, T], U],
                        num: Callable[[T], int],
                        get: Callable[[T, U], U],
                        get_all: property,
                        add: Callable[..., T],
                        remove: Callable[..., T],
                        clear: Callable[[T], T],
                        expected_error_message: Callable[[T, U], str],
                        expected_remove_error: Type[E] = ValueError,
                        support_duplicates: bool = True):
    it = create_it()
    other1 = create_other("1", it)
    other2 = create_other("2", it)
    other3 = create_other("3", it)
    duplicate = create_other("2", it)
    assert other1 != other2
    assert other1 != other3
    assert other2 != other3
    assert num(it) == 0

    add(it, other1)
    add(it, other2)
    add(it, other3)
    assert num(it) == 3

    with raises(ValueError, match=expected_error_message(it, duplicate)):
        add(it, duplicate)

    assert num(it) == 3
    assert remove(it, other1)

    with raises(expected_remove_error):
        remove(it, other1)

    with raises(expected_remove_error):
        remove(it, None)

    assert num(it) == 2

    assert get(it, duplicate) == other2

    # noinspection PyArgumentList
    all_objects = list(get_all.fget(it))
    assert other2 in all_objects
    assert other3 in all_objects

    clear(it)
    assert num(it) == 0

    # Make sure you can add an item back after it has been removed
    add(it, other1)
    assert num(it) == 1

    if support_duplicates:
        # Make sure adding an already-added item does not change the collection
        add(it, other1)
        assert num(it) == 1

    remove(it, other1)
    assert num(it) == 0

    # Make sure remove on an empty list raises an exception.
    with raises(expected_remove_error):
        remove(it, other2)
    assert num(it) == 0


def validate_identified_object_name_collection(create_it: Callable[[], T],
                                               create_other: Callable[[str, T], U],
                                               num: Callable[[T], int],
                                               get: Callable[[T, U], U],
                                               get_all_with_type: Callable[[T], T],
                                               get_all: property,
                                               add: Callable[..., T],
                                               remove: Callable[..., T],
                                               clear: Callable[[T], T],
                                               expected_error_message: Callable[[T, U], str],
                                               expected_remove_error: Type[E] = ValueError,
                                               support_duplicates: bool = True):
    it = create_it()
    other1 = create_other("1", it)
    other2 = create_other("2", it)
    other3 = create_other("3", it)
    duplicate = create_other("2", it)
    assert other1 != other2
    assert other1 != other3
    assert other2 != other3
    assert num(it) == 0

    add(it, other1.name, other1.type)
    add(it, other2.name, other2.type)
    add(it, other3.name, other3.type)
    assert num(it) == 3

    assert Counter(get_all_with_type(it, other1.type.name)) == Counter([other1, other2, other3])
    assert Counter(get_all_with_type(it, other1.type)) == Counter([other1, other2, other3])

    with raises(ValueError, match=expected_error_message(it, duplicate.name)):
        add(it, duplicate.name, duplicate.type)

    assert num(it) == 3
    assert remove(it, other1)

    with raises(expected_remove_error):
        remove(it, other1)

    with raises(expected_remove_error):
        remove(it, None)

    assert num(it) == 2

    assert get(it, duplicate) == other2

    # noinspection PyArgumentList
    all_objects = list(get_all.fget(it))
    assert other2 in all_objects
    assert other3 in all_objects

    clear(it)
    assert num(it) == 0

    # Make sure you can add an item back after it has been removed
    add(it, other1.name, other1.type)
    assert num(it) == 1

    if support_duplicates:
        # Make sure adding an already-added item does not change the collection
        add(it, other1.name, other1.type)
        assert num(it) == 1

    remove(it, other1)
    assert num(it) == 0

    # Make sure remove on an empty list raises an exception.
    with raises(expected_remove_error):
        remove(it, other2)
    assert num(it) == 0


#
# NOTE: The callables below that use `...` do so to work around bugs in the type checking of both the IDE and mypy.
#       Ideally they should have `get: Callable[[T, str], U]`, `add: Callable[[T, U], T]` and `remove: Callable[[T, U], T]`
#
def validate_collection_unordered(create_it: Callable[[], T],
                                  create_other: Callable[[str, T], U],
                                  num: Callable[[T], int],
                                  get: Callable[..., U],
                                  get_all: property,
                                  add: Callable[..., T],
                                  remove: Callable[..., T],
                                  clear: Callable[[T], T],
                                  expected_remove_error: Type[E] = ValueError):
    validate_collection(
        create_it,
        create_other,
        num,
        lambda it, other: get(it, other.mrid),
        get_all,
        add,
        remove,
        clear,
        lambda it, dup: rf"An? (current )?{dup.__class__.__name__} with mRID {dup.mrid} already exists in {str(it)}",
        expected_remove_error)


#
# NOTE: The callables below that use `...` do so to work around bugs in the type checking of both the IDE and mypy.
#       Ideally they should have `get: Callable[[T, int], Optional[V]]`, `add: Callable[[T, V], T]`, `add_with_index: Callable[[T, V, int], T]`
#       and `remove: Callable[[T, Optional[V]], T]`
#
def validate_collection_ordered(create_it: Callable[[], T],
                                create_other: Callable[[int, T], V],
                                num: Callable[[T], int],
                                get: Callable[..., Optional[V]],
                                get_all: property,
                                add: Callable[..., T],
                                add_with_index: Callable[..., T],
                                remove: Callable[..., T],
                                clear: Callable[[T], T]):
    it = create_it()
    other1 = create_other(1, it)
    other2 = create_other(2, it)
    other3 = create_other(3, it)

    if isinstance(other1, IdentifiedObject):
        raise ValueError("do not use this function with identified 'other', use one of the other variants instead.")

    assert other1 != other2
    assert other1 != other3
    assert other2 != other3

    assert num(it) == 0

    add(it, other1)
    add(it, other2)
    add(it, other3)
    assert num(it) == 3

    # Non-identified objects can be added more than once
    add(it, other1)
    add_with_index(it, other1, 1)
    assert num(it) == 5

    assert remove(it, other2)
    with raises(ValueError):
        remove(it, other2)
    with raises(ValueError):
        remove(it, None)
    assert num(it) == 4

    assert get(it, 2) == other3

    # noinspection PyArgumentList
    assert list(get_all.fget(it)) == [other1, other1, other3, other1]

    clear(it)
    assert num(it) == 0

    # Make sure you can add an item back after it has been removed
    add(it, other2)
    assert num(it) == 1

    with raises(Exception, match=rf"Unable to add {other3.__class__.__name__} to {str(it)}. \w* number 20 is invalid. Expected "
                                 rf"a value between 0 and {num(it)}. Make sure you are adding the \w* in the correct order and "
                                 rf"there are no gaps in the numbering."):
        add_with_index(it, other3, 20)

    remove(it, other2)
    assert num(it) == 0

    # Make sure you can call remove on an empty list.
    with raises(ValueError):
        remove(it, other2)
    assert num(it) == 0
