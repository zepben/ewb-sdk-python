#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['Equipment']

import datetime
from typing import Generator, List, TYPE_CHECKING, TypeVar, Type, Iterable

from typing_extensions import deprecated

from zepben.ewb.collections.autoslot import dataslot
from zepben.ewb.collections.boilerplate import MRIDListAccessor, MRIDListRouter, NamingOptions
from zepben.ewb.model.cim.extensions.iec61970.base.core.site import Site
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.core.substation import Substation

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint
    from zepben.ewb.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
    from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
    from zepben.ewb.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
    TEquipmentContainer = TypeVar("TEquipmentContainer", bound=EquipmentContainer)


@dataslot
class Equipment(PowerSystemResource):
    """
    Abstract class, should only be used through subclasses.
    Any part of a power system that is a physical device, electronic or mechanical.
    """

    in_service: bool = True
    """If True, the equipment is in service."""
    normally_in_service: bool = True
    """If True, the equipment is _normally_ in service."""
    commissioned_date: datetime.datetime | None = None
    """The date this equipment was commissioned into service."""

    usage_points: List[UsagePoint] | None = MRIDListAccessor()
    equipment_containers: List[EquipmentContainer] | None = MRIDListAccessor(
        naming_options = NamingOptions(attr_alias='containers'))
    operational_restrictions: List[OperationalRestriction] | None = MRIDListAccessor()
    current_containers: List[EquipmentContainer] | None = MRIDListAccessor()

    def _retype(self):
        self.usage_points: MRIDListRouter = ...
        self.equipment_containers: MRIDListRouter = ...
        self.operational_restrictions: MRIDListRouter = ...
        self.current_containers: MRIDListRouter = ...

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
    def containers(self) -> Iterable[EquipmentContainer]:
        """
        The `EquipmentContainer`s this equipment belongs to.
        """
        return self.equipment_containers

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

    # Equipment containers

    @deprecated("Use len(equipment_containers) instead.")
    def num_containers(self) -> int: ...

    @deprecated("Use equipment_containers.get_by_mrid() instead")
    def get_container(self, mrid: str) -> EquipmentContainer: ...

    @deprecated("Use equipment_containers.append() instead")
    def add_container(self, ec: EquipmentContainer) -> Equipment: ...

    @deprecated("Use equipment_containers.remove() instead")
    def remove_container(self, ec: EquipmentContainer) -> Equipment: ...

    @deprecated("Use equipment_containers.clear() instead")
    def clear_containers(self) -> Equipment: ...

    # Current containers

    @deprecated("Use len(current_containers) instead.")
    def num_current_containers(self) -> int: ...

    @deprecated("Use current_containers.get_by_mrid() instead")
    def get_current_container(self, mrid: str) -> EquipmentContainer: ...

    @deprecated("Use current_containers.append() instead")
    def add_current_container(self, equipment_container: EquipmentContainer) -> Equipment: ...

    @deprecated("Use current_containers.remove() instead")
    def remove_current_container(self, equipment_container: EquipmentContainer) -> Equipment: ...

    @deprecated("Use current_containers.clear() instead")
    def clear_current_containers(self) -> Equipment: ...

    # Usage points

    @deprecated("Use len(usage_points) instead.")
    def num_usage_points(self) -> int: ...

    @deprecated("Use usage_points.get_by_mrid() instead")
    def get_usage_point(self, mrid: str) -> UsagePoint: ...

    @deprecated("Use usage_points.append() instead")
    def add_usage_point(self, up: UsagePoint) -> Equipment: ...

    @deprecated("Use usage_points.remove() instead")
    def remove_usage_point(self, up: UsagePoint) -> Equipment: ...

    @deprecated("Use usage_points.clear() instead")
    def clear_usage_points(self) -> Equipment: ...

    # Operational restrictions

    @deprecated("Use len(operational_restrictions) instead.")
    def num_operational_restrictions(self) -> int: ...

    @deprecated("Use operational_restrictions.get_by_mrid() instead")
    def get_operational_restriction(self, mrid: str) -> OperationalRestriction: ...

    @deprecated("Use operational_restrictions.append() instead")
    def add_operational_restriction(self, op: OperationalRestriction) -> Equipment: ...

    @deprecated("Use operational_restrictions.remove() instead")
    def remove_operational_restriction(self, op: OperationalRestriction) -> Equipment: ...

    @deprecated("Use operational_restrictions.clear() instead")
    def clear_operational_restrictions(self) -> Equipment: ...
