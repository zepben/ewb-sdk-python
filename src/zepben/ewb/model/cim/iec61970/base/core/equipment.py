#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['Equipment']

import datetime
from typing import Optional, Generator, List, TYPE_CHECKING, TypeVar, Type

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
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


@dataslot
@boilermaker
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
    equipment_containers: List[EquipmentContainer] | None = MRIDListAccessor()
    operational_restrictions: List[OperationalRestriction] | None = MRIDListAccessor()
    current_containers: List[EquipmentContainer] | None = MRIDListAccessor()

    def _retype(self):
        self.usage_points: MRIDListRouter[UsagePoint] = ...
        self.equipment_containers: MRIDListRouter[EquipmentContainer] = ...
        self.operational_restrictions: MRIDListRouter[OperationalRestriction] = ...
        self.current_containers: MRIDListRouter[EquipmentContainer] = ...
    
    @property
    def sites(self) -> Generator[Site, None, None]:
        """
        The `Site`s this equipment belongs to.
        """
        return ngen(_of_type(self.equipment_containers, Site))

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
        return ngen(_of_type(self.equipment_containers, Feeder))

    def lv_feeders(self, network_state_operators: Type[NetworkStateOperators]) -> Generator[LvFeeder, None, None]:
        """
        The `LvFeeder` this equipment belongs too based on `NetworkStateOperators`
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
        return ngen(_of_type(self.equipment_containers, LvFeeder))

    @property
    def substations(self) -> Generator[Substation, None, None]:
        """
        The `Substation`s this equipment belongs to.
        """
        return ngen(_of_type(self.equipment_containers, Substation))

    @property
    def current_feeders(self) -> Generator[Feeder, None, None]:
        """
        The current `Feeder`s this equipment belongs to.
        """
        return ngen(_of_type(self.current_containers, Feeder))

    @property
    def current_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        The current `LvFeeder`s this equipment belongs to.
        """
        return ngen(_of_type(self.current_containers, LvFeeder))

    @property
    def containers(self) -> Generator[EquipmentContainer, None, None]:
        """
        The `EquipmentContainer`s this equipment belongs to.
        """
        return ngen(self.equipment_containers)

    def num_containers(self) -> int:
        """
        Returns The number of `EquipmentContainer`s associated with this `Equipment`
        """
        return nlen(self.equipment_containers)

    def num_substations(self) -> int:
        """
        Returns The number of `zepben.ewb.model.cim.iec61970.base.core.substation.Substation`s associated with this `Equipment`
        """
        return len(list(_of_type(self.equipment_containers, Substation)))

    def num_sites(self) -> int:
        """
        Returns The number of `Site`s associated with this `Equipment`
        """
        return len(list(_of_type(self.equipment_containers, Site)))

    def num_normal_feeders(self) -> int:
        """
        Returns The number of normal `Feeder`s associated with this `Equipment`
        """
        return len(list(_of_type(self.equipment_containers, Feeder)))

    @deprecated("BOILERPLATE: Use len(usage_points) instead")
    def num_usage_points(self) -> int:
        return len(self.usage_points)

    @deprecated("BOILERPLATE: Use len(current_containers) instead")
    def num_current_containers(self) -> int:
        return len(self.current_containers)

    @deprecated("BOILERPLATE: Use len(operational_restrictions) instead")
    def num_operational_restrictions(self) -> int:
        return len(self.operational_restrictions)

    @deprecated("BOILERPLATE: Use equipment_containers.get_by_mrid(mrid) instead")
    def get_container(self, mrid: str) -> EquipmentContainer:
        return self.equipment_containers.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use equipment_containers.append(ec) instead")
    def add_container(self, ec: EquipmentContainer) -> Equipment:
        self.equipment_containers.append(ec)
        return self

    @deprecated("Boilerplate: Use equipment_containers.remove(ec) instead")
    def remove_container(self, ec: EquipmentContainer) -> Equipment:
        self.equipment_containers.remove(ec)
        return self

    @deprecated("BOILERPLATE: Use equipment_containers.clear() instead")
    def clear_containers(self) -> Equipment:
        return self.equipment_containers.clear()

    @deprecated("BOILERPLATE: Use current_containers.get_by_mrid(mrid) instead")
    def get_current_container(self, mrid: str) -> EquipmentContainer:
        return self.current_containers.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use current_containers.append(equipment_container) instead")
    def add_current_container(self, equipment_container: EquipmentContainer) -> Equipment:
        self.current_containers.append(equipment_container)
        return self

    @deprecated("Boilerplate: Use current_containers.remove(equipment_container) instead")
    def remove_current_container(self, equipment_container: EquipmentContainer) -> Equipment:
        self.current_containers.remove(equipment_container)
        return self

    @deprecated("BOILERPLATE: Use current_containers.clear() instead")
    def clear_current_containers(self) -> Equipment:
        return self.current_containers.clear()

    @deprecated("BOILERPLATE: Use usage_points.get_by_mrid(mrid) instead")
    def get_usage_point(self, mrid: str) -> UsagePoint:
        return self.usage_points.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use usage_points.append(up) instead")
    def add_usage_point(self, up: UsagePoint) -> Equipment:
        self.usage_points.append(up)
        return self

    @deprecated("Boilerplate: Use usage_points.remove(up) instead")
    def remove_usage_point(self, up: UsagePoint) -> Equipment:
        self.usage_points.remove(up)
        return self

    @deprecated("BOILERPLATE: Use usage_points.clear() instead")
    def clear_usage_points(self) -> Equipment:
        return self.usage_points.clear()

    @deprecated("BOILERPLATE: Use operational_restrictions.get_by_mrid(mrid) instead")
    def get_operational_restriction(self, mrid: str) -> OperationalRestriction:
        return self.operational_restrictions.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use operational_restrictions.append(op) instead")
    def add_operational_restriction(self, op: OperationalRestriction) -> Equipment:
        self.operational_restrictions.append(op)
        return self

    @deprecated("Boilerplate: Use operational_restrictions.remove(op) instead")
    def remove_operational_restriction(self, op: OperationalRestriction) -> Equipment:
        self.operational_restrictions.remove(op)
        return self

    @deprecated("BOILERPLATE: Use operational_restrictions.clear() instead")
    def clear_operational_restrictions(self) -> Equipment:
        return self.operational_restrictions.clear()

def _of_type(containers: List[EquipmentContainer] | None, ectype: Type[TEquipmentContainer]) -> Generator[TEquipmentContainer, None, None]:
    yield from (ec for ec in containers if isinstance(ec, ectype)) if containers is not None else {}
