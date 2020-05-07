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

from dataclasses import dataclass, field, InitVar
from typing import Optional, Dict, Set, Generator, List

from zepben.cimbend.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.cimbend.util import nlen, ngen, contains_mrid

__all__ = ['EquipmentContainer', 'Feeder', 'Site']


@dataclass
class EquipmentContainer(ConnectivityNodeContainer):
    """
    A modeling construct to provide a root class for containing equipment.

    Attributes -
        _equipment : The :class:`equipment.Equipment` contained in this ``EquipmentContainer``
    """

    equipment_: InitVar[List[Equipment]] = field(default=list())
    _equipment: Optional[Dict[str, Equipment]] = field(init=False, default=None)

    def __post_init__(self, equipment_: List[Equipment]):
        super().__post_init__()
        for eq in equipment_:
            self.add_equipment(eq)

    @property
    def num_equipment(self):
        """
        :return: The number of :class:`equipment.Equipment`s associated with this ``EquipmentContainer``
        """
        return nlen(self._equipment)

    @property
    def equipment(self) -> Generator[Equipment, None, None]:
        """
        :return: Generator over the ``Equipment``s of this ``EquipmentContainer``.
        """
        return ngen(self._equipment)

    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the ``Equipment`` for this ``EquipmentContainer`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`equipment.Equipment`
        :return: The :class:`equipment.Equipment` with the specified ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return self._equipment[mrid]

    def add_equipment(self, equipment: Equipment) -> Equipment:
        """
        :param equipment: the :class:`equipment.Equipment` to associate with this ``EquipmentContainer``.
        :return: The previous ``Equipment`` stored by ``equipment``s mrid, otherwise ``equipment`` is returned
        if there was no previous value.
        """
        self._equipment = dict() if self._equipment is None else self._equipment
        return self._equipment.setdefault(equipment.mrid, equipment)

    def remove_equipment(self, equipment: Equipment) -> Equipment:
        """
        :param equipment: the :class:`equipment.Equipment` to disassociate with this ``EquipmentContainer``.
        :raises: KeyError if ``equipment`` was not associated with this ``EquipmentContainer``.
        :return: The previous ``Equipment`` stored by ``equipment``s mrid if it existed.
        """
        if self._equipment is not None:
            previous = self._equipment[equipment.mrid]
            del self._equipment[equipment.mrid]
        else:
            raise KeyError(equipment)

        if not self._equipment:
            self._equipment = None
        return previous

    def clear_equipment(self) -> EquipmentContainer:
        """
        Clear all equipment.
        :return: A reference to this ``EquipmentContainer`` to allow fluent use.
        """
        self._equipment = None
        return self

    def current_feeders(self) -> Generator[Feeder, None, None]:
        """
        Convenience function to find all of the current feeders of the equipment associated with this equipment container.
        :return: the current feeders for all associated feeders
        """
        seen = set()
        for equip in self._equipment.values():
            for f in equip.current_feeders:
                if f not in seen:
                    seen.add(f.mrid)
                    yield f

    def normal_feeders(self) -> Generator[Feeder, None, None]:
        """
        Convenience function to find all of the normal feeders of the equipment associated with this equipment container.
        :return: the normal feeders for all associated feeders
        """
        seen = set()
        for equip in self._equipment.values():
            for f in equip.normal_feeders:
                if f not in seen:
                    seen.add(f.mrid)
                    yield f


@dataclass
class Feeder(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources.
    The organization of a feeder does not necessarily reflect connectivity or current operation state.

    Attributes -
        normal_head_terminal : The normal head terminal or terminals of the feeder.
        normal_energizing_substation : The substation that nominally energizes the feeder. Also used for naming purposes.
        _current_equipment : The :class:`equipment.Equipment` of this ``Feeder``
    """
    normal_head_terminal: Optional[Terminal] = None
    normal_energizing_substation: Optional[Substation] = None
    currentequipment: InitVar[List[Equipment]] = field(default=list())
    _current_equipment: Optional[Dict[str, Equipment]] = field(init=False, default=None)

    def __post_init__(self, equipment_: List[Equipment], currentequipment: List[Equipment]):
        super().__post_init__(equipment_)
        for eq in currentequipment:
            self.add_current_equipment(eq)

    @property
    def num_current_equipment(self):
        """
        :return: The number of :class:`equipment.Equipment`s associated with this ``Feeder``
        """
        return nlen(self._current_equipment)

    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the ``Equipment`` for this ``Feeder`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`equipment.Equipment`
        :return: The :class:`equipment.Equipment` with the specified ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return self._current_equipment[mrid]

    @property
    def current_equipment(self) -> Generator[Equipment, None, None]:
        """
        Perform the specified action against each :class:`equipment.Equipment` associated with this ``Feeder``.

        :return: A reference to this ``Feeder`` to allow fluent use.
        """
        return ngen(self._current_equipment)

    def add_current_equipment(self, equipment: Equipment) -> Equipment:
        """
        :param equipment: the :class:`equipment.Equipment` to associate with this ``Feeder``.
        :return: The previous ``Equipment`` stored by ``equipment``s mrid, otherwise ``equipment`` is returned
        if there was no previous value.
        """
        self._current_equipment = dict() if self._current_equipment is None else self._current_equipment
        return self._current_equipment.setdefault(equipment.mrid, equipment)

    def remove_current_equipment(self, equipment: Equipment) -> Equipment:
        """
        :param equipment: the :class:`equipment.Equipment` to disassociate with this ``Feeder``.
        :raises: KeyError if ``equipment`` was not associated with this ``Feeder``.
        :return: The previous ``Equipment`` stored by ``equipment``s mrid if it existed.
        """
        if self._current_equipment is not None:
            previous = self._current_equipment[equipment.mrid]
            del self._current_equipment[equipment.mrid]
        else:
            raise KeyError(equipment)

        if not self._current_equipment:
            self._current_equipment = None
        return previous

    def clear_current_equipment(self) -> Feeder:
        """
        Clear all equipment.
        :return: A reference to this ``Feeder`` to allow fluent use.
        """
        self._current_equipment = None
        return self


@dataclass
class Site(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources located at a site.
    Note this is not a CIM concept - however represents an ``EquipmentContainer`` in CIM. This is to avoid the use of
    ``EquipmentContainer`` as a concrete class.
    """
    pass
