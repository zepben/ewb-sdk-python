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
from typing import Optional, Dict

from dataclassy import dataclass

__all__ = ["NetworkHierarchy", "NetworkHierarchyIdentifiedObject", "NetworkHierarchyFeeder", "NetworkHierarchyGeographicalRegion", "NetworkHierarchySubstation",
           "NetworkHierarchySubGeographicalRegion"]


@dataclass(slots=True)
class NetworkHierarchy(object):
    """Container for simplified network hierarchy objects"""
    geographical_regions: Dict[str, NetworkHierarchyGeographicalRegion]
    sub_geographical_regions: Dict[str, NetworkHierarchySubGeographicalRegion]
    substations: Dict[str, NetworkHierarchySubstation]
    feeders: Dict[str, NetworkHierarchyFeeder]


@dataclass(slots=True)
class NetworkHierarchyIdentifiedObject(object):
    """A simplified representation of an identified object for requesting the network hierarchy."""
    mrid: str
    name: str


class NetworkHierarchyGeographicalRegion(NetworkHierarchyIdentifiedObject):
    """A simplified representation of a geographical region for requesting the network hierarchy."""
    sub_geographical_regions: Dict[str, NetworkHierarchySubGeographicalRegion] = None


class NetworkHierarchySubGeographicalRegion(NetworkHierarchyIdentifiedObject):
    """A simplified representation of a subgeographical region for requesting the network hierarchy."""
    substations: Dict[str, NetworkHierarchySubstation] = None
    geographical_region: Optional[NetworkHierarchyGeographicalRegion] = None


class NetworkHierarchySubstation(NetworkHierarchyIdentifiedObject):
    """A simplified representation of a substation for requesting the network hierarchy."""
    feeders: Dict[str, NetworkHierarchyFeeder]
    sub_geographical_region: Optional[NetworkHierarchySubGeographicalRegion] = None


class NetworkHierarchyFeeder(NetworkHierarchyIdentifiedObject):
    """A simplified representation of a feeder for requesting the network hierarchy."""
    substation: Optional[NetworkHierarchySubstation] = None