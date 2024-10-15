#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re
from collections import Counter
from typing import TypeVar, Callable, Generator, List, Dict, Union, Type, Tuple

import pytest

from zepben.evolve import IdentifiedObject, TIdentifiedObject

UIdentifiedObject = TypeVar("UIdentifiedObject", bound=IdentifiedObject)
UOther = TypeVar("UOther")
K = TypeVar("K")

_U = Union[UIdentifiedObject, UOther]


def validate_unordered_1234567890(
    create_it: Callable[[], TIdentifiedObject],
    create_other: Callable[[str], UIdentifiedObject],
    get_all: property,  # Callable[[TIdentifiedObject], Generator[UIdentifiedObject, None, None]]
    num: Callable[..., int],  # Callable[[TIdentifiedObject], int]
    get_by_id: Callable[..., UIdentifiedObject],  # Callable[[TIdentifiedObject, str], UIdentifiedObject]
    add: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UIdentifiedObject], TIdentifiedObject]
    remove: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UIdentifiedObject], TIdentifiedObject]
    clear: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject], TIdentifiedObject]
):
    """
    Validate the internal collection for an associated :class:`IdentifiedObject` that has no order significance.

    NOTE: The callables using `...` do so to work around bugs in the type checking of both the IDE and mypy, where passing a reference to the
          class method doesn't recognise it needs the `self` parameter, and therefore marks the parameter as having the incorrect type. Actual
          signatures are stored in comments against the arguments.
    """
    _validate_unordered(create_it, create_other, get_all.fget, num, get_by_id, add, remove, clear)


def validate_unordered_other_1234567890(
    create_it: Callable[[], TIdentifiedObject],
    create_other: Callable[[int], UOther],
    get_all: property,  # Callable[[TIdentifiedObject], Generator[UOther, None, None]]
    num: Callable[..., int],  # Callable[[TIdentifiedObject], int]
    get_by_key: Callable[..., UOther],  # Callable[[TIdentifiedObject, K], UOther]
    add: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UOther], TIdentifiedObject]
    remove: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UOther], TIdentifiedObject]
    clear: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject], TIdentifiedObject]
    get_key: Callable[..., K],  # Callable[[UOther], K]
    key_to_str: Callable[[K], str] = str
):
    """
    Validate the internal collection for an associated object that is not an [IdentifiedObject] that has no order significance.

    NOTE: The callables using `...` do so to work around bugs in the type checking of both the IDE and mypy, where passing a reference to the
          class method doesn't recognise it needs the `self` parameter, and therefore marks the parameter as having the incorrect type. Actual
          signatures are stored in comments against the arguments.
    """
    _validate_unordered_other(create_it, create_other, get_all.fget, num, get_by_key, add, remove, clear, get_key, key_to_str)


def validate_ordered_1234567890(
    create_it: Callable[[], TIdentifiedObject],
    create_other: Callable[[str, int], UIdentifiedObject],
    get_all: property,  # Callable[[TIdentifiedObject], Generator[UIdentifiedObject, None, None]]
    num: Callable[..., int],  # Callable[[TIdentifiedObject], int]
    get_by_id: Callable[..., UIdentifiedObject],  # Callable[[TIdentifiedObject, str], UIdentifiedObject]
    get_by_index: Callable[..., UIdentifiedObject],  # Callable[[TIdentifiedObject, int], UIdentifiedObject]
    add: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UIdentifiedObject], TIdentifiedObject]
    remove: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UIdentifiedObject], TIdentifiedObject]
    clear: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject], TIdentifiedObject]
    index_of: Callable[..., int],  # Callable[[UIdentifiedObject], int]
):
    """
    Validate the internal collection for an associated :class:`IdentifiedObject` that has order significance, baked into the object itself, not just
    the placement in the collection.

    NOTE: Baked in index is expected to be 1-based, not 0-based.

    NOTE: The callables using `...` do so to work around bugs in the type checking of both the IDE and mypy, where passing a reference to the
          class method doesn't recognise it needs the `self` parameter, and therefore marks the parameter as having the incorrect type. Actual
          signatures are stored in comments against the arguments.
    """
    _validate_ordered(create_it, create_other, get_all.fget, num, get_by_id, get_by_index, add, remove, clear, index_of)


