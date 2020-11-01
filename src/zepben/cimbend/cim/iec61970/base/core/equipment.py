#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List

from zepben.cimbend.cim.iec61970.base.core.equipment_container import Feeder, Site
from zepben.cimbend.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.cimbend.cim.iec61970.base.core.substation import Substation
from zepben.cimbend.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ['Equipment']


class Equipment(PowerSystemResource):
    """
    Abstract class, should only be used through subclasses.
    Any part of a power system that is a physical device, electronic or mechanical.
    """

    in_service: bool = True
    """If True, the equipment is in service."""
    normally_in_service: bool = True
    """If True, the equipment is _normally_ in service."""

    _usage_points: Optional[List[UsagePoint]] = None
    _equipment_containers: Optional[List[EquipmentContainer]] = None
    _operational_restrictions: Optional[List[OperationalRestriction]] = None
    _current_feeders: Optional[List[Feeder]] = None

    def __init__(self, usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                 operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None):
        if usage_points:
            for up in usage_points:
                self.add_usage_point(up)
        if equipment_containers:
            for container in equipment_containers:
                self.add_container(container)
        if operational_restrictions:
            for restriction in operational_restrictions:
                self.add_restriction(restriction)
        if current_feeders:
            for cf in current_feeders:
                self.add_current_feeder(cf)

    @property
    def equipment_containers(self) -> Generator[Equipment, None, None]:
        """
        The `zepben.cimbend.cim.iec61970.base.core.equipment_container.EquipmentContainer`s this equipment belongs to.
        """
        return ngen(self._equipment_containers)

    @property
    def current_feeders(self) -> Generator[Feeder, None, None]:
        """
        The current `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder`s this equipment belongs to.
        """
        return ngen(self._current_feeders)

    @property
    def normal_feeders(self) -> Generator[Feeder, None, None]:
        """
        The normal `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder`s this equipment belongs to.
        """
        for feeder in self._equipment_containers_of_type(Feeder):
            yield feeder

    @property
    def sites(self) -> Generator[Site, None, None]:
        """
        The `zepben.cimbend.cim.iec61970.base.core.equipment_container.Site`s this equipment belongs to.
        """
        for site in self._equipment_containers_of_type(Site):
            yield site

    @property
    def substations(self) -> Generator[Substation, None, None]:
        """
        The `zepben.cimbend.cim.iec61970.base.core.substation.Substation`s this equipment belongs to.
        """
        for sub in self._equipment_containers_of_type(Substation):
            yield sub

    @property
    def usage_points(self) -> Generator[UsagePoint, None, None]:
        """
        The `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint`s for this equipment.
        """
        return ngen(self._usage_points)

    @property
    def operational_restrictions(self) -> Generator[OperationalRestriction, None, None]:
        """
        The `zepben.cimbend.cim.iec61968.operations.operational_restriction.OperationalRestriction`s that this equipment is associated with.
        """
        return ngen(self._operational_restrictions)

    def num_equipment_containers(self) -> int:
        """
        Returns The number of `zepben.cimbend.cim.iec61970.base.core.equipment_container.EquipmentContainer`s associated with this `Equipment`
        """
        return nlen(self._equipment_containers)

    def num_substations(self) -> int:
        """
        Returns The number of `zepben.cimbend.cim.iec61970.base.core.substation.Substation`s associated with this `Equipment`
        """
        return len(self._equipment_containers_of_type(Substation))

    def num_sites(self) -> int:
        """
        Returns The number of `zepben.cimbend.cim.iec61970.base.core.equipment_container.Site`s associated with this `Equipment`
        """
        return len(self._equipment_containers_of_type(Site))

    def num_normal_feeders(self) -> int:
        """
        Returns The number of normal `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder`s associated with this `Equipment`
        """
        return len(self._equipment_containers_of_type(Feeder))

    def num_usage_points(self) -> int:
        """
        Returns The number of `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint`s associated with this `Equipment`
        """
        return nlen(self._usage_points)

    def num_current_feeders(self) -> int:
        """
        Returns The number of `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder`s associated with this `Equipment`
        """
        return nlen(self._current_feeders)

    def num_restrictions(self) -> int:
        """
        Returns The number of `zepben.cimbend.cim.iec61968.operations.operational_restriction.OperationalRestriction`s associated with this `Equipment`
        """
        return nlen(self._operational_restrictions)

    def get_container(self, mrid: str) -> Equipment:
        """
        Get the `zepben.cimbend.cim.iec61970.base.core.equipment_container.EquipmentContainer` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `zepben.cimbend.cim.iec61970.base.core.equipment_container.EquipmentContainer`
        Returns The `zepben.cimbend.cim.iec61970.base.core.equipment_container.EquipmentContainer` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._equipment_containers, mrid)

    def add_container(self, ec: EquipmentContainer) -> Equipment:
        """
        Associate an `zepben.cimbend.cim.iec61970.base.core.equipment_container.EquipmentContainer` with this `Equipment`

        `ec` The `zepben.cimbend.cim.iec61970.base.core.equipment_container.EquipmentContainer` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `EquipmentContainer` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(ec, self.get_container, "An EquipmentContainer"):
            return self
        self._equipment_containers = list() if self._equipment_containers is None else self._equipment_containers
        self._equipment_containers.append(ec)
        return self

    def remove_containers(self, ec: EquipmentContainer) -> Equipment:
        """
        Disassociate `ec` from this `Equipment`.

        `ec` The `zepben.cimbend.cim.iec61970.base.core.equipment_container.EquipmentContainer` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `ec` was not associated with this `Equipment`.
        """
        self._equipment_containers = safe_remove(self._equipment_containers, ec)
        return self

    def clear_containers(self) -> Equipment:
        """
        Clear all equipment.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self._equipment_containers = None
        return self

    def get_current_feeder(self, mrid: str) -> Equipment:
        """
        Get the `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder`
        Returns The `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._current_feeders, mrid)

    def add_current_feeder(self, feeder: Feeder) -> Equipment:
        """
        Associate `feeder` with this `Equipment`.

        `feeder` The `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `Feeder` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(feeder, self.get_current_feeder, "A Feeder"):
            return self
        self._current_feeders = list() if self._current_feeders is None else self._current_feeders
        self._current_feeders.append(feeder)
        return self

    def remove_current_feeder(self, feeder: Feeder) -> Equipment:
        """
        Disassociate `feeder` from this `Equipment`

        `feeder` The `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `feeder` was not associated with this `Equipment`.
        """
        self._current_feeders = safe_remove(self._current_feeders, feeder)
        return self

    def clear_current_feeders(self) -> Equipment:
        """
        Clear all current `Feeder`s.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self._current_feeders = None
        return self

    def get_usage_point(self, mrid: str) -> UsagePoint:
        """
        Get the `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint`
        Returns The `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._usage_points, mrid)

    def add_usage_point(self, up: UsagePoint) -> Equipment:
        """
        Associate `up` with this `Equipment`.

        `up` the `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `UsagePoint` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(up, self.get_usage_point, "A UsagePoint"):
            return self
        self._usage_points = list() if self._usage_points is None else self._usage_points
        self._usage_points.append(up)
        return self

    def remove_usage_point(self, up: UsagePoint) -> Equipment:
        """
        Disassociate `up` from this `Equipment`.

        `up` The `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `Equipment`.
        """
        self._usage_points = safe_remove(self._usage_points, up)
        return self

    def clear_usage_points(self) -> Equipment:
        """
        Clear all usage_points.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self._usage_points = None
        return self

    def get_restriction(self, mrid: str) -> OperationalRestriction:
        """
        Get the `zepben.cimbend.cim.iec61968.operations.operational_restriction.OperationalRestriction` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `zepben.cimbend.cim.iec61968.operations.operational_restriction.OperationalRestriction`
        Returns The `zepben.cimbend.cim.iec61968.operations.operational_restriction.OperationalRestriction` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._operational_restrictions, mrid)

    def add_restriction(self, op: OperationalRestriction) -> Equipment:
        """
        Associate `op` with this `Equipment`.

        `op` The `zepben.cimbend.cim.iec61968.operations.operational_restriction.OperationalRestriction` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `OperationalRestriction` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(op, self.get_restriction, "An OperationalRestriction"):
            return self
        self._operational_restrictions = list() if self._operational_restrictions is None else self._operational_restrictions
        self._operational_restrictions.append(op)
        return self

    def remove_restriction(self, op: OperationalRestriction) -> Equipment:
        """
        Disassociate `up` from this `Equipment`.

        `op` The `zepben.cimbend.cim.iec61968.operations.operational_restriction.OperationalRestriction` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `op` was not associated with this `Equipment`.
        """
        self._operational_restrictions = safe_remove(self._operational_restrictions, op)
        return self

    def clear_restrictions(self) -> Equipment:
        """
        Clear all `OperationalRestrictions`.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self._operational_restrictions = None
        return self

    def _equipment_containers_of_type(self, ectype: type) -> List[EquipmentContainer]:
        """Get the `EquipmentContainer`s for this `Equipment` of type `ectype`"""
        if self._equipment_containers:
            return [ec for ec in self._equipment_containers if isinstance(ec, ectype)]
        else:
            return []
