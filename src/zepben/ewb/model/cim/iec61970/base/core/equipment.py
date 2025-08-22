#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['Equipment']

import datetime
from typing import Optional, Generator, List, TYPE_CHECKING, TypeVar, Type

from zepben.ewb.collections.mrid_list import MRIDList
from zepben.ewb.collections.zepben_list import ZepbenList
from zepben.ewb.model.cim.extensions.iec61970.base.core.site import Site
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint
    from zepben.ewb.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
    from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
    from zepben.ewb.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
    TEquipmentContainer = TypeVar("TEquipmentContainer", bound=EquipmentContainer)


class Equipment(PowerSystemResource):
    """
    Abstract class, should only be used through subclasses.
    Any part of a power system that is a physical device, electronic or mechanical.
    """

    in_service: bool = True
    """If True, the equipment is in service."""
    normally_in_service: bool = True
    """If True, the equipment is _normally_ in service."""
    commissioned_date: Optional[datetime.datetime] = None
    """The date this equipment was commissioned into service."""

    usage_points: Optional[List[UsagePoint]] = None
    equipment_containers: Optional[List[EquipmentContainer]] = None
    operational_restrictions: Optional[List[OperationalRestriction]] = None
    current_containers: Optional[List[EquipmentContainer]] = None

    def __post_init__(self):
        self.usage_points : MRIDList[UsagePoint] = MRIDList(self.usage_points)
        self.equipment_containers : MRIDList[EquipmentContainer] = MRIDList(self.equipment_containers)
        self.operational_restrictions : MRIDList[OperationalRestriction] = MRIDList(self.operational_restrictions)
        self.current_containers : MRIDList[EquipmentContainer] = MRIDList(self.current_containers)


    @property
    def sites(self) -> Generator[Site, None, None]:
        """
        The `Site`s this equipment belongs to.
        """
        return self.equipment_containers.of_type(Site)

    def feeders(self, network_state_operators: Type[NetworkStateOperators]) -> Generator[Feeder, None, None]:
        """
        The `Feeder` this equipment belongs too based on `NetworkStateOperators`
        """
        if network_state_operators.NORMAL:
            return self.normal_feeders
        else:
            return self.current_feeders

    @property
    def normal_feeders(self) -> Generator[Feeder, None, None]:
        """
        The normal `Feeder`s this equipment belongs to.
        """
        return self.equipment_containers.of_type(Feeder)

    def lv_feeders(self, network_state_operators: Type[NetworkStateOperators]) -> Generator[LvFeeder, None, None]:
        """
        The `LvFeeder` this equipment belongs to based on `NetworkStateOperators`
        """
        if network_state_operators.NORMAL:
            return self.normal_lv_feeders
        else:
            return self.current_lv_feeders

    @property
    def normal_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        The normal `LvFeeder`s this equipment belongs to.
        """
        return self.equipment_containers.of_type(LvFeeder)

    @property
    def substations(self) -> Generator[Substation, None, None]:
        """
        The `Substation`s this equipment belongs to.
        """
        return self.equipment_containers.of_type(Substation)

    @property
    def current_feeders(self) -> Generator[Feeder, None, None]:
        """
        The current `Feeder`s this equipment belongs to.
        """
        return self.equipment_containers.of_type(Feeder)

    @property
    def current_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        The current `LvFeeder`s this equipment belongs to.
        """
        return self.current_containers.of_type(LvFeeder)

    @property
    def containers(self) -> ZepbenList[EquipmentContainer]:
        """
        The `EquipmentContainer`s this equipment belongs to.
        """
        return self.equipment_containers

    def num_containers(self) -> int:
        """
        Returns The number of `EquipmentContainer`s associated with this `Equipment`
        """
        return len(self.equipment_containers)

    def num_substations(self) -> int:
        """
        Returns The number of `zepben.ewb.model.cim.iec61970.base.core.substation.Substation`s associated with this `Equipment`
        """
        return self.equipment_containers.num_of_type(Substation)

    def num_sites(self) -> int:
        """
        Returns The number of `Site`s associated with this `Equipment`
        """
        return self.equipment_containers.num_of_type(Site)

    def num_normal_feeders(self) -> int:
        """
        Returns The number of normal `Feeder`s associated with this `Equipment`
        """
        return self.equipment_containers.num_of_type(Feeder)

    def num_usage_points(self) -> int:
        """
        Returns The number of `UsagePoint`s associated with this `Equipment`
        """
        return len(self.usage_points)

    def num_current_containers(self) -> int:
        """
        Returns The number of `EquipmentContainer`s associated with this `Equipment`
        """
        return len(self.current_containers)

    def num_operational_restrictions(self) -> int:
        """
        Returns The number of `OperationalRestriction`s associated with this `Equipment`
        """
        return len(self.operational_restrictions)

    def get_container(self, mrid: str) -> EquipmentContainer:
        """
        Get the `EquipmentContainer` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `EquipmentContainer`
        Returns The `EquipmentContainer` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.equipment_containers.get_by_mrid(mrid)

    def add_container(self, ec: EquipmentContainer) -> Equipment:
        """
        Associate an `EquipmentContainer` with this `Equipment`

        `ec` The `EquipmentContainer` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `EquipmentContainer` with the same `mrid` already exists for this `Equipment`.
        """
        # TODO: remove this blasphemy
        if self._validate_reference(ec, self.get_container, "An EquipmentContainer"):
            return self
        self.equipment_containers.add(ec)
        return self

    def remove_container(self, ec: EquipmentContainer) -> Equipment:
        """
        Disassociate `ec` from this `Equipment`.

        `ec` The `EquipmentContainer` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `ec` was not associated with this `Equipment`.
        """

        self.equipment_containers.remove(ec)
        return self

    def clear_containers(self) -> Equipment:
        """
        Clear all equipment.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self.equipment_containers.clear()
        return self

    def get_current_container(self, mrid: str) -> EquipmentContainer:
        """
        Get the `EquipmentContainer` for this `Equipment` in the current state of the network, identified by `mrid`

        `mrid` The mRID of the required `EquipmentContainer`
        Returns The `EquipmentContainer` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.current_containers.get_by_mrid(mrid)

    def add_current_container(self, equipment_container: EquipmentContainer) -> Equipment:
        """
        Associate `equipment_container` with this `Equipment` in the current state of the network.

        `equipment_container` The `EquipmentContainer` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `EquipmentContainer` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(equipment_container, self.get_current_container, "A current EquipmentContainer"):
            return self
        self.current_containers.add(equipment_container)
        return self

    def remove_current_container(self, equipment_container: EquipmentContainer) -> Equipment:
        """
        Disassociate `equipment_container` from this `Equipment` in the current state of the network.

        `equipment_container` The `EquipmentContainer` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `equipment_container` was not associated with this `Equipment`.
        """
        self.current_containers.remove(equipment_container)
        return self

    def clear_current_containers(self) -> Equipment:
        """
        Clear all current `EquipmentContainer`s in the current state of the network.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self.current_containers.clear()
        return self

    def get_usage_point(self, mrid: str) -> UsagePoint:
        """
        Get the `UsagePoint` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `UsagePoint`
        Returns The `UsagePoint` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.usage_points.get_by_mrid(mrid)

    def add_usage_point(self, up: UsagePoint) -> Equipment:
        """
        Associate `up` with this `Equipment`.

        `up` the `UsagePoint` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `UsagePoint` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(up, self.get_usage_point, "A UsagePoint"):
            return self
        self.usage_points.add(up)
        return self

    def remove_usage_point(self, up: UsagePoint) -> Equipment:
        """
        Disassociate `up` from this `Equipment`.

        `up` The `UsagePoint` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `Equipment`.
        """
        self.usage_points.remove(up)
        return self

    def clear_usage_points(self) -> Equipment:
        """
        Clear all usage_points.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self.usage_points.clear()
        return self

    def get_operational_restriction(self, mrid: str) -> OperationalRestriction:
        """
        Get the `OperationalRestriction` for this `Equipment` identified by `mrid`

        `mrid` The mRID of the required `OperationalRestriction`
        Returns The `OperationalRestriction` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.operational_restrictions.get_by_mrid(mrid)

    def add_operational_restriction(self, op: OperationalRestriction) -> Equipment:
        """
        Associate `op` with this `Equipment`.

        `op` The `OperationalRestriction` to associate with this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if another `OperationalRestriction` with the same `mrid` already exists for this `Equipment`.
        """
        if self._validate_reference(op, self.get_operational_restriction, "An OperationalRestriction"):
            return self
        self.operational_restrictions.add(op)
        return self

    def remove_operational_restriction(self, op: OperationalRestriction) -> Equipment:
        """
        Disassociate `up` from this `Equipment`.

        `op` The `OperationalRestriction` to disassociate from this `Equipment`.
        Returns A reference to this `Equipment` to allow fluent use.
        Raises `ValueError` if `op` was not associated with this `Equipment`.
        """
        self.operational_restrictions.remove(op)
        return self

    def clear_operational_restrictions(self) -> Equipment:
        """
        Clear all `OperationalRestrictions`.
        Returns A reference to this `Equipment` to allow fluent use.
        """
        self.operational_restrictions.clear()
        return self