def validate_ordered_other_1234567890(
    create_it: Callable[[], TIdentifiedObject],
    create_other: Callable[[int], UOther],
    get_all: property,  # Callable[[TIdentifiedObject], Generator[UOther, None, None]]
    num: Callable[..., int],  # Callable[[TIdentifiedObject], int]
    get_by_index: Callable[..., UOther],  # Callable[[TIdentifiedObject, int], UOther]
    for_each: Callable[..., None],  # Callable[[TIdentifiedObject, Callable[[int, UOther], None]], None]
    add: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UOther], TIdentifiedObject]
    add_with_index: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UOther, int], TIdentifiedObject]
    remove: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UOther], TIdentifiedObject]
    remove_at_index: Callable[..., UOther],  # Callable[[TIdentifiedObject, int], UOther]
    clear: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject], TIdentifiedObject]
):
    """
    Validate the internal collection for an associated object that is not an :class:`IdentifiedObject` that has order significance.

    NOTE: Positional index is expected to be 0-based, not 1-based.

    NOTE: The callables using `...` do so to work around bugs in the type checking of both the IDE and mypy, where passing a reference to the
          class method doesn't recognise it needs the `self` parameter, and therefore marks the parameter as having the incorrect type. Actual
          signatures are stored in comments against the arguments.
    """
    _validate_ordered_other(create_it, create_other, get_all.fget, num, get_by_index, for_each, add, add_with_index, remove, remove_at_index, clear)


def _validate_unordered(
    create_it: Callable[[], TIdentifiedObject],
    create_other: Callable[[str], UIdentifiedObject],
    get_all: Callable[[TIdentifiedObject], Generator[UIdentifiedObject, None, None]],
    num: Callable[[TIdentifiedObject], int],
    get_by_id: Callable[[TIdentifiedObject, str], UIdentifiedObject],
    add: Callable[[TIdentifiedObject, UIdentifiedObject], TIdentifiedObject],
    remove: Callable[[TIdentifiedObject, UIdentifiedObject], TIdentifiedObject],
    clear: Callable[[TIdentifiedObject], TIdentifiedObject]
):
    """
    Validate the internal collection for an associated :class:`IdentifiedObject` that has no order significance.

    NOTE: The callables using `...` do so to work around bugs in the type checking of both the IDE and mypy, where passing a reference to the
          class method doesn't recognise it needs the `self` parameter, and therefore marks the parameter as having the incorrect type. Actual
          signatures are stored in comments against the arguments.
    """
    it = create_it()
    other1 = create_other("1")
    other2 = create_other("2")
    other3 = create_other("3")
    duplicate1 = create_other("1")

    expected_duplicate_errors = {
        duplicate1: rf"An? (current )?{other1.__class__.__name__} with mRID {other1.mrid} already exists in {re.escape(str(it))}"
    }

    def validate_before_removal():
        assert get_by_id(it, "1") == other1
        assert get_by_id(it, "2") == other2

    def validate_after_removal():
        with pytest.raises(KeyError):
            get_by_id(it, "1")
        assert get_by_id(it, "2") == other2

    _validate(
        it,
        [other1, other2, other3],
        get_all,
        num,
        add,
        remove,
        clear,
        validate_collection=_assert_unordered,
        perform_duplicate_validation=_create_duplicates_throw_validator(it, expected_duplicate_errors, add),
        before_removal_validation=validate_before_removal,
        after_removal_validation=validate_after_removal,
        others_have_order=False
    )


