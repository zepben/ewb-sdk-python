"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field, InitVar
from typing import Optional, Generator
from typing import List

from zepben.cimbend.cim.iec61968.assets.asset import AssetContainer
from zepben.cimbend.cim.iec61968.common.location import Location
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["Meter", "EndDevice", "UsagePoint"]

logger = logging.getLogger(__name__)


@dataclass
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

    Attributes -
        customer_mrid : The :class:`zepben.cimbend.Customer` associated with this EndDevice.
        service_location : The :class:`zepben.cimbend.Location` of this EndDevice
        usage_points : The :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint`s associated with this
                        ``EndDevice``
    """

    customer_mrid: Optional[str] = None
    service_location: Optional[Location] = None
    usagepoints: InitVar[List[UsagePoint]] = field(default=list())
    _usage_points: Optional[List[UsagePoint]] = field(init=False, default=None)

    def __post_init__(self, organisationroles: List[AssetOrganisationRole], usagepoints: [List[UsagePoint]]):
        super().__post_init__(organisationroles)
        for up in usagepoints:
            self.add_usage_point(up)

    @property
    def num_usage_points(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint`s associated
        with this ``EndDevice``
        """
        return nlen(self._usage_points)

    @property
    def usage_points(self) -> Generator[UsagePoint, None, None]:
        """
        :return: Generator over the ``UsagePoint``s of this ``EndDevice``.
        """
        return ngen(self._usage_points)

    def get_usage_point(self, mrid: str) -> UsagePoint:
        """
        Get the ``UsagePoint`` for this ``EndDevice`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint`
        :return: The :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._usage_points, mrid)

    def add_usage_point(self, up: UsagePoint) -> EndDevice:
        """
        Add a ``UsagePoint`` to this ``EndDevice``.

        :param up: the :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint` to
        associate with this ``EndDevice``. Will only add to this object if it is not already associated.
        :return: A reference to this ``EndDevice`` to allow fluent use.
        """
        if self._validate_reference(up, self.get_usage_point, "A UsagePoint"):
            return self
        self._usage_points = list() if self._usage_points is None else self._usage_points
        self._usage_points.append(up)
        return self

    def remove_usage_point(self, up: UsagePoint) -> EndDevice:
        """
        Remove a ``UsagePoint`` from this ``EndDevice``

        :param up: the :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint` to
        disassociate with this ``EndDevice``.
        :raises: ValueError if ``up`` was not associated with this ``EndDevice``.
        :return: A reference to this ``EndDevice`` to allow fluent use.
        """
        self._usage_points = safe_remove(self._usage_points, up)
        return self

    def clear_usage_points(self) -> EndDevice:
        """
        Clear all usage_points.
        :return: A reference to this ``EndDevice`` to allow fluent use.
        """
        self._usage_points = None
        return self


