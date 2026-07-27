#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['Equipment']

import datetime
from typing import Optional, Generator, List, TYPE_CHECKING, TypeVar, Type
from abc import ABCMeta
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_substation import LvSubstation
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
from zepben.ewb.model.cim.extensions.iec61970.base.core.site import Site
from zepben.ewb.util import ngen
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb import Alias
from zepben.ewb.boilerplate.collections.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint
    from zepben.ewb.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
    from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
    from zepben.ewb.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
    TEquipmentContainer = TypeVar("TEquipmentContainer", bound=EquipmentContainer)


@zb_dataclass
class Equipment(PowerSystemResource, metaclass=ABCMeta):
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

    _usage_points: Optional[List[UsagePoint]] = field(default=None)
    _equipment_containers: Optional[List[EquipmentContainer]] = field(default=None)
    _operational_restrictions: Optional[List[OperationalRestriction]] = field(default=None)
    _current_containers: Optional[List[EquipmentContainer]] = field(default=None)

    containers: MridCollection[EquipmentContainer] = LazyMridList(
        _equipment_containers,
        "An EquipmentContainer",
    )
    equipment_containers = Alias(containers)

    current_containers: MridCollection[EquipmentContainer] = LazyMridList(
        _current_containers,
        "A current EquipmentContainer",
    )

    usage_points: MridCollection[UsagePoint] = LazyMridList(
        _usage_points,
        "A UsagePoint",
    )

    operational_restrictions: MridCollection[OperationalRestriction] = LazyMridList(
        _operational_restrictions,
        "An OperationalRestriction",
    )


    @property
    def sites(self) -> Generator['Site', None, None]:
        """
        The `Site`s this equipment belongs to.
        """
        return ngen(_of_type(self._equipment_containers, Site))

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
        return ngen(_of_type(self._equipment_containers, Feeder))

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
        return ngen(_of_type(self._equipment_containers, LvFeeder))

    @property
    def normal_lv_substations(self) -> Generator[LvSubstation, None, None]:
        """
        The normal `LvSubstation's this equipment belongs to.
        """
        return ngen(_of_type(self._equipment_containers, LvSubstation))

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


    def num_sites(self) -> int:
        """
        Returns The number of `Site`s associated with this `Equipment`
        """
        return len(list(self.sites))


    # region deprecated list boilerplate
    # region containers boilerplate

    @deprecated("Use len(obj.containers) instead.")
    def num_containers(self) -> int:
        return len(self.containers)

    @deprecated("Use len(obj.containers) instead.")
    def num_substations(self) -> int:
        return len(self.containers)

    @deprecated("Use len(obj.containers) instead.")
    def num_normal_feeders(self) -> int:
        return len(self.containers)

    @deprecated("Use obj.containers.get_by_mrid(mrid) instead.")
    def get_container(self, mrid: str) -> EquipmentContainer:
        return self.containers.get_by_mrid(mrid)

    @deprecated("Use obj.containers.append(ec) instead.")
    def add_container(self, ec: EquipmentContainer) -> Equipment:
        self.containers.append(ec)
        return self

    @deprecated("Use obj.containers.remove(ec) instead.")
    def remove_container(self, ec: EquipmentContainer) -> Equipment:
        self.containers.remove(ec)
        return self

    @deprecated("Use obj.containers.clear() instead.")
    def clear_containers(self) -> Equipment:
        self.containers.clear()
        return self

    # endregion containers boilerplate

    # region current_containers boilerplate

    @deprecated("Use len(obj.current_containers) instead.")
    def num_current_containers(self) -> int:
        return len(self.current_containers)

    @deprecated("Use obj.current_containers.get_by_mrid(mrid) instead.")
    def get_current_container(self, mrid: str) -> EquipmentContainer:
        return self.current_containers.get_by_mrid(mrid)

    @deprecated("Use obj.current_containers.append(equipment_container) instead.")
    def add_current_container(self, equipment_container: EquipmentContainer) -> Equipment:
        self.current_containers.append(equipment_container)
        return self

    @deprecated("Use obj.current_containers.remove(equipment_container) instead.")
    def remove_current_container(self, equipment_container: EquipmentContainer) -> Equipment:
        self.current_containers.remove(equipment_container)
        return self

    @deprecated("Use obj.current_containers.clear() instead.")
    def clear_current_containers(self) -> Equipment:
        self.current_containers.clear()
        return self

    # endregion current_containers boilerplate

    # region usage_points boilerplate

    @deprecated("Use len(obj.usage_points) instead.")
    def num_usage_points(self) -> int:
        return len(self.usage_points)

    @deprecated("Use obj.usage_points.get_by_mrid(mrid) instead.")
    def get_usage_point(self, mrid: str) -> UsagePoint:
        return self.usage_points.get_by_mrid(mrid)

    @deprecated("Use obj.usage_points.append(up) instead.")
    def add_usage_point(self, up: UsagePoint) -> Equipment:
        self.usage_points.append(up)
        return self

    @deprecated("Use obj.usage_points.remove(up) instead.")
    def remove_usage_point(self, up: UsagePoint) -> Equipment:
        self.usage_points.remove(up)
        return self

    @deprecated("Use obj.usage_points.clear() instead.")
    def clear_usage_points(self) -> Equipment:
        self.usage_points.clear()
        return self

    # endregion usage_points boilerplate

    # region operational_restrictions boilerplate

    @deprecated("Use len(obj.operational_restrictions) instead.")
    def num_operational_restrictions(self) -> int:
        return len(self.operational_restrictions)

    @deprecated("Use obj.operational_restrictions.get_by_mrid(mrid) instead.")
    def get_operational_restriction(self, mrid: str) -> OperationalRestriction:
        return self.operational_restrictions.get_by_mrid(mrid)

    @deprecated("Use obj.operational_restrictions.append(op) instead.")
    def add_operational_restriction(self, op: OperationalRestriction) -> Equipment:
        self.operational_restrictions.append(op)
        return self

    @deprecated("Use obj.operational_restrictions.remove(op) instead.")
    def remove_operational_restriction(self, op: OperationalRestriction) -> Equipment:
        self.operational_restrictions.remove(op)
        return self

    @deprecated("Use obj.operational_restrictions.clear() instead.")
    def clear_operational_restrictions(self) -> Equipment:
        self.operational_restrictions.clear()
        return self

    # endregion operational_restrictions boilerplate

    # endregion deprecated list boilerplate


def _of_type(containers: Optional[List[EquipmentContainer]], ectype: Type[TEquipmentContainer]) -> Generator[TEquipmentContainer, None, None]:
    yield from (ec for ec in containers if isinstance(ec, ectype)) if containers is not None else {}
