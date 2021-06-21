#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass, field
from typing import Optional, Any, List, Dict, TypeVar

from zepben.evolve import IdentifiedObject

T = TypeVar("T")


@dataclass()
class Difference:
    pass


@dataclass()
class ValueDifference(Difference):
    source_value: Optional[Any]
    target_value: Optional[Any]


@dataclass()
class CollectionDifference(Difference):
    missing_from_target: List[Any] = field(default_factory=list)
    missing_from_source: List[Any] = field(default_factory=list)
    modifications: List[Difference] = field(default_factory=list)


@dataclass()
class ObjectDifference(Difference):
    source: T
    target: T
    differences: Dict[str, Difference] = field(default_factory=dict)


@dataclass()
class ReferenceDifference(Difference):
    source: Optional[IdentifiedObject]
    target_value: Optional[IdentifiedObject]


@dataclass()
class IndexedDifference(Difference):
    index: int
    difference: Difference
