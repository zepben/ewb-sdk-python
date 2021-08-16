#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Optional, Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Terminal

from zepben.evolve.model.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment

__all__ = ['ConductingEquipment']

from zepben.evolve.util import get_by_mrid, require, ngen


class ConductingEquipment(Equipment):
    """
    Abstract class, should only be used through subclasses.
    The parts of the AC power system that are designed to carry current or that are conductively connected through
    terminals.

    ConductingEquipment are connected by `zepben.evolve.cim.iec61970.base.core.Terminal`'s which are in turn associated with
    `zepben.evolve.cim.iec61970.base.connectivity_node.ConnectivityNode`'s. Each `zepben.evolve.iec61970.base.core.terminal.Terminal` is associated with
    _exactly one_ `ConnectivityNode`, and through that `ConnectivityNode` can be linked with many other `Terminals` and `ConductingEquipment`.
    """

    base_voltage: Optional[BaseVoltage] = None
    """`zepben.evolve.iec61970.base.core.base_voltage.BaseVoltage` of this `ConductingEquipment`. Use only when there is no voltage level container used and 
    only one base voltage applies. For example, not used for transformers."""

    _terminals: List[Terminal] = []

    def __init__(self, terminals: List[Terminal] = None, **kwargs):
        super(ConductingEquipment, self).__init__(**kwargs)
        if terminals:
            for term in terminals:
                if term.conducting_equipment is None:
                    term.conducting_equipment = self
                self.add_terminal(term)

    def get_base_voltage(self, terminal: Terminal = None):
        """
        Get the `zepben.evolve.iec61970.base.core.base_voltage.BaseVoltage` of this `ConductingEquipment`.
        Note `terminal` is not used here, but this method can be overridden in child classes (e.g PowerTransformer).

        `terminal` The `zepben.evolve.cim.iec61970.base.core.terminal.Terminal` to get the voltage at.
        Returns thee BaseVoltage of this `ConductingEquipment` at `terminal`
        """
        return self.base_voltage

    @property
    def terminals(self) -> Generator[Terminal, None, None]:
        """
        `ConductingEquipment` have `zepben.evolve.cim.iec61970.base.core.terminal.Terminal`s that may be connected to other `ConductingEquipment`
        `zepben.evolve.cim.iec61970.base.core.terminal.Terminal`s via `ConnectivityNode`s.
        """
        return ngen(self._terminals)

    def num_terminals(self):
        """
        Get the number of `zepben.evolve.cim.iec61970.base.core.terminal.Terminal`s for this `ConductingEquipment`.
        """
        return len(self._terminals)

    def get_terminal_by_mrid(self, mrid: str) -> Terminal:
        """
        Get the `zepben.evolve.iec61970.base.core.terminal.Terminal` for this `ConductingEquipment` identified by `mrid`

        `mrid` the mRID of the required `zepben.evolve.cim.iec61970.base.core.terminal.Terminal`
        Returns The `zepben.evolve.cim.iec61970.base.core.terminal.Terminal` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._terminals, mrid)

    def get_terminal_by_sn(self, sequence_number: int):
        """
        Get the `zepben.evolve.iec61970.base.core.terminal.Terminal` on this `ConductingEquipment` by its `sequence_number`.

        `sequence_number` The `sequence_number` of the `zepben.evolve.iec61970.base.core.terminal.Terminal` in relation to this `ConductingEquipment`.
        Returns The `zepben.evolve.iec61970.base.core.terminal.Terminal` on this `ConductingEquipment` with sequence number `sequence_number`
        Raises IndexError if no `zepben.evolve.iec61970.base.core.terminal.Terminal` was found with sequence_number `sequence_number`.
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

        `terminal` The `zepben.evolve.cim.iec61970.base.core.terminal.Terminal` to associate with this `ConductingEquipment`.
        Returns A reference to this `ConductingEquipment` to allow fluent use.
        Raises `ValueError` if another `zepben.evolve.iec61970.base.core.terminal.Terminal` with the same `mrid` already exists for this `ConductingEquipment`.
        """
        if self._validate_terminal(terminal):
            return self

        if terminal.sequence_number == 0:
            terminal.sequence_number = self.num_terminals() + 1

        self._terminals.append(terminal)
        self._terminals.sort(key=lambda t: t.sequence_number)

        return self

    def remove_terminal(self, terminal: Terminal) -> ConductingEquipment:
        """
        Disassociate `terminal` from this `ConductingEquipment`

        `terminal` the `zepben.evolve.cim.iec61970.base.core.terminal.Terminal` to disassociate from this `ConductingEquipment`.
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
        return (f"{super(ConductingEquipment, self).__repr__()}, in_service={self.in_service}, "
                f"normally_in_service={self.normally_in_service}, location={self.location}"
                )

    def _validate_terminal(self, terminal: Terminal) -> bool:
        """
        Validate a terminal against this `ConductingEquipment`'s `zepben.evolve.iec61970.base.core.terminal.Terminal`s.

        `terminal` The `zepben.evolve.iec61970.base.core.terminal.Terminal` to validate.
        Returns True if `zepben.evolve.iec61970.base.core.terminal.Terminal`` is already associated with this `ConductingEquipment`, otherwise False.
        Raises `ValueError` if `zepben.evolve.iec61970.base.core.terminal.Terminal`s `conducting_equipment` is not this `ConductingEquipment`,
        or if this `ConductingEquipment` has a different `zepben.evolve.iec61970.base.core.terminal.Terminal` with the same mRID.
        """
        if self._validate_reference(terminal, self.get_terminal_by_mrid, "A Terminal"):
            return True

        if self._validate_reference_by_sn(terminal.sequence_number, terminal, self.get_terminal_by_sn, "A Terminal"):
            return True

        if not terminal.conducting_equipment:
            terminal.conducting_equipment = self

        require(terminal.conducting_equipment is self,
                lambda: f"Terminal {terminal} references another piece of conducting equipment {terminal.conducting_equipment}, expected {str(self)}.")
        return False
