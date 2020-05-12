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
from typing import List, Set, Optional, Generator, Tuple

from zepben.cimbend.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.cimbend.cim.iec61970.base.core.equipment import Equipment
from zepben.cimbend.exceptions import NoEquipmentException

__all__ = ['ConductingEquipment']

from zepben.cimbend.util import get_by_mrid, require, contains_mrid


@dataclass
class ConductingEquipment(Equipment):
    """
    Abstract class, should only be used through subclasses.
    The parts of the AC power system that are designed to carry current or that are conductively connected through
    terminals.

    ConductingEquipment are connected by :class:`zepben.cimbend.Terminal`'s which are in turn associated with
    :class:`zepben.cimbend.ConnectivityNode`'s. Each `Terminal` is associated with _exactly one_ `ConnectivityNode`,
    and through that `ConnectivityNode` can be linked with many other `Terminals` and thus `ConductingEquipment`.

    Attributes -
        - base_voltage : A :class:`zepben.cimbend.BaseVoltage`.
        - terminals : Conducting equipment have terminals that may be connected to other conducting equipment terminals
                      via connectivity nodes or topological nodes. The sequenceNumber of each ``Terminal`` is the index
                      of the Terminal in the list.
    """
    base_voltage: Optional[BaseVoltage] = None
    terminals_: InitVar[List[Terminal]] = field(default=list())
    _terminals: List[Terminal] = field(default_factory=list, init=False)

    def __post_init__(self, usagepoints: List[UsagePoint],
                      equipmentcontainers: List[EquipmentContainer],
                      operationalrestrictions: List[OperationalRestriction],
                      currentfeeders: List[Feeder],
                      terminals_: List[Terminal]):
        super().__post_init__(usagepoints, equipmentcontainers, operationalrestrictions, currentfeeders)
        for term in terminals_:
            term.conducting_equipment = self
            self.add_terminal(term)

    @property
    def nominal_voltage(self):
        return self.base_voltage.nominal_voltage if self.base_voltage is not None else 0

    @property
    def num_terminals(self):
        """
        Get the number of :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal`s for this ``ConductingEquipment``.
        """
        return len(self._terminals)

    @property
    def terminals(self) -> Generator[Tuple[int, Terminal], None, None]:
        """
        :return: Generator over the terminals of this ``ConductingEquipment``.
        """
        for i, term in enumerate(self._terminals):
            yield i, term

    def get_terminal_by_mrid(self, mrid: str) -> Terminal:
        """
        Get the ``Terminal`` for this ``ConductingEquipment`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal`
        :return: The :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal` with the specified ``mrid`` if it
        exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._terminals, mrid)

    def get_terminal_by_sn(self, sequence_number: int):
        """
        Get a ``Terminal`` by its sequenceNumber.
        :param sequence_number: The sequenceNumber of the `Terminal` in relation to this ``ConductingEquipment``.
        :raises: IndexError if this ``ConductingEquipment`` does not have ``sequence_number`` ``Terminal``'s.
        :return: The ``Terminal`` referred to by ``sequenceNumber``
        """
        return self._terminals[sequence_number]

    def __getitem__(self, item):
        return self.get_terminal_by_sn(item)

    def add_terminal(self, terminal: Terminal) -> ConductingEquipment:
        """
        :param terminal: the :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal` to add to this
        ``ConductingEquipment``, assigning it a sequence_number of ``num_terminals``.
        :return: A reference to this ``ConductingEquipment`` to allow fluent use.
        """
        self.insert_terminal(terminal)
        return self

    def insert_terminal(self, terminal: Terminal, sequence_number: int = None) -> ConductingEquipment:
        """
        :param terminal: the :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal` to
        associate with this ``ConductingEquipment``.
        :param sequence_number: The ``sequenceNumber`` for ``terminal``. You should aim to always insert ``Terminal``s
        in order.
        :return: A reference to this ``ConductingEquipment`` to allow fluent use.
        """
        if sequence_number is None:
            sequence_number = self.num_terminals
        require(terminal.conducting_equipment is self,
                lambda: f"Terminal {terminal} references another piece of conducting equipment ${terminal.conducting_equipment}, expected {self}.")
        require(not contains_mrid(self._terminals, terminal.mrid),
                lambda: f"A Terminal with mRID {terminal.mrid} already exists in {str(self)}.")
        require(0 <= sequence_number <= self.num_terminals,
                lambda: f"Unable to add Terminal to ConductingEquipment {self}. Sequence number {sequence_number} is invalid. "
                        f"Expected a value between 0 and {self.num_terminals}. Make sure you are adding the terminals in the correct order and there are no missing sequence numbers.")
        self._terminals.insert(sequence_number, terminal)
        return self

    def __setitem__(self, key, value):
        self.insert_terminal(value, key)

    def remove_terminal(self, terminal: Terminal) -> ConductingEquipment:
        """
        :param terminal: the :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal` to
        disassociate from this ``ConductingEquipment``.
        :raises: ValueError if ``terminal`` was not associated with this ``ConductingEquipment``.
        :return: A reference to this ``ConductingEquipment`` to allow fluent use.
        """
        self._terminals.remove(terminal)
        return self

    def clear_terminals(self) -> ConductingEquipment:
        """
        Clear all terminals.
        :return: A reference to this ``ConductingEquipment`` to allow fluent use.
        """
        self._terminals.clear()
        return self

    def __repr__(self):
        return (f"{super().__repr__()}, num_cores={self.num_cores} in_service={self.in_service}, "
                f"normally_in_service={self.normally_in_service}, location={self.location}"
                )

    def __lt__(self, other):
        """
        This definition should only be used for sorting within a :class:`zepben.cimbend.tracing.queue.PriorityQueue`
        :param other: Another Terminal to compare against
        :return: True if self has more cores than other, False otherwise.
        """
        return self.num_cores > other.num_cores

    @property
    def num_cores(self):
        return self.__num_cores

    def is_metered(self):
        """
        Check whether this piece of equipment is metered. A piece of equipment is metered if it's associated with at
        least one :class:`zepben.cimbend.UsagePoint` that has an :class:`zepben.cimbend.EndDevice` attached to it.
        :return: True if this equipment has at least one `EndDevice` on one `UsagePoint`, False otherwise.
        """
        for up in self.usage_points:
            if up.is_metered():
                return True
        else:
            return False

    def terminal_sequence_number(self, terminal):
        """
        Sequence number for terminals is stored as the index of the terminal in `self.terminals`
        :param terminal: The terminal to retrieve the sequence number for
        :return:
        """
        return self.get_terminal_by_mrid(terminal.mrid)

    def get_terminal_for_node(self, node):
        for t in self._terminals:
            if t.connectivity_node.mrid == node.mrid:
                return t
        raise NoEquipmentException(f"Equipment {self.mrid} is not connected to node {node.mrid}")

    def get_nominal_voltage(self, terminal=None):
        """
        Get the nominal voltage for this piece of equipment.
        In cases where this equipment has multiple nominal voltages (i.e, transformers),
        this method should be overridden so providing a terminal will provide the voltage corresponding to that terminal

        :param terminal: Terminal to fetch voltage for
        """
        return self.nominal_voltage

    def get_connected_equipment(self, exclude: Set = None):
        """
        Get all :class:`ConductingEquipment` connected to this piece of equipment. An `Equipment` is connected if it has
        a `Terminal` associated with a `ConnectivityNode` that this `ConductingEquipment` is also associated with.

        :param exclude: Equipment to exclude from return.
        :return: A list of `ConductingEquipment` that are connected to this.
        """
        if exclude is None:
            exclude = []
        connected_equip = []
        for terminal in self._terminals:
            conn_node = terminal.connectivity_node
            for term in conn_node:
                if term.conducting_equipment in exclude:
                    continue
                if term != terminal:  # Don't include ourselves.
                    connected_equip.append(term.conducting_equipment)
        return connected_equip

