#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["NetworkHierarchy"]

from typing import Dict

from zepben.ewb import Circuit, Loop, Substation
from zepben.ewb.dataclassy import dataclass
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion


@dataclass(slots=True)
class NetworkHierarchy(object):
    """Container for simplified network hierarchy objects"""
    geographical_regions: Dict[str, GeographicalRegion]
    sub_geographical_regions: Dict[str, SubGeographicalRegion]
    substations: Dict[str, Substation]
    feeders: Dict[str, Feeder]
    circuits: Dict[str, Circuit]
    loops: Dict[str, Loop]
