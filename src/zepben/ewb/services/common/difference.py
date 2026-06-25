#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from math import isnan
from dataclasses import dataclass, field
from typing import Optional, Any, List, Dict, TypeVar, Generic

from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable

T = TypeVar("T")


@dataclass()
class Difference:
    pass


@dataclass()
class ValueDifference(Difference):
    source_value: Optional[Any]
    target_value: Optional[Any]

    def __eq__(self, other):
        if (isinstance(self.source_value, float)
            and isinstance(self.target_value, float)
            and isnan(self.source_value)
            and isnan(self.target_value)
        ):
            return True
        else:
            return super().__eq__(other)


@dataclass()
class CollectionDifference(Difference):
    missing_from_target: List[Any] = field(default_factory=list)
    missing_from_source: List[Any] = field(default_factory=list)
    modifications: List[Difference] = field(default_factory=list)


@dataclass()
class ObjectDifference(Difference, Generic[T]):
    source: T
    target: T
    differences: Dict[str, Difference] = field(default_factory=dict)

    def __str__(self):
        return f"source: {str(self.source)}, target: {str(self.target)}, diff: {self.differences}"


@dataclass()
class ReferenceDifference(Difference):
    source: Optional[Identifiable]
    target_value: Optional[Identifiable]


@dataclass()
class IndexedDifference(Difference):
    index: int
    difference: Difference