#
# NOTE: The callables using `...` do so to work around bugs in the type checking of both the IDE and mypy, where passing a reference to the
#       class method doesn't recognise it needs the `self` parameter, and therefore marks the parameter as having the incorrect type. Actual
#       signatures are stored in comments against the arguments.
#
def _validate_unordered_other(
    create_it: Callable[[], TIdentifiedObject],
    create_other: Callable[[int], UOther],
    get_all: Callable[[TIdentifiedObject], Generator[UOther, None, None]],
    num: Callable[..., int],  # Callable[[TIdentifiedObject], int]
    get_by_key: Callable[..., UOther],  # Callable[[TIdentifiedObject, K], UOther]
    add: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UOther], TIdentifiedObject]
    remove: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject, UOther], TIdentifiedObject]
    clear: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject], TIdentifiedObject]
    get_key: Callable[..., K],  # Callable[[UOther], K]
    key_to_str: Callable[[K], str] = str
):
    """
    Validate the internal collection for an associated object that is not an [IdentifiedObject] that has no order significance.
    """
    it = create_it()
    other1 = create_other(1)
    other2 = create_other(2)
    other3 = create_other(3)
    other_duplicate_key = create_other(1)

    if isinstance(other1, IdentifiedObject):
        raise ValueError("do not use this function with identified 'other', use one of the other variants instead.")

    # Just check that the duplicate key is in the error message.
    expected_duplicate_errors = {
        # NOTE: We use key_to_str to allow us to customise how a key is presented. e.g. for enums we want only the name, not the class.
        other_duplicate_key: rf".*{re.escape(key_to_str(get_key(other_duplicate_key)))}.*"
    }

    def validate_before_removal():
        assert get_by_key(it, get_key(other1)) == other1
        assert get_by_key(it, get_key(other2)) == other2

    def validate_after_removal():
        with pytest.raises(KeyError):
            get_by_key(it, get_key(other1))
        assert get_by_key(it, get_key(other2)) == other2

    _validate(
        it,
        [other1, other2, other3],
        get_all,
        num,
        add,
        remove,
        clear,
        validate_collection=_assert_unordered,
        perform_duplicate_validation=_create_duplicates_throw_validator(it, expected_duplicate_errors, add),
        before_removal_validation=validate_before_removal,
        after_removal_validation=validate_after_removal,
        others_have_order=False
    )


#
# NOTE: The callables using `...` do so to work around bugs in the type checking of both the IDE and mypy, where passing a reference to the
#       class method doesn't recognise it needs the `self` parameter, and therefore marks the parameter as having the incorrect type. Actual
#       signatures are stored in comments against the arguments.
#
def _validate_ordered(
    create_it: Callable[[], TIdentifiedObject],
    create_other: Callable[[str, int], UIdentifiedObject],
    get_all: Callable[[TIdentifiedObject], Generator[UIdentifiedObject, None, None]],
    num: Callable[..., int],  # Callable[[TIdentifiedObject], int]
    get_by_id: Callable[[..., str], UIdentifiedObject],  # Callable[[TIdentifiedObject, str], UIdentifiedObject]
    get_by_index: Callable[[..., int], UIdentifiedObject],  # Callable[[TIdentifiedObject, int], UIdentifiedObject]
    add: Callable[[..., UIdentifiedObject], TIdentifiedObject],  # Callable[[TIdentifiedObject, UIdentifiedObject], TIdentifiedObject]
    remove: Callable[[..., UIdentifiedObject], TIdentifiedObject],  # Callable[[TIdentifiedObject, UIdentifiedObject], TIdentifiedObject]
    clear: Callable[..., TIdentifiedObject],  # Callable[[TIdentifiedObject], TIdentifiedObject]
    index_of: Callable[..., int],  # Callable[[UIdentifiedObject], int]
):
    """
    Validate the internal collection for an associated :class:`IdentifiedObject` that has order significance, baked into the object itself, not just
    the placement in the collection.

    NOTE: Baked in index is expected to be 1-based, not 0-based.
    """
    it = create_it()
    other1 = create_other("1", 1)
    other2 = create_other("2", 2)
    other_auto = create_other("3", 0)
    other_duplicate_id = create_other("1", 4)
    other_duplicate_index = create_other("4", 1)

    assert [index_of(o) for o in [other1, other2, other_auto, other_duplicate_id, other_duplicate_index]] == [1, 2, 0, 4, 1]

    expected_duplicate_errors = {
        other_duplicate_id: rf"An? (current )?{other1.__class__.__name__} with mRID {other1.mrid} already exists in {re.escape(str(it))}",
        other_duplicate_index: rf"Unable to add {re.escape(str(other_duplicate_index))} to {re.escape(str(it))}. A {re.escape(str(other1))} already exists with \w+ 1."
    }

    def validate_before_removal():
        assert get_by_id(it, other1.mrid) == other1
        assert get_by_id(it, other2.mrid) == other2

        # Adding the auto indexed object should have set its index, which was 0 above.
        assert index_of(other_auto) == 3

        # We should be able to get each item by its index, and nulls for invalid indexes.
        with pytest.raises(IndexError):
            get_by_index(it, 0)
        assert get_by_index(it, 1) == other1
        assert get_by_index(it, 2) == other2
        assert get_by_index(it, 3) == other_auto
        with pytest.raises(IndexError):
            get_by_index(it, 4)

    def validate_after_removal():
        with pytest.raises(KeyError):
            get_by_id(it, other1.mrid)
        assert get_by_id(it, other2.mrid) == other2

        with pytest.raises(IndexError):
            get_by_index(it, 1)
        assert get_by_index(it, 2) == other2

    _validate(
        it,
        [other1, other2, other_auto],
        get_all,
        num,
        add,
        remove,
        clear,
        validate_collection=_assert_ordered,
        perform_duplicate_validation=_create_duplicates_throw_validator(it, expected_duplicate_errors, add),
        before_removal_validation=validate_before_removal,
        after_removal_validation=validate_after_removal,
        others_have_order=True
    )


