#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["UsagePoint"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.common.location import Location
    from zepben.ewb.model.cim.iec61968.metering.end_device import EndDevice
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment


@dataslot
class UsagePoint(IdentifiedObject):
    """
    Logical or physical point in the network to which readings or events may be attributed.
    Used at the place where a physical or virtual meter may be located; however, it is not required that a meter be present.
    """

    usage_point_location: Location | None = None
    """Service `zepben.ewb.model.cim.iec61968.common.location.Location` where the service delivered by this `UsagePoint` is consumed."""

    is_virtual: bool | None = None
    """
    If true, this usage point is virtual, i.e., no physical location exists in the network where a meter could be located to
    collect the meter readings. For example, one may define a virtual usage point to serve as an aggregation of usage for all
    of a company's premises distributed widely across the distribution territory. Otherwise, the usage point is physical,
    i.e., there is a logical point in the network where a meter could be located to collect meter readings.
    """

    connection_category: str | None = None
    """
    A code used to specify the connection category, e.g., low voltage or low pressure, where the usage point is defined.
    """

    rated_power: int | None = None
    """Active power that this usage point is configured to deliver in watts."""

    approved_inverter_capacity: int | None = None
    """The approved inverter capacity at this UsagePoint in volt-amperes."""

    phase_code: PhaseCode = PhaseCode.NONE
    """
    Phase code. Number of wires and specific nominal phases can be deduced from enumeration literal values. For example, ABCN is three-phase,
    four-wire, s12n (splitSecondary12N) is single-phase, three-wire, and s1n and s2n are single-phase, two-wire.
    """

    equipment: List[Equipment] | None = MRIDListAccessor()
    end_devices: List[EndDevice] | None = MRIDListAccessor()

    def _retype(self):
        self.equipment: MRIDListRouter[Equipment] = ...
        self.end_devices: MRIDListRouter[EndDevice] = ...
    
    @deprecated("BOILERPLATE: Use len(equipment) instead")
    def num_equipment(self):
        return len(self.equipment)

    @deprecated("BOILERPLATE: Use len(end_devices) instead")
    def num_end_devices(self):
        return len(self.end_devices)

    @deprecated("BOILERPLATE: Use equipment.get_by_mrid(mrid) instead")
    def get_equipment(self, mrid: str) -> Equipment:
        return self.equipment.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use equipment.append(equipment) instead")
    def add_equipment(self, equipment: Equipment) -> UsagePoint:
        self.equipment.append(equipment)
        return self

    @deprecated("Boilerplate: Use equipment.remove(equipment) instead")
    def remove_equipment(self, equipment: Equipment) -> UsagePoint:
        self.equipment.remove(equipment)
        return self

    @deprecated("BOILERPLATE: Use equipment.clear() instead")
    def clear_equipment(self) -> UsagePoint:
        return self.equipment.clear()

    @deprecated("BOILERPLATE: Use end_devices.get_by_mrid(mrid) instead")
    def get_end_device(self, mrid: str) -> EndDevice:
        return self.end_devices.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use end_devices.append(end_device) instead")
    def add_end_device(self, end_device: EndDevice) -> UsagePoint:
        self.end_devices.append(end_device)
        return self

    @deprecated("Boilerplate: Use end_devices.remove(end_device) instead")
    def remove_end_device(self, end_device: EndDevice) -> UsagePoint:
        self.end_devices.remove(end_device)
        return self

    @deprecated("BOILERPLATE: Use end_devices.clear() instead")
    def clear_end_devices(self) -> UsagePoint:
        return self.end_devices.clear()

    def is_metered(self):
        """
        Check whether this `UsagePoint` is metered. A `UsagePoint` is metered if it's associated with at least one `EndDevice`.
        Returns True if this `UsagePoint` has an `EndDevice`, False otherwise.
        """
        return nlen(self.end_devices) > 0
