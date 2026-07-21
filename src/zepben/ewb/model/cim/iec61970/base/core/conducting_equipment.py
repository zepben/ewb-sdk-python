#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['ConductingEquipment']

import sys
from typing import List, Optional, Generator, TYPE_CHECKING, Union
from abc import ABCMeta
from dataclasses import field

from typing_extensions import deprecated

from zepben.ewb.dataclass_descriptors.mrid_list import LazyMridList, Backfill
from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
from zepben.ewb.util import get_by_mrid, require, ngen
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.base_voltage import BaseVoltage


class TerminalsList(LazyMridList[Terminal]):

    def get_by_sequence_number(self, sequence_number: int) -> Terminal:
        term = next((it for it in self if it.sequence_number == sequence_number), None)
        if term is None:
            raise IndexError(f"No Terminal with sequence_number {sequence_number} was found in ConductingEquipment {str(self.instance)}")
        return term

@zb_dataclass
class ConductingEquipment(Equipment, metaclass=ABCMeta):
    """
    Abstract class, should only be used through subclasses.
    The parts of the AC power system that are designed to carry current or that are conductively connected through
    terminals.

    ConductingEquipment are connected by `Terminal`'s which are in turn associated with
    `ConnectivityNode`'s. Each `Terminal` is associated with
    _exactly one_ `ConnectivityNode`, and through that `ConnectivityNode` can be linked with many other `Terminals` and `ConductingEquipment`.
    """

    base_voltage: Optional[BaseVoltage] = None
    """
    `BaseVoltage` of this `ConductingEquipment`. Use only when there is no voltage level container used and only one base voltage applies. For example, not
    used for transformers.
    """

    _terminals: List[Terminal] = field(default_factory=list)
    max_terminals = int(sys.maxsize)

    # pylint: disable=unused-argument
    def get_base_voltage(self, terminal: Terminal = None):
        """
        Get the `BaseVoltage` of this `ConductingEquipment`.
        Note `terminal` is not used here, but this method can be overridden in child classes (e.g PowerTransformer).

        `terminal` The `Terminal` to get the voltage at.
        Returns thee BaseVoltage of this `ConductingEquipment` at `terminal`
        """
        return self.base_voltage

    # pylint: enable=unused-argument

    @property
    def base_voltage_value(self) -> int:
        """
        :return: The value of the nominal voltage for the base voltage if there is one, otherwise 0.
        """
        return self.base_voltage.nominal_voltage if self.base_voltage and self.base_voltage.nominal_voltage else 0

    terminals: TerminalsList = TerminalsList(
        _terminals,
        "A Terminal",
        backfill=Backfill(Terminal.conducting_equipment),
        validate=lambda self, it: self._validate_terminal(it),
        sort_by=lambda it: it.sequence_number
    )

    def __repr__(self):
        return (f"{super(ConductingEquipment, self).__repr__()}, in_service={self.in_service}, "
                f"normally_in_service={self.normally_in_service}, location={self.location}"
                )

    def _validate_terminal(self, terminal: Terminal) -> bool:
        """
        Validate a terminal against this `ConductingEquipment`'s `Terminal`s.

        `terminal` The `Terminal` to validate.
        Returns True if `Terminal`` is already associated with this `ConductingEquipment`, otherwise False.
        Raises `ValueError` if `Terminal`s `conducting_equipment` is not this `ConductingEquipment`,
        or if this `ConductingEquipment` has a different `Terminal` with the same mRID.
        """
        if self._validate_reference_by_field(terminal, terminal.sequence_number, self.get_terminal_by_sn, "sequence_number"):
            return True

        require(self.num_terminals() < self.max_terminals,
                lambda: f"Unable to add {terminal} to {str(self)}. This conducting equipment already has the maximum number of terminals ({self.max_terminals}).")

        if terminal.sequence_number == 0:
            terminal.sequence_number = self.num_terminals() + 1

        return False


    # region deprecated list boilerplate

    # region terminals boilerplate

    @deprecated("Use len(terminals) instead.")
    def num_terminals(self) -> int:
        return len(self.terminals)

    @deprecated(
        "Use terminals.get_by_sequence_number(identifier) for integer identifiers " +
        "or terminals.get_by_mrid(identifier) for string identifiers instead."
    )
    def get_terminal(self, identifier: Union[int, str]) -> Terminal:
        if isinstance(identifier, int):
            return self.terminals.get_by_sequence_number(identifier)

        if isinstance(identifier, str):
            return self.terminals.get_by_mrid(identifier)

        raise TypeError(
            f"`identifier` parameter not a recognised type: {type(identifier)}"
        )

    @deprecated("Use terminals.get_by_mrid(mrid) instead.")
    def get_terminal_by_mrid(self, mrid: str) -> Terminal:
        return self.terminals.get_by_mrid(mrid)

    @deprecated(
        "Use terminals.get_by_sequence_number(sequence_number) instead."
    )
    def get_terminal_by_sn(self, sequence_number: int) -> Terminal:
        return self.terminals.get_by_sequence_number(sequence_number)

    @deprecated("Use terminals.get_by_sequence_number(item) instead.")
    def __getitem__(self, item: int) -> Terminal:
        return self.terminals.get_by_sequence_number(item)

    @deprecated("Use terminals.append(terminal) instead.")
    def add_terminal(self, terminal: Terminal) -> ConductingEquipment:
        self.terminals.append(terminal)
        return self

    @deprecated("Use terminals.remove(terminal) instead.")
    def remove_terminal(self, terminal: Terminal) -> ConductingEquipment:
        self.terminals.remove(terminal)
        return self

    @deprecated("Use terminals.clear() instead.")
    def clear_terminals(self) -> ConductingEquipment:
        self.terminals.clear()
        return self

    # endregion

    # endregion