def _validate_ordered_other(
    create_it: Callable[[], TIdentifiedObject],
    create_other: Callable[[int], UOther],
    get_all: Callable[[TIdentifiedObject], Generator[UOther, None, None]],
    num: Callable[[TIdentifiedObject], int],
    get_by_index: Callable[[TIdentifiedObject, int], UOther],
    for_each: Callable[[TIdentifiedObject, Callable[[int, UOther], None]], None],
    add: Callable[[TIdentifiedObject, UOther], TIdentifiedObject],
    add_with_index: Callable[[TIdentifiedObject, UOther, int], TIdentifiedObject],
    remove: Callable[[TIdentifiedObject, UOther], TIdentifiedObject],
    remove_at_index: Callable[[TIdentifiedObject, int], UOther],
    clear: Callable[[TIdentifiedObject], TIdentifiedObject],
):
    it = create_it()
    other1 = create_other(1)
    other2 = create_other(2)
    other3 = create_other(3)
    others = [other1, other2, other3]

    assert not isinstance(other1, IdentifiedObject), "do not use this function with identified 'other', use one of the `validate_ordered` instead."

    looped = []

    def on_each(index: int, item: UOther):
        assert index == len(looped)
        looped.append(item)

    def validate_before_removal():
        for_each(it, on_each)
        assert looped == [other1, other2, other3]

        other4 = create_other(4)
        add_with_index(it, other4, 1)

        assert num(it) == 4
        assert list(get_all(it)) == [other1, other4, other2, other3]
        assert get_by_index(it, 1) == other4

        # Put the collection back to how it was before we added the duplicate for future tests.
        assert remove_at_index(it, 1) == other4

        # Adding to an invalid index is not valid.
        expected_message = (
            rf"Unable to add {other4.__class__.__name__} to {it}. \w* number 5 is invalid. Expected a value between 0 and {num(it)}. "
            "Make sure you are adding the items in order and there are no gaps in the numbering."
        )
        with pytest.raises(ValueError, match=expected_message):
            add_with_index(it, other4, 5)

        # Python has reverse index support
        with pytest.raises(IndexError):
            get_by_index(it, -4)
        assert get_by_index(it, -3) == other1
        assert get_by_index(it, -2) == other2
        assert get_by_index(it, -1) == other3

        assert get_by_index(it, 0) == other1
        assert get_by_index(it, 1) == other2
        assert get_by_index(it, 2) == other3
        with pytest.raises(IndexError):
            assert get_by_index(it, 3)

        # Removing an invalid index throws an exception in the python library.
        with pytest.raises(IndexError):
            assert remove_at_index(it, 5)

    def validate_after_removal():
        with pytest.raises(IndexError):
            assert get_by_index(it, -3)
        assert get_by_index(it, 0) == other2
        assert get_by_index(it, 1) == other3
        with pytest.raises(IndexError):
            assert get_by_index(it, 2)

    _validate(
        it,
        others,
        get_all,
        num,
        add,
        remove,
        clear,
        validate_collection=_assert_ordered,
        perform_duplicate_validation=_create_duplicates_supported_validator(it, others, get_all, num, add, remove, _assert_ordered),
        before_removal_validation=validate_before_removal,
        after_removal_validation=validate_after_removal,
        others_have_order=False  # Order comes from insertion order, not the other objects.
    )