@dataclass
class UsagePoint(IdentifiedObject):
    """
    Logical or physical point in the network to which readings or events may be attributed.
    Used at the place where a physical or virtual meter may be located; however, it is not required that a meter be present.

    Attributes -
        usage_point_location : The :class:`zepben.cimbend.iec61968.common.location.Location` of this UsagePoint
        end_devices : The :class:`EndDevice`'s (Meter's) associated with this UsagePoint.
        equipment : The :class:`zepben.model.Equipment` associated with this UsagePoint.
    """

    usage_point_location: Optional[Location] = None
    equipment_: InitVar[List[Equipment]] = field(default=list())
    _equipment: Optional[List[Equipment]] = field(init=False, default=None)
    enddevices: InitVar[List[EndDevice]] = field(default=list())
    _end_devices: Optional[List[EndDevice]] = field(init=False, default=None)

    def __post_init__(self, equipment_: List[Equipment], enddevices: List[EndDevice]):
        super().__post_init__()
        for eq in equipment_:
            self.add_equipment(eq)
        for ed in enddevices:
            self.add_end_device(ed)

    @property
    def num_equipment(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment`s associated
        with this ``UsagePoint``
        """
        return nlen(self._equipment)

    @property
    def num_end_devices(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61968.metering.metering.EndDevice`s associated
        with this ``UsagePoint``
        """
        return nlen(self._end_devices)

    @property
    def end_devices(self) -> Generator[EndDevice, None, None]:
        """
        :return: Generator over the ``EndDevice``s of this ``UsagePoint``.
        """
        return ngen(self._end_devices)

    @property
    def equipment(self) -> Generator[Equipment, None, None]:
        """
        :return: Generator over the ``Equipment``s of this ``UsagePoint``.
        """
        return ngen(self._equipment)

    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the ``equipment`` for this ``UsagePoint`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment`
        :return: The :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._equipment, mrid)

    def add_equipment(self, equipment: Equipment) -> UsagePoint:
        """
        Add an ``Equipment`` to this ``UsagePoint``

        :param equipment: the :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment` to
        associate with this ``UsagePoint``. Will only add to this object if it is not already associated.
        :return: A reference to this ``UsagePoint`` to allow fluent use.
        """
        if self._validate_reference(equipment, self.get_equipment, "An Equipment"):
            return self

        self._equipment = list() if self._equipment is None else self._equipment
        self._equipment.append(equipment)
        return self

    def remove_equipment(self, equipment: Equipment) -> UsagePoint:
        """
        Remove an ``Equipment`` from this ``UsagePoint``

        :param equipment: the :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment` to
        disassociate with this ``UsagePoint``.
        :raises: ValueError if ``equipment`` was not associated with this ``UsagePoint``.
        :return: A reference to this ``UsagePoint`` to allow fluent use.
        """
        self._equipment = safe_remove(self._equipment, equipment)
        return self

    def clear_equipment(self) -> UsagePoint:
        """
        Clear all equipment.
        :return: A reference to this ``UsagePoint`` to allow fluent use.
        """
        self._equipment = None
        return self

    def get_end_device(self, mrid: str) -> EndDevice:
        """
        Get the ``EndDevice`` for this ``UsagePoint`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61968.metering.metering.EndDevice`
        :return: The :class:`zepben.cimbend.iec61968.metering.metering.EndDevice` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._end_devices, mrid)

    def add_end_device(self, end_device: EndDevice) -> UsagePoint:
        """
        Add an ``EndDevice`` to this ``UsagePoint``

        :param end_device: the :class:`zepben.cimbend.iec61968.metering.metering.EndDevice` to
        associate with this ``UsagePoint``. Will only add to this object if it is not already associated.
        :return: A reference to this ``UsagePoint`` to allow fluent use.
        """
        if self._validate_reference(end_device, self.get_end_device, "An EndDevice"):
            return self
        self._end_devices = list() if self._end_devices is None else self._end_devices
        self._end_devices.append(end_device)
        return self

    def remove_end_device(self, end_device: EndDevice) -> UsagePoint:
        """
        Remove an ``EndDevice`` from this ``UsagePoint``
        :param end_device: the :class:`zepben.cimbend.iec61968.metering.metering.EndDevice` to
        disassociate with this ``UsagePoint``.
        :raises: ValueError if ``end_device`` was not associated with this ``UsagePoint``.
        :return: A reference to this ``UsagePoint`` to allow fluent use.
        """
        self._end_devices = safe_remove(self._end_devices, end_device)
        return self

    def clear_end_devices(self) -> UsagePoint:
        """
        Clear all end_devices.
        :return: A reference to this ``UsagePoint`` to allow fluent use.
        """
        self._end_devices = None
        return self

    def is_metered(self):
        """
        Check whether this `UsagePoint` is metered. A `UsagePoint` is metered if it's associated with at
        least one  :class:`EndDevice`.
        :return: True if this UsagePoint has an EndDevice, False otherwise.
        """
        return nlen(self._end_devices) > 0


@dataclass
class Meter(EndDevice):
    """
    Physical asset that performs the metering role of the usage point.
    Used for measuring consumption and detection of events.

    """

    @property
    def company_meter_id(self):
        """ :return: Get this Meters ID. Currently stored in ``IdentifiedObject.name`` """
        return self.name

    @company_meter_id.setter
    def company_meter_id(self, meter_id):
        """ :param meter_id: The ID to set for this Meter. Will use ``IdentifiedObject.name`` as a backing field. """
        self.name = meter_id

