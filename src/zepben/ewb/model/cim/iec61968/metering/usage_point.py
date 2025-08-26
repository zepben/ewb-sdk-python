#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["UsagePoint"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.common.location import Location
    from zepben.ewb.model.cim.iec61968.metering.end_device import EndDevice
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment


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

    _equipment: Optional[List[Equipment]] = None
    _end_devices: Optional[List[EndDevice]] = None

    def __init__(self, equipment: List[Equipment] = None, end_devices: List[EndDevice] = None, **kwargs):
        super(UsagePoint, self).__init__(**kwargs)
        if equipment:
            for eq in equipment:
                self.add_equipment(eq)
        if end_devices:
            for ed in end_devices:
                self.add_end_device(ed)

    def num_equipment(self):
        """
        Returns The number of `Equipment`s associated with this `UsagePoint`
        """
        return nlen(self._equipment)

    def num_end_devices(self):
        """
        Returns The number of `EndDevice`s associated with this `UsagePoint`
        """
        return nlen(self._end_devices)

    @property
    def end_devices(self) -> Generator[EndDevice, None, None]:
        """
        The `EndDevice`'s (Meter's) associated with this `UsagePoint`.
        """
        return ngen(self._end_devices)

    @property
    def equipment(self) -> Generator[Equipment, None, None]:
        """
        The `zepben.model.Equipment` associated with this `UsagePoint`.
        """
        return ngen(self._equipment)

    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` for this `UsagePoint` identified by `mrid`

        `mrid` The mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._equipment, mrid)

    def add_equipment(self, equipment: Equipment) -> UsagePoint:
        """
        Associate an `Equipment` with this `UsagePoint`

        `equipment` The `Equipment` to associate with this `UsagePoint`.
        Returns A reference to this `UsagePoint` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `UsagePoint`.
        """
        if self._validate_reference(equipment, self.get_equipment, "An Equipment"):
            return self

        self._equipment = list() if self._equipment is None else self._equipment
        self._equipment.append(equipment)
        return self

    def remove_equipment(self, equipment: Equipment) -> UsagePoint:
        """
        Disassociate an `Equipment` from this `UsagePoint`

        `equipment` The `Equipment` to disassociate with this `UsagePoint`.
        Returns A reference to this `UsagePoint` to allow fluent use.
        Raises `ValueError` if `equipment` was not associated with this `UsagePoint`.
        """
        self._equipment = safe_remove(self._equipment, equipment)
        return self

    def clear_equipment(self) -> UsagePoint:
        """
        Clear all equipment.
        Returns A reference to this `UsagePoint` to allow fluent use.
        """
        self._equipment = None
        return self

    def get_end_device(self, mrid: str) -> EndDevice:
        """
        Get the `EndDevice` for this `UsagePoint` identified by `mrid`

        `mrid` The mRID of the required `EndDevice`
        Returns The `EndDevice` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._end_devices, mrid)

    def add_end_device(self, end_device: EndDevice) -> UsagePoint:
        """
        Associate an `EndDevice` with this `UsagePoint`

        `end_device` The `EndDevice` to associate with this `UsagePoint`.
        Returns A reference to this `UsagePoint` to allow fluent use.
        Raises `ValueError` if another `EndDevice` with the same `mrid` already exists for this `UsagePoint`.
        """
        if self._validate_reference(end_device, self.get_end_device, "An EndDevice"):
            return self
        self._end_devices = list() if self._end_devices is None else self._end_devices
        self._end_devices.append(end_device)
        return self

    def remove_end_device(self, end_device: EndDevice) -> UsagePoint:
        """
        Disassociate `end_device` from this `UsagePoint`.

        `end_device` The `EndDevice` to disassociate from this `UsagePoint`.
        Returns A reference to this `UsagePoint` to allow fluent use.
        Raises `ValueError` if `end_device` was not associated with this `UsagePoint`.
        """
        self._end_devices = safe_remove(self._end_devices, end_device)
        return self

    def clear_end_devices(self) -> UsagePoint:
        """
        Clear all end_devices.
        Returns A reference to this `UsagePoint` to allow fluent use.
        """
        self._end_devices = None
        return self

    def is_metered(self):
        """
        Check whether this `UsagePoint` is metered. A `UsagePoint` is metered if it's associated with at least one `EndDevice`.
        Returns True if this `UsagePoint` has an `EndDevice`, False otherwise.
        """
        return nlen(self._end_devices) > 0
