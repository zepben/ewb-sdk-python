#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import pytest

from zepben.ewb.boilerplate.collections.mrid_list import MridList
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder


class CallbackBackfill:
    def __init__(
        self,
        callback: Callable[[Owner, Feeder], None],
    ):
        self._callback = callback

    def apply(self, item: Feeder, owner: Owner):
        self._callback(owner, item)


def record_backfill(owner: Owner, item: Feeder):
    owner._events.append(("backfill", item.mrid))


def reject_backfill(_owner: Owner, _item: Feeder):
    raise ValueError("backfill failed")


def record_validation(owner: Owner, item: Feeder):
    owner._events.append(("validate", item.mrid))


def reject_validation(_owner: Owner, _item: Feeder):
    raise ValueError("validation failed")


def validate_for_combined_test(owner: Owner, item: Feeder):
    record_validation(owner, item)

    if item.mrid == "invalid":
        raise ValueError("invalid feeder")


@dataclass
class Owner:
    _feeders: list[Feeder] = field(
        default_factory=list,
        repr=False,
    )
    _events: list[tuple[str, str]] = field(
        default_factory=list,
        repr=False,
    )

    feeders = MridList(
        _feeders,
        "Feeder",
    )
    backfilled_feeders = MridList(
        _feeders,
        "Feeder",
        backfill=CallbackBackfill(record_backfill),
    )
    rejecting_backfill_feeders = MridList(
        _feeders,
        "Feeder",
        backfill=CallbackBackfill(reject_backfill),
    )
    validated_feeders = MridList(
        _feeders,
        "Feeder",
        validate=record_validation,
    )
    rejecting_validation_feeders = MridList(
        _feeders,
        "Feeder",
        validate=reject_validation,
    )
    backfilled_validated_feeders = MridList(
        _feeders,
        "Feeder",
        backfill=CallbackBackfill(record_backfill),
        validate=record_validation,
    )
    sorted_feeders = MridList(
        _feeders,
        "Feeder",
        sort_by=lambda feeder: feeder.mrid,
    )
    fully_configured_feeders = MridList(
        _feeders,
        "Feeder",
        backfill=CallbackBackfill(record_backfill),
        validate=validate_for_combined_test,
        sort_by=lambda feeder: feeder.mrid,
    )


@pytest.fixture
def owner() -> Owner:
    owner = Owner()

    # All wrappers intentionally point at this same non-null backing list.
    # Reset it and the callback log for each test.
    owner._feeders.clear()
    owner._events.clear()

    return owner


def test_append_adds_item_to_owner_backing_list(owner: Owner):
    feeder = Feeder("feeder")

    owner.feeders.append(feeder)

    assert owner._feeders == [feeder]


def test_appending_same_instance_twice_only_adds_it_once(
    owner: Owner,
):
    feeder = Feeder("feeder")

    owner.feeders.append(feeder)
    owner.feeders.append(feeder)

    assert owner._feeders == [feeder]


def test_appending_different_instance_with_same_mrid_raises(
    owner: Owner,
):
    existing = Feeder("duplicate")
    owner.feeders.append(existing)

    with pytest.raises(
        ValueError,
        match=r"Feeder with mRID duplicate already exists",
    ):
        owner.feeders.append(Feeder("duplicate"))

    assert owner._feeders == [existing]


def test_rejected_duplicate_does_not_run_backfill_or_validation(
    owner: Owner,
):
    feeder = Feeder("feeder")
    owner.backfilled_validated_feeders.append(feeder)
    owner._events.clear()

    owner.backfilled_validated_feeders.append(feeder)

    assert owner._feeders == [feeder]
    assert owner._events == []


def test_append_applies_backfill(owner: Owner):
    feeder = Feeder("feeder")

    owner.backfilled_feeders.append(feeder)

    assert owner._events == [("backfill", "feeder")]
    assert owner._feeders == [feeder]


def test_backfill_failure_does_not_append_item(owner: Owner):
    with pytest.raises(ValueError, match="backfill failed"):
        owner.rejecting_backfill_feeders.append(Feeder("feeder"))

    assert owner._feeders == []


