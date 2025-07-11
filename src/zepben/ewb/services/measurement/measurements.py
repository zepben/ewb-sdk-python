#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["MeasurementService"]

from typing import List, Optional, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.meas.measurement_value import MeasurementValue

if TYPE_CHECKING:
    from zepben.ewb import IdentifiedObject


class MeasurementService:

    def __init__(self):
        super().__init__()
        self._measurements: List[MeasurementValue] = []

    def add(self, value: MeasurementValue):
        self._measurements.append(value)

    def remove(self, value: MeasurementValue):
        self._measurements.remove(value)

    def len_of(self, t: type = None) -> int:
        return len([m for m in self._measurements if isinstance(m, t)]) if t is not None else len(self._measurements)

    def objects(self, obj_type: Optional[type] = None, exc_types: Optional[List[type]] = None) -> Generator[IdentifiedObject, None, None]:
        for m in self._measurements:
            yield m
