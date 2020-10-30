#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Set, Optional, Generator, Tuple

from zepben.cimbend.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.cimbend.cim.iec61970.base.core.equipment import Equipment
from zepben.cimbend.exceptions import NoEquipmentException

__all__ = ['ConductingEquipment']

from zepben.cimbend.util import get_by_mrid, require


class ConductingEquipment(Equipment):
    """
    Abstract class, should only be used through subclasses.
    The parts of the AC power system that are designed to carry current or that are conductively connected through
    terminals.

    ConductingEquipment are connected by `zepben.cimbend.cim.iec61970.base.core.Terminal`'s which are in turn associated with
    `zepben.cimbend.cim.iec61970.base.connectivity_node.ConnectivityNode`'s. Each `zepben.cimbend.iec61970.base.core.terminal.Terminal` is associated with
    _exactly one_ `ConnectivityNode`, and through that `ConnectivityNode` can be linked with many other `Terminals` and `ConductingEquipment`.
    """

    base_voltage: Optional[BaseVoltage] = None
    """`zepben.cimbend.iec61970.base.core.base_voltage.BaseVoltage` of this `ConductingEquipment`. Use only when there is no voltage level container used and 
    only one base voltage applies. For example, not used for transformers."""

    _terminals: List[Terminal] = []

    def __init__(self, usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                 operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None, terminals: List[Terminal] = None):
        super(ConductingEquipment, self).__init__(usage_points, equipment_containers, operational_restrictions, current_feeders)
        if terminals:
            for term in terminals:
                self.add_terminal(term)

    @property
    def nominal_voltage(self):
        return self.base_voltage.nominal_voltage if self.base_voltage is not None else 0

    @property
    def terminals(self) -> Generator[Terminal, None, None]:
        """
        `ConductingEquipment` have `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal`s that may be connected to other `ConductingEquipment`
        `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal`s via `ConnectivityNode`s.
        """
        for term in self._terminals:
            yield term

    def num_terminals(self):
        """
        Get the number of `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal`s for this `ConductingEquipment`.
        """
        return len(self._terminals)

    def get_terminal_by_mrid(self, mrid: str) -> Terminal:
        """
        Get the `zepben.cimbend.iec61970.base.core.terminal.Terminal` for this `ConductingEquipment` identified by `mrid`

        `mrid` the mRID of the required `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal`
        Returns The `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._terminals, mrid)

    def get_terminal_by_sn(self, sequence_number: int):
        """
        Get the `zepben.cimbend.iec61970.base.core.terminal.Terminal` on this `ConductingEquipment` by its `sequence_number`.

        `sequence_number` The `sequence_number` of the `zepben.cimbend.iec61970.base.core.terminal.Terminal` in relation to this `ConductingEquipment`.
        Returns The `zepben.cimbend.iec61970.base.core.terminal.Terminal` on this `ConductingEquipment` with sequence number `sequence_number`
        Raises IndexError if no `zepben.cimbend.iec61970.base.core.terminal.Terminal` was found with sequence_number `sequence_number`.
        """
        for term in self._terminals:
            if term.sequence_number == sequence_number:
                return term
        raise IndexError(f"No Terminal with sequence_number {sequence_number} was found in ConductingEquipment {str(self)}")

    def __getitem__(self, item: int):
        return self.get_terminal_by_sn(item)

    def add_terminal(self, terminal: Terminal) -> ConductingEquipment:
        """
        Associate `terminal` with this `ConductingEquipment`. If `terminal.sequence_number` == 0, the terminal will be assigned a sequence_number of
        `self.num_terminals() + 1`.

        `terminal` The `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal` to associate with this `ConductingEquipment`.
        Returns A reference to this `ConductingEquipment` to allow fluent use.
        Raises `ValueError` if another `zepben.cimbend.iec61970.base.core.terminal.Terminal` with the same `mrid` already exists for this `ConductingEquipment`.
        """
        if terminal.sequence_number == 0:
            terminal.sequence_number = self.num_terminals() + 1

        if self._validate_terminal(terminal):
            return self

        self._terminals.append(terminal)
        self._terminals.sort(key=lambda t: t.sequence_number)

        return self

    def remove_terminal(self, terminal: Terminal) -> ConductingEquipment:
        """
        Disassociate `terminal` from this `ConductingEquipment`

        `terminal` the `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal` to disassociate from this `ConductingEquipment`.
        Returns A reference to this `ConductingEquipment` to allow fluent use.
        Raises `ValueError` if `terminal` was not associated with this `ConductingEquipment`.
        """
        self._terminals.remove(terminal)
        return self

    def clear_terminals(self) -> ConductingEquipment:
        """
        Clear all terminals.
        Returns A reference to this `ConductingEquipment` to allow fluent use.
        """
        self._terminals.clear()
        return self

    def __repr__(self):
        return (f"{super().__repr__()}, num_cores={self.num_cores} in_service={self.in_service}, "
                f"normally_in_service={self.normally_in_service}, location={self.location}"
                )

    def __lt__(self, other):
        """
        This definition should only be used for sorting within a `zepben.cimbend.tracing.queue.PriorityQueue`
        `other` Another Terminal to compare against
        Returns True if self has more cores than other, False otherwise.
        """
        return self.num_cores > other.num_cores

    def _validate_terminal(self, terminal: Terminal) -> bool:
        """
        Validate a terminal against this `ConductingEquipment`'s `zepben.cimbend.iec61970.base.core.terminal.Terminal`s.

        `terminal` The `zepben.cimbend.iec61970.base.core.terminal.Terminal` to validate.
        Returns True if `zepben.cimbend.iec61970.base.core.terminal.Terminal`` is already associated with this `ConductingEquipment`, otherwise False.
        Raises `ValueError` if `zepben.cimbend.iec61970.base.core.terminal.Terminal`s `conducting_equipment` is not this `ConductingEquipment`,
        or if this `ConductingEquipment` has a different `zepben.cimbend.iec61970.base.core.terminal.Terminal` with the same mRID.
        """
        if self._validate_reference(terminal, self.get_terminal_by_mrid, "A Terminal"):
            return True

        if self._validate_reference_by_sn(terminal.sequence_number, terminal, self.get_terminal_by_sn, "A Terminal"):
            return True

        require(terminal.conducting_equipment is self,
                lambda: f"Terminal {terminal} references another piece of conducting equipment {terminal.conducting_equipment}, expected {str(self)}.")
        return False

    def get_terminal_for_node(self, node):
        for t in self._terminals:
            if t.connectivity_node.mrid == node.mrid:
                return t
        raise NoEquipmentException(f"Equipment {self.mrid} is not connected to node {node.mrid}")

    def get_connected_equipment(self, exclude: Set = None):
        """
        Get all `ConductingEquipment` connected to this piece of equipment. An `Equipment` is connected if it has
        a `zepben.cimbend.iec61970.base.core.terminal.Terminal` associated with a `ConnectivityNode` that this `ConductingEquipment` is also associated with.

        `exclude` Equipment to exclude from return.
        Returns A list of `ConductingEquipment` that are connected to this.
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
