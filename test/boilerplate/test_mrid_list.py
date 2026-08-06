#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

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
    owner.events.append(("backfill", item.mrid))


def reject_backfill(_owner: Owner, _item: Feeder):
    raise ValueError("backfill failed")


def record_validation(owner: Owner, item: Feeder):
    owner.events.append(("validate", item.mrid))


def reject_validation(_owner: Owner, _item: Feeder):
    raise ValueError("validation failed")


@dataclass
class Owner:
    backing_feeders: list[Feeder] = field(
        default_factory=list,
        repr=False,
    )
    events: list[tuple[str, str]] = field(
        default_factory=list,
        repr=False,
    )

    feeders = MridList(
        backing_feeders,
        "Feeder",
    )
    backfilled_feeders = MridList(
        backing_feeders,
        "Feeder",
        backfill=CallbackBackfill(record_backfill),
    )
    rejecting_backfill_feeders = MridList(
        backing_feeders,
        "Feeder",
        backfill=CallbackBackfill(reject_backfill),
    )
    validated_feeders = MridList(
        backing_feeders,
        "Feeder",
        validate=record_validation,
    )
    rejecting_validation_feeders = MridList(
        backing_feeders,
        "Feeder",
        validate=reject_validation,
    )
    backfilled_validated_feeders = MridList(
        backing_feeders,
        "Feeder",
        backfill=CallbackBackfill(record_backfill),
        validate=record_validation,
    )
    sorted_feeders = MridList(
        backing_feeders,
        "Feeder",
        sort_by=lambda feeder: feeder.mrid,
    )


def test_append_adds_item_to_owner_backing_list():
    owner = Owner()
    feeder = Feeder("feeder")

    owner.feeders.append(feeder)

    assert owner.backing_feeders == [feeder]


def test_append_applies_backfill():
    owner = Owner()
    feeder = Feeder("feeder")

    owner.backfilled_feeders.append(feeder)

    assert owner.events == [("backfill", "feeder")]
    assert owner.backing_feeders == [feeder]


def test_backfill_failure_does_not_append_item():
    owner = Owner()

    with pytest.raises(ValueError, match="backfill failed"):
        owner.rejecting_backfill_feeders.append(Feeder("feeder"))

    assert owner.backing_feeders == []


def test_append_runs_validation():
    owner = Owner()
    feeder = Feeder("feeder")

    owner.validated_feeders.append(feeder)

    assert owner.events == [("validate", "feeder")]
    assert owner.backing_feeders == [feeder]


def test_validation_failure_does_not_append_item():
    owner = Owner()

    with pytest.raises(ValueError, match="validation failed"):
        owner.rejecting_validation_feeders.append(Feeder("feeder"))

    assert owner.backing_feeders == []


def test_append_runs_backfill_before_validation():
    owner = Owner()
    feeder = Feeder("feeder")

    owner.backfilled_validated_feeders.append(feeder)

    assert owner.events == [
        ("backfill", "feeder"),
        ("validate", "feeder"),
    ]
    assert owner.backing_feeders == [feeder]


def test_append_sorts_owner_backing_list():
    owner = Owner()
    second = Feeder("second")
    first = Feeder("first")

    owner.sorted_feeders.append(second)
    owner.sorted_feeders.append(first)

    assert owner.backing_feeders == [first, second]


def test_readding_same_item_still_sorts_owner_backing_list():
    owner = Owner()
    first = Feeder("first")
    second = Feeder("second")
    owner.sorted_feeders.extend([first, second])
    second.mrid = "before-first"

    owner.sorted_feeders.append(second)

    assert owner.backing_feeders == [second, first]
    assert len(owner.backing_feeders) == 2


def test_remove_removes_item_from_owner_backing_list():
    owner = Owner()
    retained = Feeder("retained")
    removed = Feeder("removed")
    owner.backing_feeders.extend([retained, removed])

    owner.feeders.remove(removed)

    assert owner.backing_feeders == [retained]


def test_clear_empties_owner_backing_list():
    owner = Owner()

    owner.backing_feeders.extend(
        [
            Feeder("first"),
            Feeder("second"),
        ]
    )

    owner.feeders.clear()

    assert owner.backing_feeders == []


def test_repr_matches_owner_backing_list_repr():
    owner = Owner()

    owner.backing_feeders.extend(
        [
            Feeder("first"),
            Feeder("second"),
        ]
    )

    assert repr(owner.feeders) == repr(owner.backing_feeders)


def test_class_field_repr_uses_descriptor_repr() -> None:
    assert repr(Owner.feeders) == object.__repr__(Owner.feeders)
