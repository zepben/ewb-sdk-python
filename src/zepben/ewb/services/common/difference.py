#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import Optional, Any, List, Dict, TypeVar

from zepben.ewb import IdentifiedObject
from zepben.ewb.dataslot.dataslot import instantiate

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
    missing_from_target: List[Any] = instantiate(list)
    missing_from_source: List[Any] = instantiate(list)
    modifications: List[Difference] = instantiate(list)


@dataclass()
class ObjectDifference(Difference):
    source: IdentifiedObject
    target: IdentifiedObject
    differences: Dict[str, Difference] = instantiate(dict)


@dataclass()
class ReferenceDifference(Difference):
    source: Optional[IdentifiedObject]
    target_value: Optional[IdentifiedObject]


@dataclass()
class IndexedDifference(Difference):
    index: int
    difference: Difference