def _validate(
    it: TIdentifiedObject,
    others: List[_U],
    get_all: Callable[[TIdentifiedObject], Generator[_U, None, None]],
    num: Callable[[TIdentifiedObject], int],
    add: Callable[[TIdentifiedObject, _U], TIdentifiedObject],
    remove: Callable[[TIdentifiedObject, _U], TIdentifiedObject],
    clear: Callable[[TIdentifiedObject], TIdentifiedObject],
    validate_collection: Callable[[Generator[_U, None, None], List[_U]], None],
    perform_duplicate_validation: Callable[[], None],
    before_removal_validation: Callable[[], None],
    after_removal_validation: Callable[[], None],
    others_have_order: bool
):
    # Make sure all the objects are not equal.
    assert len(set(others)) == len(others)

    # Make sure the item under test is empty to begin with, so nothing messes with our tests.
    assert num(it) == 0
    assert not list(get_all(it))

    other1, other2, other3 = others
    add(it, other1)
    add(it, other2)
    add(it, other3)

    assert num(it) == 3
    validate_collection(get_all(it), [other1, other2, other3])

    perform_duplicate_validation()

    # Ensure there are no changes to our collection after the duplicate testing, otherwise it may provide false positives below.
    assert num(it) == 3
    validate_collection(get_all(it), [other1, other2, other3])

    before_removal_validation()

    # Should be able to remove an existing item, but not one that isn't in the list anymore.
    remove(it, other1), "remove should return true for previously-added object"

    #
    # NOTE: inlining `remove_exception_types` directly into `pytest.raises` as `(ValueError, KeyError)` causes type errors (which are incorrect).
    #       We check for both ValueError and KeyError as different underlying collections throw different exceptions.
    #
    remove_exception_types: Tuple[Type[Exception], Type[Exception]] = (ValueError, KeyError)
    with pytest.raises(remove_exception_types):
        remove(it, other1)

    # Make sure the items is fully removed.
    assert num(it) == 2
    validate_collection(get_all(it), [other2, other3])

    after_removal_validation()

    # Make sure we can add the item back in, and it ends up in the correct spot in the collection.
    add(it, other1)
    assert num(it) == 3
    if others_have_order:
        validate_collection(get_all(it), [other1, other2, other3])
    else:
        validate_collection(get_all(it), [other2, other3, other1])

    clear(it)
    assert num(it) == 0
    assert not list(get_all(it))

    # Make sure you can call remove on an empty collection.
    with pytest.raises(remove_exception_types):
        remove(it, other3)
    assert num(it) == 0
    assert not list(get_all(it))

    # Make sure you can add an item back after it has been cleared
    add(it, other1)
    assert num(it) == 1
    validate_collection(get_all(it), [other1])


def _assert_unordered(actual: Generator[_U, None, None], expected: List[_U]):
    assert Counter(actual) == Counter(expected)


def _assert_ordered(actual: Generator[_U, None, None], expected: List[_U]):
    assert list(actual) == expected


def _create_duplicates_throw_validator(
    it: TIdentifiedObject,
    expected_duplicate_errors: Dict[_U, str],
    add: Callable[[TIdentifiedObject, _U], TIdentifiedObject]
) -> Callable[[], None]:
    def func():
        for other_duplicate, expected_error in expected_duplicate_errors.items():
            with pytest.raises(ValueError, match=expected_error):
                add(it, other_duplicate)

    return func


def _create_duplicates_supported_validator(
    it: TIdentifiedObject,
    others: List[_U],
    get_all: Callable[[TIdentifiedObject], Generator[_U, None, None]],
    num: Callable[[TIdentifiedObject], int],
    add: Callable[[TIdentifiedObject, _U], TIdentifiedObject],
    remove: Callable[[TIdentifiedObject, _U], bool],
    validate_collection: Callable[[Generator[_U, None, None], List[_U]], None],
) -> Callable[[], None]:
    def func():
        #
        # NOTE: We add all the items a second time to allow us to clean it up, as the remove below will take the first instance out, changing
        #       the order of the final collection if we only use a single duplicate.
        #
        for duplicate in others:
            add(it, duplicate)

        assert num(it) == len(others) * 2
        validate_collection(get_all(it), others + others)

        # Put the collection back to how it was before we added the duplicate for future tests.
        for duplicate in others:
            assert remove(it, duplicate), "Should be able to remove the duplicate"

    return func
