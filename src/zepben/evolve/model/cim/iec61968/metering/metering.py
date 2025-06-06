#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from enum import Enum
from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.evolve.model.cim.iec61968.assets.asset_function import AssetFunction

if TYPE_CHECKING:
    from zepben.evolve import Equipment

from zepben.evolve.model.cim.iec61968.assets.asset import AssetContainer
from zepben.evolve.model.cim.iec61968.common.location import Location
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["Meter", "EndDevice", "UsagePoint", "EndDeviceFunction", "EndDeviceFunctionKind"]

logger = logging.getLogger(__name__)


class EndDevice(AssetContainer):
    """
    Asset container that performs one or more end device functions. One type of end device is a meter which can perform
    metering, load management, connect/disconnect, accounting functions, etc. Some end devices, such as ones monitoring
    and controlling air conditioners, refrigerators, pool pumps may be connected to a meter. All end devices may have
    communication capability defined by the associated communication function(s).

    An end device may be owned by a consumer, a service provider, utility or otherwise.

    There may be a related end device function that identifies a sensor or control point within a metering application
    or communications systems (e.g., water, gas, electricity).

    Some devices may use an optical port that conforms to the ANSI C12.18 standard for communications.
    """

    customer_mrid: Optional[str] = None
    """The `zepben.evolve.cim.iec61968.customers.customer.Customer` owning this `EndDevice`."""

    service_location: Optional[Location] = None
    """Service `zepben.evolve.cim.iec61968.common.location.Location` whose service delivery is measured by this `EndDevice`."""

    _usage_points: Optional[List[UsagePoint]] = None

    _functions: Optional[List[EndDeviceFunction]] = None

    def __init__(self, usage_points: List[UsagePoint] = None, functions: List[EndDeviceFunction] = None, **kwargs):
        super(EndDevice, self).__init__(**kwargs)
        if usage_points:
            for up in usage_points:
                self.add_usage_point(up)
        if functions:
            for edf in functions:
                self.add_function(edf)

    def num_usage_points(self):
        """
        Returns The number of `UsagePoint`s associated with this `EndDevice`
        """
        return nlen(self._usage_points)

    @property
    def usage_points(self) -> Generator[UsagePoint, None, None]:
        """
        The `UsagePoint`s associated with this `EndDevice`
        """
        return ngen(self._usage_points)

    def get_usage_point(self, mrid: str) -> UsagePoint:
        """
        Get the `UsagePoint` for this `EndDevice` identified by `mrid`

        `mrid` the mRID of the required `UsagePoint`
        Returns The `UsagePoint` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._usage_points, mrid)

    def add_usage_point(self, up: UsagePoint) -> EndDevice:
        """
        Associate `up` to this `EndDevice`.

        `up` the `UsagePoint` to associate with this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if another `UsagePoint` with the same `mrid` already exists for this `EndDevice`.
        """
        if self._validate_reference(up, self.get_usage_point, "A UsagePoint"):
            return self
        self._usage_points = list() if self._usage_points is None else self._usage_points
        self._usage_points.append(up)
        return self

    def remove_usage_point(self, up: UsagePoint) -> EndDevice:
        """
        Disassociate `up` from this `EndDevice`

        `up` the `UsagePoint` to disassociate from this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `EndDevice`.
        """
        self._usage_points = safe_remove(self._usage_points, up)
        return self

    def clear_usage_points(self) -> EndDevice:
        """
        Clear all usage_points.
        Returns A reference to this `EndDevice` to allow fluent use.
        """
        self._usage_points = None
        return self

    def num_functions(self):
        """
        Returns The number of `EndDeviceFunction`s associated with this `EndDevice`
        """
        return nlen(self._functions)

    @property
    def functions(self) -> Generator[EndDeviceFunction, None, None]:
        """
        The `EndDeviceFunction`s associated with this `EndDevice`
        """
        return ngen(self._functions)

    def get_function(self, mrid: str) -> EndDeviceFunction:
        """
        Get the `EndDeviceFunction` for this `EndDevice` identified by `mrid`

        `mrid` the mRID of the required `EndDeviceFunction`
        Returns The `EndDeviceFunction` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._functions, mrid)

    def add_function(self, edf: EndDeviceFunction) -> EndDevice:
        """
        Associate `edf` to this `EndDevice`.

        `edf` the `EndDeviceFunction` to associate with this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if another `EndDeviceFunction` with the same `mrid` already exists for this `EndDevice`.
        """
        if self._validate_reference(edf, self.get_function, "An EndDeviceFunction"):
            return self
        self._functions = list() if self._functions is None else self._functions
        self._functions.append(edf)
        return self

    def remove_function(self, edf: EndDeviceFunction) -> EndDevice:
        """
        Disassociate `edf` from this `EndDevice`

        `up` the `EndDeviceFunction` to disassociate from this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `EndDevice`.
        """
        self._functions = safe_remove(self._functions, edf)
        return self

    def clear_functions(self) -> EndDevice:
        """
        Clear all end_device_functions.
        Returns A reference to this `EndDevice` to allow fluent use.
        """
        self._functions = None
        return self


class UsagePoint(IdentifiedObject):
    """
    Logical or physical point in the network to which readings or events may be attributed.
    Used at the place where a physical or virtual meter may be located; however, it is not required that a meter be present.
    """

    usage_point_location: Optional[Location] = None
    """Service `zepben.evolve.cim.iec61968.common.location.Location` where the service delivered by this `UsagePoint` is consumed."""

    is_virtual: bool = False
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


class Meter(EndDevice):
    """
    Physical asset that performs the metering role of the usage point. Used for measuring consumption and detection of events.
    """

    @property
    def company_meter_id(self):
        """ Returns this `Meter`s ID. Currently stored in `IdentifiedObject.name` """
        return self.name

    @company_meter_id.setter
    def company_meter_id(self, meter_id):
        """
        `meter_id` The ID to set for this Meter. Will use `IdentifiedObject.name` as a backing field.
        """
        self.name = meter_id


class EndDeviceFunction(AssetFunction):
    """
    Function performed by an end device such as a meter, communication equipment, controllers, etc.
    """

    enabled: bool = True
    """True if the function is enabled."""


class EndDeviceFunctionKind(Enum):
    """
    Kind of end device function.
    """

    UNKNOWN = 0
    """Unknown function kind."""

    autonomousDst = 1
    """Autonomous application of daylight saving time (DST)."""

    demandResponse = 2
    """Demand response functions."""

    electricMetering = 3
    """Electricity metering."""

    metrology = 4
    """Presentation of metered values to a user or another system (always a function of a meter, but might not be supported by a load control unit)."""

    onRequestRead = 5
    """On-request reads."""

    outageHistory = 6
    """Reporting historical power interruption data."""

    relaysProgramming = 7
    """Support for one or more relays that may be programmable in the meter (and tied to TOU, time pulse, load control or other functions)."""

    reverseFlow = 8
    """Detection and monitoring of reverse flow."""

    @property
    def short_name(self):
        return str(self)[22:]