def test_append_runs_validation(owner: Owner):
    feeder = Feeder("feeder")

    owner.validated_feeders.append(feeder)

    assert owner._events == [("validate", "feeder")]
    assert owner._feeders == [feeder]


def test_validation_failure_does_not_append_item(owner: Owner):
    with pytest.raises(ValueError, match="validation failed"):
        owner.rejecting_validation_feeders.append(Feeder("feeder"))

    assert owner._feeders == []


def test_append_runs_backfill_before_validation(owner: Owner):
    feeder = Feeder("feeder")

    owner.backfilled_validated_feeders.append(feeder)

    assert owner._events == [
        ("backfill", "feeder"),
        ("validate", "feeder"),
    ]
    assert owner._feeders == [feeder]


def test_append_sorts_owner_backing_list(owner: Owner):
    second = Feeder("second")
    first = Feeder("first")

    owner.sorted_feeders.append(second)
    owner.sorted_feeders.append(first)

    assert owner._feeders == [first, second]


def test_remove_removes_item_from_owner_backing_list(
    owner: Owner,
):
    retained = Feeder("retained")
    removed = Feeder("removed")
    owner._feeders.extend([retained, removed])

    owner.feeders.remove(removed)

    assert owner._feeders == [retained]


def test_clear_empties_owner_backing_list(owner: Owner):
    owner._feeders.extend(
        [
            Feeder("first"),
            Feeder("second"),
        ]
    )

    owner.feeders.clear()

    assert owner._feeders == []


def test_repr_matches_owner_backing_list_repr(owner: Owner):
    owner._feeders.extend(
        [
            Feeder("first"),
            Feeder("second"),
        ]
    )

    assert repr(owner.feeders) == repr(owner._feeders)




def test_mrid_list_all_functionality_together(owner: Owner):
    third = Feeder("third")
    first = Feeder("first")
    second = Feeder("second")

    owner.fully_configured_feeders.extend([third, first, second])

    assert owner._feeders == [first, second, third]
    assert len(owner.fully_configured_feeders) == 3
    assert list(owner.fully_configured_feeders) == [
        first,
        second,
        third,
    ]
    assert next(iter(owner.fully_configured_feeders)) is first
    assert owner.fully_configured_feeders[0] is first
    assert list(owner.fully_configured_feeders[1:]) == [
        second,
        third,
    ]
    assert second in owner.fully_configured_feeders
    assert (
        owner.fully_configured_feeders.get_by_mrid("second")
        is second
    )
    assert repr(owner.fully_configured_feeders) == repr(
        owner._feeders
    )

    with pytest.raises(KeyError, match="missing"):
        owner.fully_configured_feeders.get_by_mrid("missing")

    indexed: list[tuple[int, Feeder]] = []
    owner.fully_configured_feeders.for_each_indexed(
        lambda index, item: indexed.append((index, item))
    )
    assert indexed == [
        (0, first),
        (1, second),
        (2, third),
    ]

    events_before_duplicate = list(owner._events)
    owner.fully_configured_feeders.append(first)

    assert owner._feeders == [first, second, third]
    assert owner._events == events_before_duplicate

    with pytest.raises(
        ValueError,
        match=r"Feeder with mRID second already exists",
    ):
        owner.fully_configured_feeders.append(Feeder("second"))

    assert owner._feeders == [first, second, third]
    assert owner._events == events_before_duplicate

    with pytest.raises(ValueError, match="invalid feeder"):
        owner.fully_configured_feeders.append(Feeder("invalid"))

    assert owner._feeders == [first, second, third]
    assert owner._events[-2:] == [
        ("backfill", "invalid"),
        ("validate", "invalid"),
    ]

    owner.fully_configured_feeders.remove(second)

    assert owner._feeders == [first, third]

    owner.fully_configured_feeders.clear()

    assert len(owner.fully_configured_feeders) == 0
    assert list(owner.fully_configured_feeders) == []
    assert owner._feeders == []
    assert owner._events[:6] == [
        ("backfill", "third"),
        ("validate", "third"),
        ("backfill", "first"),
        ("validate", "first"),
        ("backfill", "second"),
        ("validate", "second"),
    ]
