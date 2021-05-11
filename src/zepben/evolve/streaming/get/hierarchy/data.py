#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Dict

from dataclassy import dataclass

__all__ = ["NetworkHierarchy"]

from zepben.evolve import Circuit, Feeder, GeographicalRegion, Loop, SubGeographicalRegion, Substation


@dataclass(slots=True)
class NetworkHierarchy(object):
    """Container for simplified network hierarchy objects"""
    geographical_regions: Dict[str, GeographicalRegion]
    sub_geographical_regions: Dict[str, SubGeographicalRegion]
    substations: Dict[str, Substation]
    feeders: Dict[str, Feeder]
    circuits: Dict[str, Circuit]
    loops: Dict[str, Loop]
