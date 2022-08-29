#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List, TYPE_CHECKING, TypeVar, Type

if TYPE_CHECKING:
    from zepben.evolve import UsagePoint, EquipmentContainer, OperationalRestriction

    TEquipmentContainer = TypeVar("TEquipmentContainer", bound=EquipmentContainer)

from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, Site
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.core.substation import Substation
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder
from zepben.evolve.util import nlen, get_by_mrid, ngen, safe_remove

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
    _current_containers: Optional[List[EquipmentContainer]] = None

    def __init__(self, usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                 operational_restrictions: List[OperationalRestriction] = None, current_containers: List[EquipmentContainer] = None, **kwargs):
        super(Equipment, self).__init__(**kwargs)
        if usage_points:
            for up in usage_points:
                self.add_usage_point(up)
        if equipment_containers:
            for container in equipment_containers:
                self.add_container(container)
        if operational_restrictions:
            for restriction in operational_restrictions:
                self.add_operational_restriction(restriction)
        if current_containers:
            for cf in current_containers:
                self.add_current_container(cf)

    @property
    def sites(self) -> Generator[Site, None, None]:
        """
        The `Site`s this equipment belongs to.
        """
        return ngen(_of_type(self._equipment_containers, Site))


    @property
    def normal_feeders(self) -> Generator[Feeder, None, None]:
        """
        The normal `Feeder`s this equipment belongs to.
        """
        return ngen(_of_type(self._equipment_containers, Feeder))

    @property
    def normal_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        The normal `LvFeeder`s this equipment belongs to.
        """
        return ngen(_of_type(self._equipment_containers, LvFeeder))

    @property
    def substations(self) -> Generator[Substation, None, None]:
        """
        The `Substation`s this equipment belongs to.
        """
        return ngen(_of_type(self._equipment_containers, Substation))

    @property
    def current_feeders(self) -> Generator[Feeder, None, None]:
        """
        The current `Feeder`s this equipment belongs to.
        """
        return ngen(_of_type(self._current_containers, Feeder))

    @property
    def current_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        The current `LvFeeder`s this equipment belongs to.
        """
        return ngen(_of_type(self._current_containers, LvFeeder))

    @property
    def containers(self) -> Generator[EquipmentContainer, None, None]:
        """
        The `EquipmentContainer`s this equipment belongs to.
        """
        return ngen(self._equipment_containers)

    def num_containers(self) -> int:
        """
        Returns The number of `EquipmentContainer`s associated with this `Equipment`
        """
        return nlen(self._equipment_containers)

    def num_substations(self) -> int:
        """
        Returns The number of `zepben.evolve.cim.iec61970.base.core.substation.Substation`s associated with this `Equipment`
        """
        return len(_of_type(self._equipment_containers, Substation))

    def num_sites(self) -> int:
        """
        Returns The number of `Site`s associated with this `Equipment`
        """
        return len(_of_type(self._equipment_containers, Site))

    def num_normal_feeders(self) -> int:
        """
        Returns The number of normal `Feeder`s associated with this `Equipment`
        """
        return len(_of_type(self._equipment_containers, Feeder))

    def num_usage_points(self) -> int:
        """
        Returns The number of `UsagePoint`s associated with this `Equipment`
        """
        return nlen(self._usage_points)

    def num_current_containers(self) -> int:
        """
        Returns The number of `EquipmentContainer`s associated with this `Equipment`
        """
        return nlen(self._current_containers)

    def num_operational_restrictions(self) -> int:
        """
        Returns The number of `OperationalRestriction`s associated with this `Equipment`
        """
        return nlen(self._operational_restrictions)

    def get_container(self, mrid: str) -> EquipmentContainer:
        """
        Get the `EquipmentContainer` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `EquipmentContainer`
        Returns The `EquipmentContainer` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._equipment_containers, mrid)

    def add_container(self, ec: EquipmentContainer) -> Equipment:
        """
        Associate an `EquipmentContainer` with this `Equipment`

        `ec` The `EquipmentContainer` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `EquipmentContainer` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(ec, self.get_container, "An EquipmentContainer"):
            return self
        self._equipment_containers = list() if self._equipment_containers is None else self._equipment_containers
        self._equipment_containers.append(ec)
        return self

    def remove_container(self, ec: EquipmentContainer) -> Equipment:
        """
        Disassociate `ec` from this `Equipment`.

        `ec` The `EquipmentContainer` to disassociate from this `Equipment`.
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

    @property
    def current_containers(self) -> Generator[EquipmentContainer, None, None]:
        """
        The `EquipmentContainer`s this equipment belongs to in the current state of the network.
        """
        return ngen(self._current_containers)

    def get_current_container(self, mrid: str) -> EquipmentContainer:
        """
        Get the `EquipmentContainer` for this `Equipment` in the current state of the network, identified by `mrid`

        `mrid` The mRID of the required `EquipmentContainer`
        Returns The `EquipmentContainer` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._current_containers, mrid)

    def add_current_container(self, equipment_container: EquipmentContainer) -> Equipment:
        """
        Associate `equipment_container` with this `Equipment` in the current state of the network.

        `equipment_container` The `EquipmentContainer` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `EquipmentContainer` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(equipment_container, self.get_current_container, "A current EquipmentContainer"):
            return self
        self._current_containers = list() if self._current_containers is None else self._current_containers
        self._current_containers.append(equipment_container)
        return self

    def remove_current_container(self, equipment_container: EquipmentContainer) -> Equipment:
        """
        Disassociate `equipment_container` from this `Equipment` in the current state of the network.

        `equipment_container` The `EquipmentContainer` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `equipment_container` was not associated with this `Equipment`.
        """
        self._current_containers = safe_remove(self._current_containers, equipment_container)
        return self

    def clear_current_containers(self) -> Equipment:
        """
        Clear all current `EquipmentContainer`s in the current state of the network.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self._current_containers = None
        return self

    @property
    def usage_points(self) -> Generator[UsagePoint, None, None]:
        """
        The `UsagePoint`s for this equipment.
        """
        return ngen(self._usage_points)

    def get_usage_point(self, mrid: str) -> UsagePoint:
        """
        Get the `UsagePoint` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `UsagePoint`
        Returns The `UsagePoint` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._usage_points, mrid)

    def add_usage_point(self, up: UsagePoint) -> Equipment:
        """
        Associate `up` with this `Equipment`.

        `up` the `UsagePoint` to associate with this `Equipment`.
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

        `up` The `UsagePoint` to disassociate from this `Equipment`.
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

    @property
    def operational_restrictions(self) -> Generator[OperationalRestriction, None, None]:
        """
        The `OperationalRestriction`s that this equipment is associated with.
        """
        return ngen(self._operational_restrictions)

    def get_operational_restriction(self, mrid: str) -> OperationalRestriction:
        """
        Get the `OperationalRestriction` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `OperationalRestriction`
        Returns The `OperationalRestriction` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._operational_restrictions, mrid)

    def add_operational_restriction(self, op: OperationalRestriction) -> Equipment:
        """
        Associate `op` with this `Equipment`.

        `op` The `OperationalRestriction` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `OperationalRestriction` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(op, self.get_operational_restriction, "An OperationalRestriction"):
            return self
        self._operational_restrictions = list() if self._operational_restrictions is None else self._operational_restrictions
        self._operational_restrictions.append(op)
        return self

    def remove_operational_restriction(self, op: OperationalRestriction) -> Equipment:
        """
        Disassociate `up` from this `Equipment`.

        `op` The `OperationalRestriction` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `op` was not associated with this `Equipment`.
        """
        self._operational_restrictions = safe_remove(self._operational_restrictions, op)
        return self

    def clear_operational_restrictions(self) -> Equipment:
        """
        Clear all `OperationalRestrictions`.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self._operational_restrictions = None
        return self


def _of_type(containers: Optional[List[EquipmentContainer]], ectype: Type[TEquipmentContainer]) -> List[TEquipmentContainer]:
    if containers:
        return [ec for ec in containers if isinstance(ec, ectype)]
    else:
        return []
