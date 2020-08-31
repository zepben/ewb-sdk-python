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

from dataclasses import dataclass, field, InitVar, MISSING
from typing import Optional, Generator, List

from zepben.cimbend.cim.iec61970.base.core.equipment_container import Feeder, Site
from zepben.cimbend.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.cimbend.cim.iec61970.base.core.substation import Substation
from zepben.cimbend.util import nlen, get_by_mrid, require, contains_mrid, ngen

__all__ = ['Equipment']


@dataclass
class Equipment(PowerSystemResource):
    """
    Abstract class, should only be used through subclasses.
    Any part of a power system that is a physical device, electronic or mechanical.
    Attributes -
        in_service : If True, the equipment is in service.
        normally_in_service : If True, the equipment is _normally_ in service.
        usage_points : List of all usage points associated with this equipment
        equipment_containers : Mapping of equipment container types to equipment container ID's this equipment
                                 is associated with.
        operational_restrictions : The :class:`zepben.cimbend.cim.iec61968.operations.operational_restriction.OperationalRestriction`s
                                   associated with this ``Equipment``.
        current_feeders : The current :class:`zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder`s associated
                          with this ``Equipment``. Current feeders

    """

    in_service: bool = True
    normally_in_service: bool = True
    usagepoints: InitVar[List[UsagePoint]] = field(default=list())
    _usage_points: Optional[List[UsagePoint]] = field(init=False, default=None)
    equipmentcontainers: InitVar[List[EquipmentContainer]] = field(default=list())
    _equipment_containers: Optional[List[EquipmentContainer]] = field(init=False, default=None)
    operationalrestrictions: InitVar[List[OperationalRestriction]] = field(default=list())
    _operational_restrictions: Optional[List[OperationalRestriction]] = field(init=False, default=None)
    currentfeeders: InitVar[List[Feeder]] = field(default=list())
    _current_feeders: Optional[List[Feeder]] = field(init=False, default=None)

    def __post_init__(self, usagepoints: List[UsagePoint],
                      equipmentcontainers: List[EquipmentContainer],
                      operationalrestrictions: List[OperationalRestriction],
                      currentfeeders: List[Feeder]):
        super().__post_init__()
        for up in usagepoints:
            self.add_usage_point(up)
        for container in equipmentcontainers:
            self.add_container(container)
        for restriction in operationalrestrictions:
            self.add_restriction(restriction)
        for cf in currentfeeders:
            self.add_current_feeder(cf)

    @property
    def position_points(self):
        return self.location.position_points

    @property
    def num_equipment_containers(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61970.base.core.equipment_container.EquipmentContainer`s associated
        with this ``Equipment``
        """
        return nlen(self._equipment_containers)

    @property
    def num_substations(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61970.base.core.substation.Substation`s associated
        with this ``Equipment``
        """
        return len(self._equipment_containers_of_type(Substation))

    @property
    def num_sites(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61970.base.core.equipment_container.Site`s associated
        with this ``Equipment``
        """
        return len(self._equipment_containers_of_type(Site))

    @property
    def num_normal_feeders(self):
        """
        :return: The number of normal :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder`s associated
        with this ``Equipment``
        """
        return len(self._equipment_containers_of_type(Feeder))

    @property
    def equipment_containers(self) -> Generator[Equipment, None, None]:
        """
        :return: Generator over the ``EquipmentContainer``s of this ``Equipment``.
        """
        return ngen(self._equipment_containers)

    @property
    def current_feeders(self) -> Generator[Feeder, None, None]:
        """
        :return: Generator over the current ``Feeder``s of this ``Equipment``.
        """
        return ngen(self._current_feeders)

    @property
    def normal_feeders(self) -> Generator[Feeder, None, None]:
        """
        :return: Generator over the normal ``Feeder``s of this ``Equipment``.
        """
        for feeder in self._equipment_containers_of_type(Feeder):
            yield feeder

    @property
    def sites(self) -> Generator[Site, None, None]:
        """
        :return: Generator over the ``Site``s of this ``Equipment``.
        """
        for site in self._equipment_containers_of_type(Site):
            yield site

    @property
    def substations(self) -> Generator[Substation, None, None]:
        """
        :return: Generator over the ``Substation``s of this ``Equipment``.
        """
        for sub in self._equipment_containers_of_type(Substation):
            yield sub

    @property
    def usage_points(self) -> Generator[UsagePoint, None, None]:
        """
        :return: Generator over the ``UsagePoint``s of this ``Equipment``.
        """
        return ngen(self._usage_points)

    @property
    def operational_restrictions(self) -> Generator[OperationalRestriction, None, None]:
        """
        :return: Generator over the ``OperationalRestriction``s of this ``Equipment``.
        """
        return ngen(self._operational_restrictions)

    def get_container(self, mrid: str) -> Equipment:
        """
        Get the ``EquipmentContainer`` for this ``Equipment`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61970.base.core.equipment_container.EquipmentContainer`
        :return: The :class:`zepben.cimbend.iec61970.base.core.equipment_container.EquipmentContainer` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._equipment_containers, mrid)

    def add_container(self, ec: EquipmentContainer) -> Equipment:
        """
        Associate an ``EquipmentContainer`` with this ``Equipment``
        :param ec: the :class:`zepben.cimbend.iec61970.base.core.equipment_container.EquipmentContainer` to
        associate with this ``Equipment``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        require(not contains_mrid(self._equipment_containers, ec.mrid),
                lambda: f"An EquipmentContainer with mRID {ec.mrid} already exists in {str(self)}.")
        self._equipment_containers = list() if self._equipment_containers is None else self._equipment_containers
        self._equipment_containers.append(ec)
        return self

    def remove_containers(self, ec: EquipmentContainer) -> Equipment:
        """
        :param ec: the :class:`zepben.cimbend.iec61970.base.core.equipment_container.EquipmentContainer` to
        disassociate with this ``Equipment``.
        :raises: KeyError if ``ec`` was not associated with this ``Equipment``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        if self._equipment_containers is not None:
            self._equipment_containers.remove(ec)
            if not self._equipment_containers:
                self._equipment_containers = None
        else:
            raise KeyError(ec)

        return self

    def clear_containers(self) -> Equipment:
        """
        Clear all equipment.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        self._equipment_containers = None
        return self

    @property
    def num_current_feeders(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder`s associated
        with this ``Equipment``
        """
        return nlen(self._current_feeders)

    def get_current_feeder(self, mrid: str) -> Equipment:
        """
        Get the ``Feeder`` for this ``Equipment`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder`
        :return: The :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._current_feeders, mrid)

    def add_current_feeder(self, feeder: Feeder) -> Equipment:
        """
        :param feeder: the :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder` to
        associate with this ``Equipment``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        require(not contains_mrid(self._current_feeders, feeder.mrid),
                lambda: f"A current Feeder with mRID {feeder.mrid} already exists in {str(self)}.")
        self._current_feeders = list() if self._current_feeders is None else self._current_feeders
        self._current_feeders.append(feeder)
        return self

    def remove_current_feeder(self, feeder: Feeder) -> Equipment:
        """
        :param feeder: the :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder` to
        disassociate with this ``Equipment``.
        :raises: KeyError if ``feeder`` was not associated with this ``Equipment``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        if self._current_feeders is not None:
            self._current_feeders.remove(feeder)
            if not self._current_feeders:
                self._current_feeders = None
        else:
            raise KeyError(feeder)

        return self

    def clear_current_feeders(self) -> Equipment:
        """
        Clear all current ``Feeder``s.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        self._current_feeders = None
        return self

    @property
    def num_usage_points(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint`s associated
        with this ``Equipment``
        """
        return nlen(self._usage_points)

    def get_usage_point(self, mrid: str) -> UsagePoint:
        """
        Get the ``UsagePoint`` for this ``Equipment`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint`
        :return: The :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._usage_points, mrid)

    def add_usage_point(self, up: UsagePoint) -> Equipment:
        """
        :param up: the :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint` to
        associate with this ``Equipment``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        require(not contains_mrid(self._usage_points, up.mrid),
                lambda: f"A UsagePoint with mRID {up.mrid} already exists in {str(self)}.")
        self._usage_points = list() if self._usage_points is None else self._usage_points
        self._usage_points.append(up)
        return self

    def remove_usage_point(self, up: UsagePoint) -> Equipment:
        """
        :param up: the :class:`zepben.cimbend.iec61968.metering.metering.UsagePoint` to
        disassociate with this ``Equipment``.
        :raises: KeyError if ``up`` was not associated with this ``Equipment``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        if self._usage_points is not None:
            self._usage_points.remove(up)
            if not self._usage_points:
                self._usage_points = None
        else:
            raise KeyError(up)

        return self

    def clear_usage_points(self) -> Equipment:
        """
        Clear all usage_points.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        self._usage_points = None
        return self

    @property
    def num_restrictions(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61968.operations.operational_restriction.OperationalRestriction`s
        associated with this ``Equipment``
        """
        return nlen(self._operational_restrictions)

    def get_restriction(self, mrid: str) -> OperationalRestriction:
        """
        Get the ``OperationalRestriction`` for this ``Equipment`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61968.operations.operational_restriction
        .OperationalRestriction`
        :return: The :class:`zepben.cimbend.iec61968.operations.operational_restriction.OperationalRestriction` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._operational_restrictions, mrid)

    def add_restriction(self, op: OperationalRestriction) -> Equipment:
        """
        :param op: The :class:`zepben.cimbend.iec61968.operations.operational_restriction.OperationalRestriction` to
        associate with this ``Equipment``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        require(not contains_mrid(self._operational_restrictions, op.mrid),
                lambda: f"An OperationalRestriction with mRID {op.mrid} already exists in {str(self)}.")
        self._operational_restrictions = list() if self._operational_restrictions is None else self._operational_restrictions
        self._operational_restrictions.append(op)
        return self

    def remove_restriction(self, op: OperationalRestriction) -> Equipment:
        """
        :param op: The :class:`zepben.cimbend.iec61968.operations.operational_restriction.OperationalRestriction` to
        disassociate with this ``Equipment``.
        :raises: KeyError if ``op`` was not associated with this ``Equipment``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        if self._operational_restrictions is not None:
            self._operational_restrictions.remove(op)
            if not self._operational_restrictions:
                self._operational_restrictions = None
        else:
            raise KeyError(op)

        return self

    def clear_restrictions(self) -> Equipment:
        """
        Clear all ``OperationalRestrictions``.
        :return: A reference to this ``Equipment`` to allow fluent use.
        """
        self._operational_restrictions = None
        return self

    def _equipment_containers_of_type(self, ectype) -> List[EquipmentContainer]:
        if self._equipment_containers:
            return [ec for ec in self._equipment_containers if isinstance(ec, ectype)]
        else:
            return []

    def pos_point(self, sequence_number):
        try:
            return self.location.position_points[sequence_number]
        except IndexError:
            return None

    def has_points(self):
        return len(self.location.position_points) > 0

    def has_usage_point(self, usage_point_mrid: str):
        return contains_mrid(self._usage_points, usage_point_mrid)
