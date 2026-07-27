#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["UsagePoint"]

from typing import Optional, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.extensions.iec61968.common.contact_details import ContactDetails
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.util import nlen
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.common.location import Location
    from zepben.ewb.model.cim.iec61968.metering.end_device import EndDevice
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment


@zb_dataclass
class UsagePoint(IdentifiedObject):
    """
    Logical or physical point in the network to which readings or events may be attributed.
    Used at the place where a physical or virtual meter may be located; however, it is not required that a meter be present.
    """

    usage_point_location: Optional[Location] = None
    """Service `zepben.ewb.model.cim.iec61968.common.location.Location` where the service delivered by this `UsagePoint` is consumed."""

    is_virtual: Optional[bool] = None
    """
    If true, this usage point is virtual, i.e., no physical location exists in the network where a meter could be located to
    collect the meter readings. For example, one may define a virtual usage point to serve as an aggregation of usage for all
    of a company's premises distributed widely across the distribution territory. Otherwise, the usage point is physical,
    i.e., there is a logical point in the network where a meter could be located to collect meter readings.
    """

    connection_category: Optional[str] = None
    """
    A code used to specify the connection category, e.g., low voltage or low pressure, where the usage point is defined.
    """

    rated_power: Optional[int] = None
    """Active power that this usage point is configured to deliver in watts."""

    approved_inverter_capacity: Optional[int] = None
    """The approved inverter capacity at this UsagePoint in volt-amperes."""

    phase_code: PhaseCode = PhaseCode.NONE
    """
    Phase code. Number of wires and specific nominal phases can be deduced from enumeration literal values. For example, ABCN is three-phase,
    four-wire, s12n (splitSecondary12N) is single-phase, three-wire, and s1n and s2n are single-phase, two-wire.
    """

    _equipment: list[Equipment] | None = field(default=None)
    _end_devices: list[EndDevice] | None = field(default=None)
    _contacts: list[ContactDetails] | None = field(default=None)


    end_devices: MridCollection[EndDevice] = LazyMridList(
        _end_devices,
        "An EndDevice",
    )

    equipment: MridCollection[Equipment] = LazyMridList(
        _equipment,
        "An Equipment",
    )

    contacts: MridCollection[ContactDetails] = LazyMridList(
        _contacts,
        "A ContactDetails"
    )

    def num_equipment(self):
        """
        Returns The number of `Equipment`s associated with this `UsagePoint`
        """
        return nlen(self._equipment)

    # region deprecated list boilerplate

    # region contacts boilerplate

    @deprecated("Use len(contacts) instead.")
    def num_contacts(self) -> int:
        return len(self.contacts)

    @deprecated("Use contacts.get_by_mrid(mrid) instead.")
    def get_contact(self, mrid: str) -> ContactDetails:
        return self.contacts.get_by_mrid(mrid)

    @deprecated("Use contacts.append(contact) instead.")
    def add_contact(self, contact: ContactDetails) -> UsagePoint:
        self.contacts.append(contact)
        return self

    @deprecated("Use contacts.remove(contact) instead.")
    def remove_contact(self, contact: ContactDetails) -> UsagePoint:
        self.contacts.remove(contact)
        return self

    @deprecated("Use contacts.clear() instead.")
    def clear_contacts(self) -> UsagePoint:
        self.contacts.clear()
        return self

    # endregion

    # region end_devices boilerplate

    @deprecated("Use len(obj.end_devices) instead.")
    def num_end_devices(self):
        return len(self.end_devices)

    @deprecated("Use obj.end_devices.get_by_mrid(mrid) instead.")
    def get_end_device(self, mrid: str) -> EndDevice:
        return self.end_devices.get_by_mrid(mrid)

    @deprecated("Use obj.end_devices.append(end_device) instead.")
    def add_end_device(self, end_device: EndDevice) -> UsagePoint:
        self.end_devices.append(end_device)
        return self

    @deprecated("Use obj.end_devices.remove(end_device) instead.")
    def remove_end_device(self, end_device: EndDevice) -> UsagePoint:
        self.end_devices.remove(end_device)
        return self

    @deprecated("Use obj.end_devices.clear() instead.")
    def clear_end_devices(self) -> UsagePoint:
        self.end_devices.clear()
        return self

    # endregion end_devices boilerplate

    # region equipment boilerplate

    @deprecated("Use len(obj.equipment) instead.")
    def num_equipment(self):
        return len(self.equipment)

    @deprecated("Use obj.equipment.get_by_mrid(mrid) instead.")
    def get_equipment(self, mrid: str) -> Equipment:
        return self.equipment.get_by_mrid(mrid)

    @deprecated("Use obj.equipment.append(equipment) instead.")
    def add_equipment(self, equipment: Equipment) -> UsagePoint:
        self.equipment.append(equipment)
        return self

    @deprecated("Use obj.equipment.remove(equipment) instead.")
    def remove_equipment(self, equipment: Equipment) -> UsagePoint:
        self.equipment.remove(equipment)
        return self

    @deprecated("Use obj.equipment.clear() instead.")
    def clear_equipment(self) -> UsagePoint:
        self.equipment.clear()
        return self

    # endregion equipment boilerplate

    # endregion deprecated list boilerplate
